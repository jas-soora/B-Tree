#Jastejpal Soora

#Node class
class Node:
    def __init__(self, leaf = False):
        self.keys = [None]*3                #array containing maximum of 3 keys
        self.children = [None]*4            #array containing maximum of 4 child pointers
        self.leaf = leaf                    #tracks if node is the same as leaf
        self.num = 0                        #number of keys

    #Function that returns index of key in b tree
    def findKey(self, key):
        i = 0
        while i < self.num and self.keys[i] < key:
            i += 1

        return i
    
    #Function to remove a key from tree
    def remove(self, key):
        i = self.findKey(key)

        if i < self.num and self.keys[i] == key:
            if self.leaf:
                self.removeFromLeaf(i)
            else:
                self.removeFromNonLeaf(i)

        else:
            if self.leaf:            
                print("Key not in tree")
                return

            #checks if subtree contains key to be removed
            if i == self.num:
                containsKey = True
            else:
                containsKey = False

            #if child where key is present has less than two keys, child is filled
            if self.children[i].num < 2:
                self.fill(i)

            if containsKey and i > self.num:
                self.children[i-1].remove(key)

            else:
                self.children[i].remove(key)

        return

    #Function to remove a key from a leaf node
    def removeFromLeaf(self, i):
        #loop shifts all keys after index one position back
        for i in range(i+1, self.num, 1):
            self.keys[i-1] = self.keys[i]

        self.num -= 1
        return

    #Function to remove a key from a non leaf node
    def removeFromNonLeaf(self, i):
        key = self.keys[i]                      #get key at index i

        if self.children[i].num >= 2:
            pre = self.getPre(i)
            self.keys[i] = pre
            self.children[i].remove[pre]

        elif self.children[i+1].num >= 2:
            suc = self.getSuc(i)
            self.keys[i] = suc
            self.children[i+1].remove(suc)

        #if both children have less than 2 keys, then merge and remove
        else:
            self.merge(i)
            self.children[i].remove(key)

        return

    #Function to get predecessor of key at index i
    def getPre(self, i):
        current = self.children[i]

        while not current.leaf:
            current = current.children[current.num]

        return current.keys[current.num-1]              #return the last key in leaf

    #Function to get successor of key at index i
    def getSuc(self, i):
        current = self.children[i+1]

        while not current.leaf:
            current = current.children[0]

        return current.keys[0]                          #return the successor

    #Function to fill child at index with less than 1 key
    def fill(self, i):
        #borrow key from left sibling
        if i != 0 and self.children[i-1].num >= 2:
            self.takeFromLeft(i)

        #borrow key from right sibling
        elif i != self.num and self.children[i+1].num >= 2:
            self.takeFromRight(i)

        #merge if left or right child does not have enough keys
        else:
            if i != self.num:
                self.merge(i)
            else:
                self.merge(i-1)

        return

    #Function to borrow key from left sibling
    def takeFromLeft(self, i):
        for n in range(self.children[i].num-1, -1, -1):
            self.children[i].keys[n+1] = self.children[i].keys[n]

        if not self.children[i].leaf:
            for j in range(self.children[i].num, -1, -1):
                self.children[i].children[j+1] = self.children[i].children[j]

        self.children[i].keys[0] = self.keys[i-1]

        if not self.children[i].leaf:
            self.children[i].children[0] = self.children[i-1].children[self.children[i-1].num]

        self.keys[i-1] = self.children[i-1].keys[self.children[i-1].num-1]

        self.children[i].num += 1
        self.children[i-1].num -= 1

        return
    
    #Function to borrow key from right sibling
    def takeFromRight(self, i):
        self.children[i].keys[self.children[i].num] = self.keys[i]

        if not self.children[i].leaf:
            self.children[i].children[self.children[i].num+1] = self.children[i+1].children[0]

        self.keys[i] = self.children[i+1].keys[0]

        for n in range(1,self.children[i+1].num, 1):
            self.children[i+1].keys[n-1] = self.children[i+1].keys[n]

        if not self.children[i+1].leaf:
            for j in range(1, self.children[i+1].num+1, 1):
                self.children[i+1].children[j-1] = self.children[i+1].children[j]

        self.children[i].num += 1
        self.children[i+1].num -= 1
        
        return

    #Function to merge child with right sibling
    def merge(self, i):
        self.children[i].keys[1] = self.keys[i]
        
        #keys are copied from right sibling into current child
        for n in range(self.children[i+1].num):
            self.children[i].keys[n+2] = self.children[i+1].keys[n]

        #children are copied from right sibling into grandchildren
        if not self.children[i].leaf:
            for j in range(self.children[i+1].num +1):
                self.children[i].children[j+2] = self.children[i+1].children[j]
                
        #keys that come after index are shifted one position back
        for k in range(i+1, self.num + 1, 1):
            self.keys[k-1] = self.keys[k]

        #child pointers are moved one position back
        for m in range(i+2, self.num + 1, 1):
            self.children[m-1] = self.children[m]
            
        #key counts are updated
        self.children[i].num += self.children[i+1].num + 1
        self.num -= 1
        
        #right sibling is deleted
        del self.children[i+1]
        
        return

    #Function to insert a key into current node when it has vacancy
    def insertVacant(self, key):
        i = self.num-1 

        #if it is a leaf node, find location to insert key
        if self.leaf:
            while i >= 0 and self.keys[i] > key:
                self.keys[i+1] = self.keys[i]
                i -= 1

            #key is inserted and count is updated
            self.keys[i+1] = key
            self.num += 1

        else:
            while i >= 0 and self.keys[i] > key:
                i -= 1

            #split child if full
            if self.children[i+1].num == 3:                  
                self.split(i+1, self.children[i+1])             
                
                if self.keys[i+1] < key:
                    i += 1

            #insert key into vacant child
            self.children[i+1].insertVacant(key)

    #Function to split child of a node that is full
    def split(self, i, node):
        z = Node(node.leaf)
        z.num = 1

        for i in range(1):
            z.keys[i] = node.keys[i+2]
        
        if not node.leaf:
            for j in range(2):
                z.children[j] = node.children[j+2]
                
        node.num = 1
        
        #create space for new child
        for k in range(self.num, i, -1):
            self.children[k+1] = self.children[k]
            
        self.children[i+1] = z
        
        for m in range(self.num-1, i-1, -1):
            self.keys[m+1] = self.keys[m]

        self.keys[i] = node.keys[1]
        self.num += 1
    
    #Function to traverse the tree
    def traverse(self):
        for i in range(self.num):
            if self.leaf == False:
                self.children[i].traverse()

            #parent is printed
            print(self.keys[i])         
        i+=1
        
        if self.leaf == False:
            self.children[i].traverse()

