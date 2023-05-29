from ete3 import PhyloTree
from numpy import random as rand
from math import fsum

import string
import os

#### ParasyteTreeGenerator Constants ####
C = "C"
D = "D"
H = "H"
L = "L"
EVENT_VECTOR = [C, D, H, L] # 4 events # strings
 
ZERO_ONE_LIST = [0, 1] # 0, 1
PROB_ZERO_ONE = [0.5, 0.5] # chance to choose zero and chance to choose one

GENERATED_PARASYTE_TREES_FOLDER = "GenParasytes" # the path folder where parasyte trees are put into, this folder should not be moved!

def parasyteTreeGenerator(host_tree: PhyloTree, p_tree: PhyloTree, prob_vector: list, N: int,
                          p_host_associations: dict):
    # pC: float = prob_vector[0]  # position 1: pC
    # pD: float = prob_vector[1]  # position 2: pD
    # pH: float = prob_vector[2]  # position 3: pH
    # pL: float = prob_vector[3]  # position 4: pL
    summ = fsum(prob_vector)
    #print(summ)
    assert (summ == 1), "The sum of the probabilities must be 1!"
    
    assert (N <= 300), "Number of trees to generate must be <= than 300!"
    
    # parasyte_tree size
    print("Original Parasyte Tree:")
    print(p_tree)
    original_size = 0
    
    # let's create a copy of the original parasyte_tree...
    # start with a new root node:  
    original_parasyte_tree_copy = PhyloTree() # root node
    
    p_host_associations_copy = p_host_associations.copy()
    
    # then let's traverse the original parasyte tree:
    original_size = create_parasyte_copy(p_tree, original_parasyte_tree_copy,
                                         p_host_associations_copy, original_size)
    print("SIZE")
    print(original_size)
    
    #print("Copy of the original parasyte tree with host associated labelled leaves:")
    #print(original_parasyte_tree_copy)
        
    
    doubled_size = original_size * 2 # ...then double the original_size
    
    parasyte_trees_gen = [] # this list will contain all useful parasyte trees generated
    
    print("doubled_original_size: " + (str)(doubled_size))
    
    for x in range(N):
        # let's generate a new parasyteTree
        parasyte_tree = PhyloTree() # node v
        # 1 of 4 events can occur: C, D, H, L
        p_size = 0
        p_size = recursive_parasyte(host_tree, parasyte_tree, False, False, p_size, doubled_size,
                                False, prob_vector) # starting from rootHost and rootNewParasyte
        
        # check if pSize is minor or equal than double the size of the original Parasyte tree:
        if p_size <= doubled_size: # if it's true then we store the tree
            parasyte_newick: str = parasyte_tree.write(format=9) + '\n'
            parasyte_trees_gen.append(parasyte_newick)
        # else: the tree is not used
        #print(parasyte_tree) # remove comment to see generated trees printed on console
    
    number_of_useful_trees = len(parasyte_trees_gen)
    if N == 1:
        print("The number of trees to generate was equal to 1, put a higher number to start a proper generation.")
    
    if N > 1: # if N > 1 let's make a file that contains the results of the generation
        generation_results(number_of_useful_trees, parasyte_trees_gen, original_parasyte_tree_copy,
                           prob_vector, N)

