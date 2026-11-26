import os
import sys

BLOCK_SIZE = 512
MAG_NUM = b"4348PRJ3"
INT_SIZE = 8
MAX_KEYS = 19
MAX_CHILDREN = 20

# Convert integer to big endian 
def int_to_big(n):
    return n.to_bytes(INT_SIZE, "big")

# Convert big endian to integer
def big_to_int(b):
    return int.from_bytes(b, "big")

# Read one 512 byte block
def read_block(f, block_id):
    f.seek(block_id * BLOCK_SIZE)
    data = f.read(BLOCK_SIZE)
    if len(data) != BLOCK_SIZE:
        raise ValueError(f"Block id: {block_id} invalid read")
    return data

# Write data to one 512 byte block
def write_block(f, block_id, data):
    if len(data) > BLOCK_SIZE:
        raise ValueError("data size exceeds block")
    f.seek(block_id * BLOCK_SIZE)
    f.write(data.ljust(BLOCK_SIZE, b"\x00"))

# Build header by writing its contents to block 0
def write_header(f, root_id, next_block_id):
    write_block(f, 0, MAG_NUM + int_to_big(root_id) + int_to_big(next_block_id))

# Read block 0
def read_header(f):
    block = read_block(f, 0)
    if block[0:8] != MAG_NUM:   # Verifies magic number
        raise ValueError("bad magic number")    
    return big_to_int(block[8:16]), big_to_int(block[16:24])

# Exit system and print error message
def kill(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

# B tree node
class Node:
    def __init__(self, block_id, parent=0, keys=None, values=None, children=None):
        self.block_id = block_id
        self.parent = parent
        self.keys = keys or []
        self.values = values or []
        self.children = children or [0] * MAX_CHILDREN

# Write a whole node and all its contents to a block
def write_node(f, node):
    # Convert block id, parent id, and current number of keys to big endian
    data = int_to_big(node.block_id) + int_to_big(node.parent) + int_to_big(len(node.keys))

    # Convert keys, values, and children to big endian
    for i in range(MAX_KEYS):
        data += int_to_big(node.keys[i] if i < len(node.keys) else 0)   # Empty slots are padded with 0s
    for i in range(MAX_KEYS):
        data += int_to_big(node.values[i] if i < len(node.values) else 0)
    for child in node.children:
        data += int_to_big(child)

    # Write to block
    write_block(f, node.block_id, data)

# Read from a block as a Node object
def read_node(f, block_id):
    b = read_block(f, block_id) # Read block as bytes
    n = big_to_int(b[16:24])    # Number of keys in the node
    
    # If the number of keys is greater than the maximum number, raise an error.
    if n > MAX_KEYS:
        raise ValueError(f"Block id: {block_id} has a greater amount than {MAX_KEYS} keys ({n}).")

    # Convert keys, values, and children from big endian to integers
    keys = [big_to_int(b[24 + 8 * i:32 + 8 * i]) for i in range(n)]
    values = [big_to_int(b[176 + 8 * i:184 + 8 * i]) for i in range(n)]
    children = [big_to_int(b[328 + 8 * i:336 + 8 * i]) for i in range(MAX_CHILDREN)]

    # Return as a Node object
    return Node(big_to_int(b[0:8]), big_to_int(b[8:16]), keys, values, children)

# Validate index file before opening it
def open_idx(path, mode="r+b"):

    # Check to see if file exists
    if not os.path.isfile(path):
        kill(f"index file '{path}' does not exist")

    # Opens file
    f = open(path, mode)

    # Check file size and read header
    try:
        if os.path.getsize(path) % BLOCK_SIZE != 0:
            raise ValueError("Invalid file size (must be multiple of 512)")
        read_header(f)

    # Check to see if the index file is valid
    except ValueError:
        f.close()
        kill(f"'{path}' is an invalid index file")
    return f

# Check if a key is valid then returns it as an integer
def check_key(s):
    # Valid if ascii and a digit less than 2^64
    if not (s.isascii() and s.isdigit()) or int(s) >= 2 ** 64:
        kill(f"'{s}' is an invalid unsigned integer")
    return int(s)

# Search tree for a node with a key that matches the key we are searching for. If found, return the key and its value. If not found, return None.
def search_tree(f, key):
    # Read the header to get the block id of the root
    block_id, _ = read_header(f)

    # Leaf node = 0
    # Traverse the tree until the block id is 0
    while block_id != 0:
        # Read current node
        node = read_node(f, block_id)
        
        # Iterate throught the keys
        i = 0

        # Skip any keys less than what we are searching for
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # i is the first key either equal to or greater than the key we are searching for
        if i < len(node.keys) and node.keys[i] == key:
            return node.keys[i], node.values[i] # If the key is equal, return the key and its value.
        block_id = node.children[i] # No match -> child is now the next node we look at

    # No more nodes to check
    return None

# Creates new index file
def create(args):
    if len(args) != 1:
        kill("usage: py CS-4348.503-Project-3-irp220000.py create <file>")
    path = args[0]
    try:
        with open(path, "xb") as f: # Create new file and write header
            write_header(f, 0, 1)

    # File already exists
    except FileExistsError:
        kill(f"file '{path}' already exists")
    # File can't be created
    except OSError as e:
        kill(f"could not create '{path}': {e.strerror}")

# Validate the search command
def search(args):
    # Kill if invalid number of arguments
    if len(args) != 2:
        kill("usage: py CS-4348.503-Project-3-irp220000.py search <file> <key>")
    key = check_key(args[1])    # Validate key

    # Validate index file and open as f
    with open_idx(args[0], "rb") as f:
        result = search_tree(f, key)    # Search tree for a match on the key given in the arguments
    
    # No key found, kill program
    if result is None:
        kill(f"key {key} not found")
    
    # Print key and value
    print(f"{result[0]},{result[1]}")

COMMANDS = {
    "create": create,
    "search": search
}

def main():
    if len(sys.argv) < 2:
        kill("usage: py CS-4348.503-Project-3-irp220000.py <command> [args]")
    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        kill(f"invalid command '{cmd}'")
    COMMANDS[cmd](sys.argv[2:])


if __name__ == "__main__":
    main()