#B tree class
class B_Tree:
    def __init__(self): 
        self.root = None
    
    #Function to insert 
    def insert(self, key):
        if self.root is None:               #if tree is empty
            self.root = Node(True)          #create new b tree leaf node
            self.root.keys[0] = key         #insert value into first position
            self.root.num = 1               #key count is updated
            
        else:                                   #if tree is not empty
            if self.root.num == 3:              #if root is full
                new = Node(False)               #create a new node
                new.children[0] = self.root     
                new.split(0, self.root) 

                i = 0
                
                if new.keys[0] < key:
                    i += 1
                    
                new.children[i].insertVacant(key)       #new value is inserted into child
                self.root = new                         #root is set to new node
                
            else:                                       #if root is not full 
                self.root.insertVacant(key)

    #Function to delete
    def delete(self, key):
        self.root.remove(key)

        if self.root.num == 0:
            #temp = self.root
            
            if(self.root.leaf):
                self.root = None
                
            else:
                self.root = self.root.children[0]
                
            #del temp #free the previous root
            
        return

    #Function to get number of nodes in tree
    def size(self, node):
        count = 1

        #base case
        if node is None: 
            return 0
        
        else:
            for i in range(len(node.children)):
                if node.children[i] is not None:
                    count += self.size(node.children[i])

            #count is returned
            return count
        
    #Function to print tree
    def printTree(self):
        if self.root is not None:
            self.root.traverse()
        print("The size of the b tree is", self.size(self.root), "nodes")


#Driver code
tree = B_Tree()
tree.insert(25)
tree.insert(30)
tree.insert(13)
tree.insert(50)
tree.insert(11)
tree.insert(12)
tree.insert(7)
tree.insert(2048)

print("Tree after populating:")
tree.printTree()
print("___________________________________________" + "\n")
print("Tree after deleting 50")
tree.delete(50)
tree.printTree()


    


                
                
