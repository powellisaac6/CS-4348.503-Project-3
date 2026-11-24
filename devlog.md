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
