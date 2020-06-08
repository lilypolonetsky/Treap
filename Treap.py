import random, math

"""
Node

Attributes
------------
key : int or str
    holds the node's key value
priority: int
    assigned by Treap class, used to mantain heap condition
left: Node
    points to its left child, None if there is no left child
right: Node
    points to its right child, None if there is no right child
"""

class Node(object):
    def __init__(self, k, p):
        self.key = k
        self.priority = p
        self.left = None
        self.right = None
        
    def __str__(self): return str(self.key) + ", " + str(self.priority)
        
        
# max treap size is 500,000 nodes
    
"""
Treap

Attributes
--------------
root: Node
    stores the node which has no parents
    in a true implementation the root should be private
    not private here so that testing can be rigorous
    
__priorityList: list
    stores a shuffled list of numbers from 0-499,999
    once a priority number is used, it is removed from the list
    ensures that each priority assigned is unique

"""

class Treap(object):
    def __init__(self):
        self.root = None
        # keeps unused priority numbers
        self.__priorityList = self.__randomNum()
    
    # generates a list of random numbers
    # used for priority numbers
    # only called once for creational purposes
    # returns: list
    def __randomNum(self):
        choices = list(range(500000))
        random.shuffle(choices)
        return choices
    
    # takes a number from the priority list
    # returns: int
    def __getPriority(self):
        if self.__priorityList[0]:
            return self.__priorityList.pop()
        else:
            raise Exception("Max nodes reached")
    
    # called by insert
    # parameters:
    #   k: key to be inserted
    # returns: Node
    def __createNode(self, k):
        priority = self.__getPriority()
        return Node(k, priority)
    
    # parameters:
    #   k: key to be inserted
    def insert(self, k):
        if not self.root: self.root = self.__createNode(k)
        else: self.root = self.__insert(k, self.root)
        
    # recursive method for insertion
    # parameters: 
    #   k: key to be inserted
    #   parent: node under consideration
    # returns: Node
    def __insert(self, k, parent):
        if not parent: return self.__createNode(k)
        
        #left tree
        if k <= parent.key:
            parent.left = self.__insert(k, parent.left)
            if parent.left.priority > parent.priority:
                parent = self.rotateRight(parent)
        #right tree   
        else:
            parent.right = self.__insert(k, parent.right)
            if parent.right.priority > parent.priority:
                parent = self.rotateLeft(parent)
                
        return parent
    
    # parameters:
    #   parent: Node to be rotated
    # returns: Node
    def rotateRight(self, parent):
        child = parent.left
        parent.left = child.right
        child.right = parent
        return child
    
    # parameters:
    #   parent: Node to be rotated
    # returns: Node    
    def rotateLeft(self, parent):
        child = parent.right
        parent.right = child.left
        child.left = parent       
        return child
    
    # searches for node with the given key
    # returns (parent, node, rel) if found, (None, None, None) if not found
    # rel relates if node is the parent's right or left child
    def __findR(self, key, cur = "start", parent = "start", rel = "left"):
        if cur == "start": 
            cur = self.root
            parent = self.root
        
        if not cur: return (None, None, None)
        
        #did we find the key?
        if cur.key == key: return (parent, cur, rel)
        #didn't find key, go right
        elif key > cur.key: return self.__findR(key, cur.right, cur, "right")
        #didn't find key, go left
        else: return self.__findR(key, cur.left, cur, "left")
        
    def find(self, key):
        parent, cur, rel = self.__findR(key)
        
        if parent != None: return True
        else: return False
    
    # returns True if the node is a leaf
    # returns False if node is not a leaf
    def __isLeaf(self, node):
        if node.right is None and node.left is None: return True
        else: return False
    
    # removes the node with the supplied key
    # returns True if node is successfully deleted
    # returns False if node is not successfully deleted
    def delete(self, key):
        parent, node, rel = self.__findR(key)
        
        #if the node was not found, stop
        if not node: return False
        
        # check if it is a leaf
        # if it's not a leaf, change the priority to -infinity
        if not self.__isLeaf(node): node.priority = -math.inf
        
        # so long as it is not a leaf,
        # go through the process of making it a leaf
        while not self.__isLeaf(node):
            # do both children exist?
            if node.left and node.right:
                # find which child has a higher priority
                # then do the proper rotation
                if node.left.priority > node.right.priority: successor = self.rotateRight(node)
                else: successor = self.rotateLeft(node)
           
            # only right child exists
            elif node.right: 
                successor = self.rotateLeft(node)
            
            #only a left child exists
            else:
                successor = self.rotateRight(node)
            
            # complete the rotation by attaching 
            # parent to successor (the node taking the place of orig node)
            if parent is node: 
                self.root = successor
            elif rel == "left": 
                parent.left = successor
            else:
                parent.right = successor
                
            # the parent of node is now successor
            parent = successor
            #update rel to reflect this
            if parent.right is node: rel = "right"
            else: rel = "left"
            
        # at this point the node is definitely a leaf 
        # snip the node
        if rel == "left": parent.left = None
        else: parent.right = None
        
        return True
                
    
    def display(self):
        self.__display(self.root, 0)
        print()

    def __display(self, t, indent):
        if t:
            if indent: print()
            print(" " * indent, end="")
            print("( " + str(t.key) + " " + str(t.height) + " " + \
                  str(t.heightDiff()) + " ", end="")
            self.__display(t.left, indent+2)
            print(" ", end="")
            self.__display(t.right, indent+2)
            print(" )", end="") 
            
    def __str__(self): return '(' + self.stringify(self.root) + ')'

    def stringify(self, n):
        if not n: return ''
        return str(n) + \
               '(' + self.stringify(n.left)  + ')' + \
               '(' + self.stringify(n.right) + ')'  

def getParentChildPriority(t, parent = "start"):
    if parent is None: return []
    
    if parent == "start": parent = t.root
            
    arr = []
        
    if parent.left: arr.append((parent.priority, parent.left.priority))
    if parent.right: arr.append((parent.priority, parent.right.priority))
        
    return arr + getParentChildPriority(t, parent.right) + getParentChildPriority(t, parent.left)

def __main():
    t = Treap()
    t.insert(20)
    t.insert(10)
    t.insert(5)
    t.insert(50)
    t.insert(40)
    t.insert(500)
    t.insert(1)
    print(t)
    
    print()
    print("deleting 50", t.delete(50))
    print()
    print("deleting 20", t.delete(20))
    
    print()
    print(t)
    
    print()
    print("find 50", t.find(50))
    print("find 2", t.find(2))    
    
    print(getParentChildPriority(t))

    
if __name__ == '__main__': 
    __main()       