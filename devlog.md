# Session 1 
### 11-24-2026 4:55 PM
Before I start session 1, I would like to give my thoughts on the project.
The project uses a B-tree to store data similarly to a database.
There are keys and values associated to each entry in the B-tree.
The key acts as an identifier for the entry while the value is the data meant to be stored.
test.idx stores everything using 512 byte blocks. 
The block id of the tree's root and the next block to be added to the file are both stored in block 0 (also called the header).
The header stores the magic number as well.
The magic number is an 8 byte value located at the top of the index file that indicates the type of file it is.
Each node of the B-tree is a subsequent block and can hold up to 19 keys.
The middle key moves up to the parent when a node becomes full balancing the tree.
The commands include create, insert, search, load, print, and extract.
I believe inserting will be the most difficult part of this project due to the balancing algorithm.
I chose to use Python because it's simple and the code I am the most familiar with.

For this session, I would like to implement the header and the create function.
I also want to implement functions for the big endian integers and 512 byte blocks.
The big endian function will convert a python integer into big endian order.
There will also be a reverse function converting big endian order to an integer.
I'll have a read function to view the contents of a block.
I'll also have a write function to change the contents of a block.
There will be a separate read and write function for the header.

NOTE: Timestamps indicate when the devlog entry was started.
I will do an initial entry before coding giving my thoughts and approach for the session, then a closing entry after coding which will state any challenges I came across and how I implemented my approach.

### 11-24-2026 6:30 PM
Big endian conversion functions, read/write block functions, read/write header functions, and the create function were all implemented.
I tested the create function which created an index file.
I checked its contents and it was exactly 512 bytes with the first 8 bytes being the magic number (4348PRJ3).
The tree was empty so the root id was 0 and the next block id was 1.

I ran into a small error trying to use python3 to run the project file on my computer.
I ended up just using "py" to run it instead since python3 kept giving me a Microsoft Store message.

I added some error handling to protect against invalid arguments, a file that already exists, and an unknown command.
I tested the create function on an index file that already exists, then with a missing argument.
Both gave the expected errors.
Lastly, I tested on an invalid command which also returned the expected error.

Next session, I want to create the structure for the B-Tree and implement the search command.
I expect coding the B-Tree will be the most difficult part due to its multikey node structure and balancing.

# Session 2
### 11-25-2026 2:31 PM
This session I'm planning on implementing the actual B-Tree structure itself.
Each node is stored in a block.
Each block stores a block id, the parent's block id, the current number of keys, 19 keys, 19 values, and 20 pointers to children.
8 byte big endian integers are used to store everything.

I'll implement the search algorithm to start at the root id which I can get from the header.
It'll read that node and attempt to search for the key in it.
If the key is not found, the search function will be directed to the child pointer that falls in range of the key.

If the child pointer is 0, that means the child is a leaf.
If the parent id is 0, that means the node is the root.
I haven't figured out what I'm going to do for when the search reaches a 0 pointer.
I imagine this will be the most challenging part.

I also want to implement a read function for the nodes themselves to allow the search algorithm to sift through the nodes easier.
I figure I might as well add the write algorithm while I'm at it since I will need some sort of way to fill the tree for a test.

### 11-25-2026 6:52 PM
I have finished everything for this session.
The first thing I implemented was the node structure which ended up being easier than I expected.
The trickiest part for me was understanding how to read and write the node.
I started by writing the block id, parent id, and number of keys first then used loops to add the keys, values, and child pointers.
It seemed odd to write all the data to a single variable at first.
I originally had multiple data variables that I was going to combine at the end of the function.
I got confused having so many of the same variable so I decided just to concatenate to a single variable.
The read_node function ended up being tricky because I had to calculate the offset for each element of the node.
Writing it out on a piece of paper helped me a lot.

I wrote some validation functions such as open_idx and check_key.
This is to ensure that a correct index file is being opened and an unsigned integer is being used as the search key.
Several other functions include validation. 
For instance, search utilizes both open_idx and check_key before it searches the tree.
All of these are to prevent the user from sending an out of bound command.

Turns out reaching a child pointer of 0 was a simple solution.
You just stop the search.
This is because when the search reaches 0, either the tree is empty or you have encountered a leaf.
Either case means the key hasn't been found.

I wrote a script to test it although it's very awkward since I'm only using write_node instead of insert.
I basically have to give it a premade tree from scratch.
I created a 2 level B-Tree then conducted a search for a key in the root, a key in each child, a key not in the tree, an invalid key, an invalid file, and an empty tree.
The correct keys/values and errors were given so everything works as intended.

Next session, I'm going to start implementing insert.
I think I'll keep it simple and avoid splitting for now.
Insertion alone should be enough work for a single session.