def recursive_parasyte(host_tree: PhyloTree, parasyte_tree: PhyloTree, d_event: bool, is_left: bool,
                      p_size: int, doubled_p_size: int, loss_failed: bool, prob_vector: list):
    p_size += 1
    #print("size = " + (str)(p_size))
    
    # base cases:
    if(p_size > doubled_p_size): # if it's major than double the size of p_tree we just exit
        #print("NewParasyteTree is bigger than double the size of the original ParasyteTree")
        return p_size
    if(host_tree.is_leaf()): # if we find a leaf:
        parasyte_tree.add_feature("name", host_tree.name) # we name it as it is named in the hostTree
        #print("Leaf Found")
        return p_size # let's exit from the recursive loop
    
    event: str
    
    if loss_failed: # if loss failed cause of duplication event followed by loss (
        # both duplicated child had loss)
        p_loss = prob_vector[3] / 2.0 # TODO change 2.0 to 3.0 if hostSwitch is implemented!
        prob_vector_no_loss = [prob_vector[0] + p_loss, prob_vector[1] + p_loss, 0.0, 0.0] 
        # Loss must be 0.0, HostSwitch not yet implemented!
        summ = fsum(prob_vector_no_loss)
        assert (summ == 1), "The sum of the probabilities of prob_vector_no_loss after a failed loss event must be 1!"
        event = rand.choice(EVENT_VECTOR, p=prob_vector_no_loss) 
        # we calculated prob of another event (C, D, H) that is not Loss!
    else:
        event = rand.choice(EVENT_VECTOR, p=prob_vector)
    
    #print("event" + (str)(event))
    
    assert (event != H), "Host Switch not implemented yet! Put 0.0 on input pH"
    
    #if (cospeciation):
    if(event == C):
        parasyte_tree.add_child() # left child   v1
        parasyte_tree.add_child() # right child  v2
        
        p_size = recursive_parasyte(host_tree.get_children()[0], parasyte_tree.get_children()[0], False, 
                      True, p_size, doubled_p_size, False, prob_vector) # hl: v1
        p_size = recursive_parasyte(host_tree.get_children()[1], parasyte_tree.get_children()[1], False,
                      False, p_size, doubled_p_size, False, prob_vector) # hr: v2
    #end cospeciation
    
    #if (duplication):
    elif(event == D):
        parasyte_tree.add_child() # left child   v1
        parasyte_tree.add_child() # right child  v2
        
        left_direction: int = -1
        right_direction: int = -1
        
        left_node = rand.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0 or 1
        right_node = rand.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE)
        
        # 0 means is mapped on this node, 1 means it goes down in one of the children.
        
        if (left_node == 0): # left node is mapped to current host node.
            p_size = recursive_parasyte(host_tree, parasyte_tree.get_children()[0], True,
                          True, p_size, doubled_p_size, False, prob_vector) # h: v1
        
        if (left_node == 1): # left node is going down in one of the host node children
            left_direction = rand.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0 or 1
            # 0 means go down on left node, 1 means go down right node
            if (left_direction == 0): # left parasyte node is mapped to host node left child
                p_size = recursive_parasyte(host_tree.get_children()[0], parasyte_tree.get_children()[0],
                            True, True, p_size, doubled_p_size, False, prob_vector) # h[0]: v1
            else: # left parasyte node is mapped to host node right child
                p_size = recursive_parasyte(host_tree.get_children()[1], parasyte_tree.get_children()[0],
                            True, True, p_size, doubled_p_size, False, prob_vector) # h[1]: v1
        
        if (right_node == 0): # right node is mapped to this host node
            p_size = recursive_parasyte(host_tree, parasyte_tree.get_children()[1], True,
                          False, p_size, doubled_p_size, False, prob_vector) # h: v2
        
        if (right_node == 1): # right node is mapped to one of the host node children, but with
            # some checks on which one to choose:
            # if left node is already going down...
            if (left_direction != -1): # we choose the mapping with left's direction
                if (left_direction == 0): # :host left child
                    p_size = recursive_parasyte(host_tree.get_children()[0], 
                        parasyte_tree.get_children()[1], True, False, p_size, 
                        doubled_p_size, False, prob_vector) # h[0]: v2
                else: # :host right child
                    p_size = recursive_parasyte(host_tree.get_children()[1], 
                        parasyte_tree.get_children()[1], True, False, p_size, 
                        doubled_p_size, False, prob_vector) # h[1]: v2
            else: # otherwise we choose the mapping with right's own direction
                right_direction = rand.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0 or 1
                # 0 means go down on left node, 1 means go down right node
                if (right_direction == 0): # right parasyte node is mapped to host node left child
                    p_size = recursive_parasyte(host_tree.get_children()[0], 
                        parasyte_tree.get_children()[1], True, False, p_size, 
                        doubled_p_size, False, prob_vector) # h[0]: v2
                else: # right parasyte node is mapped to host node right child
                    p_size = recursive_parasyte(host_tree.get_children()[1], 
                        parasyte_tree.get_children()[1], True, False, p_size, 
                        doubled_p_size, False, prob_vector) # h[1]: v2
    #end duplication
    
    #if (host_switch):
    # Work in Progress...
    
    #end host_switch
    
    #if (loss):
    else:
        if d_event: # if this node is born from duplication event:
            #print("duplicationLoss")
            if is_left: # if we are on left node
                parasyte_tree.add_feature("name", "lossEvent")
            else: # we are on right node
                if(parasyte_tree.get_sisters()[0].name == "lossEvent"): 
                    # if there was already a loss on left node
                    #print("there was already a loss on left node")
                    p_size = recursive_parasyte(host_tree, parasyte_tree, False, False, p_size-1,
                                              doubled_p_size, True, prob_vector)
                    # then we recalculate recursively probability of another event (C, D, H).
                    return p_size
                # "otherwise there was a loss on right node"
        # this code below is always read if there wasn't a duplication event on the node before
        node = rand.choice(ZERO_ONE_LIST, p=PROB_ZERO_ONE) # 50% chance 0, 50% chance 1
        if(node == 0): # left node has been chosen
        # is_left variable doesn't matter on this event since it is only useful
        # whenever two children are created or when a duplication event occurs
            p_size = recursive_parasyte(host_tree.get_children()[0], parasyte_tree, False,
                            False, p_size-1, doubled_p_size, False, prob_vector) # hl: v
        else: # right node chosen
            p_size = recursive_parasyte(host_tree.get_children()[1], parasyte_tree, False,
                            False, p_size-1, doubled_p_size, False, prob_vector) # hr: v
    #end loss
    
    return p_size

