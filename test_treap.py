from Treap import Treap
import random, pytest

def createRandomTreap(num):
    t = Treap()
    for i in range(num):
        n = random.randint(0,10000)
        t.insert(n)
    return t

def getParentChildPriority(t, parent = "start"):
    if parent is None: return []
    
    if parent == "start": parent = t.root
            
    arr = []
        
    if parent.left: arr.append((parent.priority, parent.left.priority))
    if parent.right: arr.append((parent.priority, parent.right.priority))
        
    return arr + getParentChildPriority(t, parent.right) + getParentChildPriority(t, parent.left)

# small number of nodes
# is each child's priority smaller than its parent?
def test_smallTreapPriorities():
    t = createRandomTreap(10)
    
    priorityL = getParentChildPriority(t)
    
    for parent,child in priorityL:
        assert parent >= child

# large number of nodes
# is each child's priority smaller than its parent?
def test_largeTreapPriorities():
    t = createRandomTreap(10000)
    
    priorityL = getParentChildPriority(t)
    
    for parent,child in priorityL:
        assert parent >= child

# small number of nodes
# does the treap satisfy the binary tree condition?
def test_smallTreapBST():
    t = createRandomTreap(10)
    tList = []
    
    tList.append(t.root)
    while len(tList) > 0:
        cur = tList.pop()
        if cur.right: 
            tList.append(cur.right)
            assert cur.right.key >= cur.key
        if cur.left: 
            tList.append(cur.left)
            assert cur.left.key <= cur.key
        

# small number of nodes
# does the treap satisfy the binary search condition?
def test_largeTreapBST():
    t = createRandomTreap(10000)
    tList = []
    
    tList.append(t.root)
    while len(tList) > 0:
        cur = tList.pop()
        if cur.right: 
            tList.append(cur.right)
            assert cur.right.key >= cur.key
        if cur.left: 
            tList.append(cur.left)
            assert cur.left.key <= cur.key
        

# small number of nodes
# check that find works
# numbers may or may not be in treap
def test_smallTreapFind():
    t = Treap()
    keys = []
    
    for i in range(10):
        keys.append(i)
        t.insert(i)
    
    for i in range(100):
        if i in keys:
            assert t.find(i) == True
        else:
            assert t.find(i) == False

# small number of nodes
# check that find works
# numbers may or may not be in treap
def test_largeTreapFind():
    t = Treap()
    keys = set()
    
    for i in range(10000):
        keys.add(i)
        t.insert(i)
    
    for i in range(11000):
        if i in keys:
            assert t.find(i) == True
        else:
            assert t.find(i) == False

# small number of nodes
# test the delete function
def test_smallTreapDelete():
    t = Treap()
    keys = []
    
    for i in range(10):
        keys.append(i)
        t.insert(i)
    
    for i in range(20):
        if i in keys: assert t.delete(i) == True
        else: assert t.delete(i) == False
        
    #check that nodes that were deleted
    #cannot be found
    for key in keys:
        assert t.find(i) == False

# small number of nodes
# test the delete function
def test_largeTreapDelete():
    t = Treap()
    keys = set()
    
    for i in range(10000):
        keys.add(i)
        t.insert(i)
    
    for i in range(11000):
        if i in keys: assert t.delete(i) == True
        else: assert t.delete(i) == False
        
    #check that nodes that were deleted
    #cannot be found
    for key in keys:
        assert t.find(i) == False
        
# check that each node has a unique priority
def test_uniquePriorities():
    for i in range(5):
        t = createRandomTreap(3000)
        priorityL = getParentChildPriority(t)
        priorities = set()
        
        for parent,child in priorityL:
            if child not in priorities: 
                assert True
                priorities.add(child)
            else: assert False

def test_findEmptyTreap():
    for i in range(10):
        t = Treap()
        n = random.randint(0,100)
        
        assert t.find(n) == False
    
def test_deleteEmptyTreap():
    for i in range(10):
        t = Treap()
        n = random.randint(0,100)
        
        assert t.delete(n) == False    

def test_findOneNode():
    for i in range(10):
        t = Treap()
        n = random.randint(0,100)
        t.insert(n)
        
        assert t.find(n) == True
        assert t.find(n+1) == False
        
def test_tortureTest():
    keys = []
    t = Treap()
    
    # pre-populate treap
    for i in range(100):
        n = random.randint(0, 500)
        keys.append(n)
        t.insert(n)
    
    for i in range(500):
        choice = random.randint(1,3)
        
        # insertion
        if choice == 1:
            n = random.randint(0, 1000)
            keys.append(n)
            t.insert(n)
            
            assert t.find(n) == True
            
        # deletion
        elif choice == 2:
            if keys[0] != None:
                key = keys.pop()
                if key: result = t.delete(key)
            
                assert result == True
                
            else:
                n = random.randint(0, 1000)
                assert t.delete(n) == False
        
        #find
        else:
            n = random.randint(0, 1000)
            if n in keys: 
                assert t.find(n) == True
            else: 
                assert t.find(n) == False
        
        #after each action
        #ensure that bst and heap conditions are being met
        priorityL = getParentChildPriority(t)
        for parent,child in priorityL:
            assert parent >= child   
            
        tList = []    
        tList.append(t.root)
        while len(tList) > 0:
            cur = tList.pop()
            if cur.right: 
                tList.append(cur.right)
                assert cur.right.key >= cur.key
            if cur.left: 
                tList.append(cur.left)
                assert cur.left.key <= cur.key        

pytest.main(["-v", "-s", "test_treap.py"])     