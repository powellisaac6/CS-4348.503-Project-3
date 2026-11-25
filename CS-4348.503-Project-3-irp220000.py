import sys

BLOCK_SIZE = 512
MAG_NUM = b"4348PRJ3"
INT_SIZE = 8

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

# Builds header by writing its contents to block 0
def write_header(f, root_id, next_block_id):
    write_block(f, 0, MAG_NUM + int_to_big(root_id) + int_to_big(next_block_id))

# Reads block 0
def read_header(f):
    block = read_block(f, 0)
    if block[0:8] != MAG_NUM:   # Verifies magic number
        raise ValueError("bad magic number")    
    return big_to_int(block[8:16]), big_to_int(block[16:24])

# Exits system and prints error message
def kill(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)

# Creates new index file
def create(args):
    if len(args) != 1:
        kill("usage: py CS-4348.503-Project-3-irp220000.py create <file>")
    path = args[0]
    try:
        with open(path, "xb") as f: # Create new file and write header
            write_header(f, 0, 1)
    except FileExistsError:
        kill(f"file '{path}' already exists")
    except OSError as e:
        kill(f"could not create '{path}': {e.strerror}")


COMMANDS = {
    "create": create
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