def create_parasyte_copy(original_parasyte_tree: PhyloTree, parasyte_tree_copy: PhyloTree, 
                         host_p_associations: dict, p_size: int):
    # store the size of the original parasyte tree
    p_size += 1
     
    if original_parasyte_tree.is_leaf(): # if current node is leaf...
        end_loop = False
        for key, v in host_p_associations.items(): # let's loop on the associations and find the right one
            for i in v:
                if i == original_parasyte_tree.name: # if we find it, we name the copy leaf as the name...
                    parasyte_tree_copy.add_feature("name", key) # ...of the host associated leaf
                    v.remove(i) # for future loops efficiency: lists shrinks
                    end_loop = True
                    break
            if end_loop: # for efficiency: when key is found loop ends
                if len(v) == 0: # for future loops efficiency: dictionary shrinks
                    host_p_associations.pop(key)
                break
        return p_size
    
    # else: add two children to the parasyte copy since is a binary tree
    parasyte_tree_copy.add_child()
    parasyte_tree_copy.add_child()
     
    # recursive pass following pre-order
    p_size = create_parasyte_copy(original_parasyte_tree.get_children()[0], 
                                   parasyte_tree_copy.get_children()[0], host_p_associations, p_size)
    p_size = create_parasyte_copy(original_parasyte_tree.get_children()[1], 
                                   parasyte_tree_copy.get_children()[1], host_p_associations, p_size)
     
    return p_size


def generation_results(number_of_useful_trees: int, parasyte_trees_gen: list, 
                       original_parasyte_tree_copy: PhyloTree, prob_vector: list, N: int):
    if number_of_useful_trees < 1: # Generation failed to generate "good" trees:
            print("Generation resulted in 0 'good enough' parasyte trees: the size of those trees resulted to be bigger than double the size of the original tree!\nNo real comparison could be made for such trees.\nTry different event probabilities: the higher duplication event probability is, the higher the chance to get bad results.")
    else: # Generation ends with positive results:
        print("Generation resulted in: " + (str)(number_of_useful_trees) + " parasyte trees generated!")
        print("The results are stored under " + GENERATED_PARASYTE_TREES_FOLDER + " folder")
        
        output_path = GENERATED_PARASYTE_TREES_FOLDER + "/gen_results_"
        filename = generate_random_filename(8, output_path)
        generation_results_file = output_path + filename
        first_line = str(prob_vector) + '\n'
        
        print("The file that stores the results is called: " + generation_results_file)
        
        try:
            with open(generation_results_file, 'x') as f: # generation_results file
                f.write(first_line)
                f.write("N: " + str(N) + '\n')
                f.writelines(parasyte_trees_gen) # add all the newick format parasyte trees
                f.write("Original Parasyte Tree:\n")
                f.write(original_parasyte_tree_copy.write(format=9)) # add copy of the original parasyte tree with host associated labelled leaves.
                
        except FileNotFoundError:
            print(GENERATED_PARASYTE_TREES_FOLDER + " not found! There should be a folder called: " + GENERATED_PARASYTE_TREES_FOLDER + ". If it's not there try creating a new one with that name.")
        finally:
            f.close()

def generate_random_filename(lenght: int, output_path: str):
    letters_and_digits = string.ascii_lowercase + string.digits
    filename = ''.join(rand.choice(list(letters_and_digits), lenght)) + ".txt"
    
    if os.path.exists(output_path + filename):
        return generate_random_filename(lenght, output_path)
    
    return filename
     