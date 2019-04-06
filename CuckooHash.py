from BitHash import BitHash, ResetBitHash
import random 

class Node(object):
    def __init__(self, k, d):
        self.key  = k 
        self.data = d

    def __str__(self):
        return "(" + str(self.key) + ", " + str(self.data) + ")"
    
class HashTab(object):
    def __init__(self, size):
        self.__hashArray1 = [None] * (size // 2)  # create 2 arrays, both half the length of size
        self.__hashArray2 = [None] * (size // 2)
        self.__numRecords = 0               # total number of nodes 
        self.__size = size                  # total size of hash table (both lists)

   # return current number of keys in table    
    def __len__(self): return self.__numRecords

    def hashFunc(self, s):
        x = BitHash(s)          # hash twice 
        y = BitHash(s, x)

        size = self.__size // 2  
        
        return x % size, y % size

    # insert and return true, return False if the key/data is already there,
    # grow the table if necessary 
    def insert(self, k, d):
        if self.find(k) != None:  return False   # if already there, return False (no duplicates)
        
        n = Node(k, d)                           # create a new node with key/data

        # increase size of table if necessary 
        if self.__numRecords >= (self.__size // 2):
            self.__growHash() 

        position1, position2 = self.hashFunc(n.key)  # hash

        # start the loop checking the 1st position in table 1
        pos = position1
        table = self.__hashArray1

        #       
        for i in range(5):
            
            if table[pos] == None:               # if the position in the current table is empty
                table[pos] = n                   # insert the node there and return True
                self.__numRecords += 1
                return True
            
            n, table[pos] = table[pos], n       # else, evict item in pos and insert the item
                                                # then deal with the displaced node.

            if pos == position1:                            # if we're checking the 1st table right now, 
                position1, position2 = self.hashFunc(n.key) # hash the displaced node,
                pos = position2                             # and check its 2nd position 
                table = self.__hashArray2                   # in the 2nd table (next time through loop)
            else:                               
                position1, position2 = self.hashFunc(n.key) # otherwise, hash the displaced node,
                pos == position1                            # and check the 1st table position. 
                table = self.__hashArray1
                
        self.__growHash()               # grow and rehash if we make it here  
        self.rehash(self.__size)                           
        self.insert(n.key, n.data)      # deal with evicted item

        return True

    # return string representation of both tables
    def __str__(self):
        str1 = "Table 1: [ " + str(self.__hashArray1[0]) 
        str2 = " Table 2: [ " + str(self.__hashArray2[0]) 
        for i in range(1, self.__size):
            str1 += ", " + str(self.__hashArray1[i])
        str1 += "]"

        for i in range(1, self.__size):
           str2 += ", " + str(self.__hashArray2[i]) 
        str2 += "]"
        
        return str1 + str2 

    # get new hash functions and reinsert everything 
    def rehash(self, size):
        ResetBitHash()          # get new hash functions
        
        temp = HashTab(size)    # create new hash tables

        # re-hash each item and insert it into the correct position in the new tables
        for i in range(self.__size // 2):
            x = self.__hashArray1[i]
            y = self.__hashArray2[i]
            if x != None:
                temp.insert(x.key, x.data)
            if y != None:
                temp.insert(y.key, y.data)

        # save new tables 
        self.__hashArray1 = temp.__hashArray1
        self.__hashArray2 = temp.__hashArray2
        self.__numRecords = temp.__numRecords
        self.__size = temp.__size
      
        
    # Increase the hash table's size x 2 
    def __growHash(self):
        newSize = self.__size * 2
        # re-hash each item and insert it into the
        # correct position in the new table
        self.rehash(newSize)

   
    # Return data if there, otherwise return None
    def find(self, k):
        pos1, pos2 = self.hashFunc(k)               # check both positions the key/data
        x = self.__hashArray1[pos1]                 # could be in. return data if found.
        y = self.__hashArray2[pos2]                 
        if x != None and x.key == k:  return x.data
        if y != None and y.key == k:  return y.data
    
        # return None if the key can't be found     
        return None

    # delete the node associated with that key and return True on success
    def delete(self, k):
        pos1, pos2 = self.hashFunc(k)  
        x = self.__hashArray1[pos1]
        y = self.__hashArray2[pos2]
        if  x != None and  x.key == k:  self.__hashArray1[pos1] = None
        elif y != None and y.key == k:  self.__hashArray2[pos2] = None
        else:   return False   # the key wasnt found in either possible position
        self.__numRecords -= 1 
        return True


# ----------------------------------------------------- #

def test():
    size = 1000
    missing = 0
    found = 0 
    
    # create a hash table with an initially small number of bukets
    c = HashTab(100)
    
    # Now insert size key/data pairs, where the key is a string consisting
    # of the concatenation of "foobarbaz" and i, and the data is i
    inserted = 0
    for i in range(size): 
        if c.insert(str(i)+"foobarbaz", i):
            inserted += 1
    print("There were", inserted, "nodes successfully inserted")
        
        
    # Make sure that all key data pairs that we inserted can be found in the
    # hash table. This ensures that resizing the number of buckets didn't 
    # cause some key/data pairs to be lost.
    for i in range(size):
        ans = c.find(str(i)+"foobarbaz")
        if ans == None or ans != i:
            print(i, "Couldn't find key", str(i)+"foobarbaz")
            missing += 1
            
    print("There were", missing, "records missing from Cuckoo")
    
    # Makes sure that all key data pairs were successfully deleted 
    for i in range(size): 
        c.delete(str(i)+"foobarbaz")
        
    for i in range(size): 
        ans = c.find(str(i)+"foobarbaz") 
        if ans != None or ans == i: 
            print(i, "Couldn't delete key", str(i)+"foobarbaz") 
            found += 1
    print("There were", found, "records not deleted from Cuckoo") 

def __main():
    test()
    
if __name__ == '__main__':
    __main()       

