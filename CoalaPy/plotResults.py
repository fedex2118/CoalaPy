from ete3 import PhyloTree
from sys import exit
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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
        
        second_line = f.readline() # read N: number of trees wanted
        N = second_line.replace('\n', "").split(":")[1]
        
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
    
    return generated_parasytes, original_parasyte_tree, prob_vector, N

def get_leaf_size(tree: PhyloTree):
    size = 0
    
    for node in tree.iter_leaf_names():
        size += 1
    
    return size

def get_distance(original_parasyte_leaf_size, generated_parasyte_leaf_size):
    return original_parasyte_leaf_size - generated_parasyte_leaf_size

def execute_plot(path):
    result_tuple = open_file(path)
    
    generated_parasytes = result_tuple[0]
    original_parasyte_tree = result_tuple[1]
    prob_vector = result_tuple[2]
    N = result_tuple[3]
    
    # get the leaf size of the original tree
    original_p_size = get_leaf_size(original_parasyte_tree)
    
    # get leaf size of all the generated trees
    generated_parasytes_leaf_sizes = [get_leaf_size(tree) for tree in generated_parasytes]
    
    # get the difference (per number of leaves) between original and parasytes
    distances = [get_distance(original_p_size, g_size) for g_size in generated_parasytes_leaf_sizes]
    
    C = "C: " + prob_vector[0]
    D = "D: " + prob_vector[1]
    H = "H: " + prob_vector[2]
    L = "L: " + prob_vector[3]
    
    # print the results
    print("Probability vector used: " + C + " " + D + " " + H + " " + L)
    print("Desired number of generated trees: " + N)
    print("Number of actually good enough trees created: " + str(len(generated_parasytes)))
    print("Number of leaves of the original parasyte tree: " + str(original_p_size))
    print("Differences:")
    print(distances)
    
    # create histogram without showing it immediately, N is the number of elements of a bin
    # every bin has lenght major of N by 1.
    num_bins = 20
    N, bins, patches = plt.hist(distances, bins=num_bins, edgecolor="black")

    # get centers of the bins: calculate the average value for every bin.
    # (value of current bin + value of next(bin)) / 2
    bin_centers = (bins[:-1] + bins[1:]) / 2.0
    
    # create a map to use later, colors go from green, yellow to red
    cmap = mcolors.LinearSegmentedColormap.from_list("mycmap", ["green", "yellow", "red"])

    # calculate color of every bin, based on the absolute value of center of the bin
    norm = mcolors.Normalize(abs(bin_centers).min(), abs(bin_centers).max())
    colors = cmap(norm(abs(bin_centers)))

    # set color for every bin
    for thispatch, thiscolor in zip(patches, colors):
        thispatch.set_facecolor(thiscolor)
    
    # Creazione delle linee vuote per la legenda
    legend_elements = [Patch(facecolor='white', edgecolor='black', label=C),
                    Patch(facecolor='white', edgecolor='black', label=D),
                    Patch(facecolor='white', edgecolor='black', label=H),
                    Patch(facecolor='white', edgecolor='black', label=L)]

    # Aggiungiamo queste linee alla legenda
    plt.legend(handles=legend_elements, bbox_to_anchor=(-0.24, -0.10), loc='lower left', 
               fontsize="small", title="       Vector")

    plt.xlabel("Difference in the number of leaves")
    plt.ylabel("Number of generated trees")
    
    plt.title("Distribution of difference in the number of leaves\nfrom the original parasyte tree")
    
    plt.show()
            


