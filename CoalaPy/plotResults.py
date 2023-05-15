from ete3 import PhyloTree
from sys import exit

def open_file(filename):
    
    assert filename.endswith(".txt"), "Wrong format for generated parasytes file: correct format .txt"
    
    generated_parasytes = []
    original_parasyte_tree: PhyloTree = None
    original_parasyte_tree_line = False # Line indicator for original_parasyte_tree
    original_parasyte_tree_str = "Original Parasyte Tree:\n"
    
    with open(filename, 'r') as f:
        
        # the probability used for this generation can be found on first line:
        first_line = f.readline() # read prob_vector: C, D, H, L
        first_line = first_line.replace('\n', "").replace('[', "").replace(']', "").replace(" ", "")
        
        prob_vector = first_line.split(",")
        
        for line in f:
            try:
                if line == original_parasyte_tree_str: # line == "Original Parasyte Tree:\n"
                    original_parasyte_tree_line = True # next line has the actual newick string
                    continue
                if original_parasyte_tree_line: # this line contains the original tree as newick
                    original_parasyte_tree = PhyloTree(line.replace('\n', ""))
                    continue
                # by default we save PhyloTrees into generated_parasytes container
                generated_parasytes += [PhyloTree(line.replace('\n', ""))] # these are the generated trees.
            except Exception as msg: # if something goes wrong:
                print(msg)
                exit(1)
        f.close()
    
    return generated_parasytes, original_parasyte_tree, prob_vector

def get_size(tree: PhyloTree):
    size = 0
    
    for node in tree.traverse():
        size += 1
    
    return size

def get_distance(original_parasyte_tree_size, generated_parasyte_tree_size):
    return abs(generated_parasyte_tree_size - original_parasyte_tree_size)

def execute_plot(path):
    result_tuple = open_file(path)
    
    generated_parasytes = result_tuple[0]
    original_parasyte_tree = result_tuple[1]
    prob_vector = result_tuple[2]
    
    original_p_size = get_size(original_parasyte_tree) # get the size of the original tree
    
    generated_parasytes_sizes = [] # get the size of all the generated trees
    for tree in generated_parasytes:
        generated_parasytes_sizes += [get_size(tree)]
    
    distances = [] # get the distance between original tree and generated
    for g_size in generated_parasytes_sizes:
        distances += [get_distance(original_p_size, g_size)]
    
    C = "C: " + prob_vector[0]
    D = "D: " + prob_vector[1]
    H = "H: " + prob_vector[2]
    L = "L: " + prob_vector[3] 
    
    # print the results
    print("With probability vector: " + C + " " + D + " " + H + " " + L)
    print("Size of the original parasyte tree: " + str(original_p_size))
    print("Distances in size between original parasyte tree and generated ones are: " + str(distances))
                
            


