Python3 Cuckoo Hash Table 

This uses 2 separate arrays, both half the length of "size"
Each item to be inserted is hashed twice.

Cuckoo hashing utilizes 2 hash functions in order to minimize collisions. The hash table in this particular implementation contains 2 lists, each one using a different hash function. When inserting into a cuckoo hash table, hash the key twice to identify 2 possible "nests" (or "buckets") for the key/data pair. If both of its nests are already occupied, evict the occupant of 1 of the nests and then repeat the insertion step for the evicted occupant.

Cuckoo hashing is also very efficient for searching. It has a worst case lookup time of O(1)! This is a vast improvement from many hash table implementations with a worst case of O(N).

When inserting into a cuckoo hash table, it's important to consider all of the potential problems that may arise. 
   - Firstly, the table may fill up, so there must be steps in place to ensure that when the table starts to fill, it will expand and all of the items will be rehashed (with new hash functions) into their proper positions. One should aim to keep the number of keys under half the capacity of the hash table (total number of nests // 2).

   - Furthermore, an infinite loop may be encountered while cuckoo hashing. This occurs if there are 2 or more items that are continuously displacing one another and are never able to find a permanent position. There should be a certain threshold in the code to detect these infinite loops and deal with them. Once detected, 2 new hash functions should be used to rehash the entire contents of the table. If this again results in an infinite loop, the table should be expanded and rehashed (as mentioned above).
