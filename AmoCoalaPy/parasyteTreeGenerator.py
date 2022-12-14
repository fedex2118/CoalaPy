from ete3 import PhyloTree

import numpy as np
import math

#### ParasyteTreeGenerator Constants ####
C = "C"
D = "D"
H = "H"
L = "L"
EVENT_VECTOR = [C, D, H, L] # 4 events # rinomino a stringhe
PROB_VECTOR = [0.50, 0.40, 0.0, 0.10] # 4 probabilities, HostSwitch 0 not implemented yet!
 
ZERO_ONE_LIST = [0, 1] # 0, 1
PROB_ZERO_ONE = [0.5, 0.5] # chance to choose zero and chance to choose one

def parasyteTreeGenerator(hostTree: PhyloTree, pTree: PhyloTree, probVector: list):
    pC: float = probVector[0]  # position 1: pC
    pD: float = probVector[1]  # position 2: pD
    pH: float = probVector[2]  # position 3: pH
    pL: float = probVector[3]  # position 4: pL
    summ = math.fsum(probVector)
    print(summ)
    assert (summ == 1), "The sum of the probabilities must be 1!"
    
    # parasyteTree size
    print("Original Parasyte Tree:")
    print(pTree)
    originalSize = 0
    # let's calculate the size in nodes of the original parasyteTree...
    for node in pTree.traverse(strategy="preorder"):
        originalSize += 1
    
    doubledSize = originalSize * 2 # ...then double the originalSize
    
    # let's generate a new parasyteTree
    parasyteTree = PhyloTree() # node v
    # 1 of 4 events can occur: C, D, H, L
    print("doubledOriginalSize: " + (str)(doubledSize))
    print("Parasyte Tree")
    pSize = 0
    pSize = recursiveParasyte(hostTree, parasyteTree, False, False, pSize, doubledSize,
                              False) # starting from rootHost and rootNewParasyte
    
    print(parasyteTree)

