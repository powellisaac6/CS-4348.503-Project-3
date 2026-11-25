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