def recursiveParasyte(hostTree: PhyloTree, parasyteTree: PhyloTree, dEvent: bool, isLeft: bool,
                      pSize: int, doubledPSize: int, lossFailed: bool):
    pSize += 1
    print("size = " + (str)(pSize))
    
    # base cases:
    if(pSize > doubledPSize): # if it's major than double the size of PTree we just exit
        print("NewParasyteTree is double the size of the original ParasyteTree")
        return pSize
    if(hostTree.is_leaf()): # if we find a leaf:
        parasyteTree.add_feature("name", hostTree.name) # we name it as it is named in the hostTree
        print("Leaf Found")
        return pSize # let's exit from the recursive loop
    
    event: str
    
    if(lossFailed): # if loss failed cause of duplication event followed by loss (
        # both duplicated child had loss)
        pLoss = PROB_VECTOR[3] / 2.0 # TODO change 2.0 to 3.0 if hostSwitch is implemented!
        probVectorNoLoss = [PROB_VECTOR[0] + pLoss, PROB_VECTOR[1] + pLoss, 0.0, 0.0] 
        # Loss must be 0.0, HostSwitch not yet implemented!
        summ = math.fsum(probVectorNoLoss)
        assert (summ == 1), "The sum of the probabilities of VectorWithoutLoss must be 1!"
        event = np.random.choice(EVENT_VECTOR, p=probVectorNoLoss) 
        # we calculated prob of another event (C, D, H) that is not Loss!
    else:
        event = np.random.choice(EVENT_VECTOR, p=PROB_VECTOR)
    
    print("event" + (str)(event))
    
    assert (event != H), "Host Switch not implemented yet! Put 0.0 on the PROB_VECTOR[2]"
    
    #if (cospeciation):
    if(event == C):
        parasyteTree.add_child() # left child   v1
        parasyteTree.add_child() # right child  v2
        
        pSize = recursiveParasyte(hostTree.get_children()[0], parasyteTree.get_children()[0], False, 
                      True, pSize, doubledPSize, False) # hl: v1
        pSize = recursiveParasyte(hostTree.get_children()[1], parasyteTree.get_children()[1], False,
                      False, pSize, doubledPSize, False) # hr: v2
    #end cospeciation
    
    #if (duplication):
    elif(event == D):
        parasyteTree.add_child() # left child   v1
        parasyteTree.add_child() # right child  v2
        
        leftDirection: int = -1
        rightDirection: int = -1
        
        leftNode = np.random.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0 or 1
        rightNode = np.random.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE)
        
        # 0 means is mapped on this node, 1 means it goes down in one of the children.
        
        if (leftNode == 0): # left node is mapped to current host node.
            pSize = recursiveParasyte(hostTree, parasyteTree.get_children()[0], True,
                          True, pSize, doubledPSize, False) # h: v1
        
        if (leftNode == 1): # left node is going down in one of the host node children
            leftDirection = np.random.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0 or 1
            # 0 means go down on left node, 1 means go down right node
            if (leftDirection == 0): # left parasyte node is mapped to host node left child
                pSize = recursiveParasyte(hostTree.get_children()[0], parasyteTree.get_children()[0],
                            True, True, pSize, doubledPSize, False) # h[0]: v1
            else: # left parasyte node is mapped to host node right child
                pSize = recursiveParasyte(hostTree.get_children()[1], parasyteTree.get_children()[0],
                            True, True, pSize, doubledPSize, False) # h[1]: v1
        
        if (rightNode == 0): # right node is mapped to this host node
            pSize = recursiveParasyte(hostTree, parasyteTree.get_children()[1], True,
                          False, pSize, doubledPSize, False) # h: v2
        
        if (rightNode == 1): # right node is mapped to one of the host node children, but with
            # some checks on which one to choose:
            # if left node is already going down...
            if (leftDirection != -1): # we choose the mapping with left's direction
                if (leftDirection == 0): # :host left child
                    pSize = recursiveParasyte(hostTree.get_children()[0], 
                        parasyteTree.get_children()[1], True, False, pSize, 
                        doubledPSize, False) # h[0]: v2
                else: # :host right child
                    pSize = recursiveParasyte(hostTree.get_children()[1], 
                        parasyteTree.get_children()[1], True, False, pSize, 
                        doubledPSize, False) # h[1]: v2
            else: # otherwise we choose the mapping with right's own direction
                rightDirection = np.random.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0 or 1
                # 0 means go down on left node, 1 means go down right node
                if (rightDirection == 0): # right parasyte node is mapped to host node left child
                    pSize = recursiveParasyte(hostTree.get_children()[0], 
                        parasyteTree.get_children()[1], True, False, pSize, 
                        doubledPSize, False) # h[0]: v2
                else: # right parasyte node is mapped to host node right child
                    pSize = recursiveParasyte(hostTree.get_children()[1], 
                        parasyteTree.get_children()[1], True, False, pSize, 
                        doubledPSize, False) # h[1]: v2
    #end duplication
    
    #if (hostSwitch):
    # Work in Progress...
    
    #end hostSwitch
    
    #if (loss):
    else:
        if(dEvent): # if this node is born from duplication event:
            #print("duplicationLoss")
            if(isLeft): # if we are on left node
                parasyteTree.add_feature("name", "lossEvent")
            else: # we are on right node
                if(parasyteTree.get_sisters()[0].name == "lossEvent"): 
                    # if there was already a loss on left node
                    print("there was already a loss on left node")
                    pSize = recursiveParasyte(hostTree, parasyteTree, False, False, pSize-1,
                                              doubledPSize, True)
                    # then we recalculate recursively probability of another event (C, D, H).
                    return pSize
                # "otherwise there was a loss on right node"
        # this code below is always read if there wasn't a duplication event on the node before
        node = np.random.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0, 50% chance 1
        if(node == 0): # left node has been chosen
            pSize = recursiveParasyte(hostTree.get_children()[0], parasyteTree, False,
                            True, pSize-1, doubledPSize, False) # hl: v
        else: # right node chosen
            pSize = recursiveParasyte(hostTree.get_children()[1], parasyteTree, False,
                            False, pSize-1, doubledPSize, False) # hr: v
    #end loss
    
    return pSize



#start = time.time()     
#nexusReader(file2) # wrong format type for testing purposes


#print(dictionary)
#print(treeList[0])
#print(treeList[1])
#end = time.time()

#nReaderTime = (end - start)

# time with first for loop  (for line in f)                 4.9114227294921875e-05
# time with second for loop (for line in f.readlines())     7.915496826171875e-05

# time with first for loop  (for line in f)                 0.0037279129028320312
# time with second for loop (for line in f.readlines())     0.0050013065338134766