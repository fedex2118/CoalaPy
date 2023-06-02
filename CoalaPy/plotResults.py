from ete3 import PhyloTree
from sys import exit
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.legend import Legend
import matplotlib.pyplot as plt

def open_file(filename):
    
    assert filename.endswith(".txt"), "Wrong format for generated parasytes file: correct format .txt"
    
    generated_parasytes = []
    original_parasyte_tree: PhyloTree = None
    original_parasyte_tree_line = False # Line indicator for original_parasyte_tree
    original_parasyte_tree_str = "Original Parasyte Tree:\n"
    host_tree: PhyloTree = None
    host_tree_line = False # Line indicator for host_tree
    host_tree_str = "Host Tree:\n"
    
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
                    original_parasyte_tree_line = False
                    continue
                if line == host_tree_str: # line == "Host Tree:\n"
                    host_tree_line = True # next line has the actual newick string
                    continue
                if host_tree_line:
                    host_tree = PhyloTree(line.replace('\n', ""))
                    host_tree_line = False
                    continue
                # by default we save PhyloTrees into generated_parasytes container
                generated_parasytes += [PhyloTree(line.replace('\n', ""))] # these are the generated trees.
            except Exception as msg: # if something goes wrong:
                print(msg)
                exit(1)
        f.close()
    
    return generated_parasytes, original_parasyte_tree, host_tree, prob_vector, N

def get_leaf_size(tree: PhyloTree):
    size = 0
    
    for node in tree.iter_leaf_names():
        size += 1
    
    return size

def get_height(tree: PhyloTree): # sum the topology distance +1 to get the exact height of tree
    return tree.get_farthest_leaf(topology_only=True)[1] + 1

def execute_plot(path):
    result_tuple = open_file(path)
    
    generated_parasytes = result_tuple[0]
    original_parasyte_tree = result_tuple[1]
    host_tree = result_tuple[2]
    prob_vector = result_tuple[3]
    N = result_tuple[4]
    
    # get the leaf size of the original p tree
    original_p_leaves = get_leaf_size(original_parasyte_tree)
    # get the leaf size of host tree
    host_tree_leaves = get_leaf_size(host_tree)
    
    # get height of original p tree
    original_p_height = get_height(original_parasyte_tree)
    # get height of host tree
    host_tree_height = get_height(host_tree)
    
    # get leaf size of all the generated trees
    generated_parasytes_leaf_size = [get_leaf_size(tree) for tree in generated_parasytes]
    
    # get height of all generated trees
    generated_parasytes_height = [get_height(tree) for tree in generated_parasytes]
    
    
    C = "C: " + prob_vector[0]
    D = "D: " + prob_vector[1]
    H = "H: " + prob_vector[2]
    L = "L: " + prob_vector[3]
    
    # print the results
    print("Probability vector used: " + C + " " + D + " " + H + " " + L)
    print("Desired number of generated trees: " + N)
    print("Number of actually good enough trees created: " + str(len(generated_parasytes)))
    print("Number of leaves of the host tree: " + str(host_tree_leaves))
    print("Number of leaves of the original parasyte tree: " + str(original_p_leaves))
    print("Height of host tree: " + str(host_tree_height))
    print("Height of original parasyte tree: " + str(original_p_height))
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # 1 row, 2 columns
    
    color_h_line = "crimson"
    color_p_line = "red"
    
    linestyle_h = "-"
    linestyle_p = "--"
    
    label_h = "Host Tree"
    label_p = "Original Parasyte Tree"

    # leaves histogram
    axs[0].hist(generated_parasytes_leaf_size, bins=10, edgecolor='black')
    axs[0].set_xlabel("Number of tree leaves")
    axs[0].set_ylabel("Number of generated trees")
    axs[0].set_title("Distribution of leaves")
    
    # vertical lines for leaves histogram
    axs[0].axvline(host_tree_leaves, color=color_h_line, linestyle=linestyle_h, linewidth=1)
    axs[0].axvline(original_p_leaves, color=color_p_line, linestyle=linestyle_p, linewidth=1)
    
    # empty patches for probability vector
    legend_elements = [Patch(facecolor='white', edgecolor='black', label=C),
                    Patch(facecolor='white', edgecolor='black', label=D),
                    Patch(facecolor='white', edgecolor='black', label=H),
                    Patch(facecolor='white', edgecolor='black', label=L)]
    
    # vector legend
    axs[0].legend(handles=legend_elements, bbox_to_anchor=(-0.21, -0.10), loc='lower left', 
                fontsize="small", title="Vector")

    # lines for custom legend
    legend_elements_2 = [Line2D([0], [0], color=color_h_line, linestyle=linestyle_h, 
                                linewidth=1, label=label_h),
                    Line2D([0], [0], color=color_p_line, linestyle=linestyle_p, 
                           linewidth=1, label=label_p)]

    # secondary custom legend for the vertical lines
    legend_2 = Legend(axs[0], legend_elements_2, [label_h, label_p], 
                      bbox_to_anchor=(-0.21, 1.094), loc='upper left', framealpha=0)
    axs[0].add_artist(legend_2)

    # heights histogram
    axs[1].hist(generated_parasytes_height, bins=10, edgecolor='black')
    axs[1].set_xlabel("Tree heights")
    axs[1].set_ylabel("Number of generated trees")
    axs[1].set_title("Distribution of heights")
    
    # vertical lines for heights histogtam
    axs[1].axvline(host_tree_height, color=color_h_line, linestyle=linestyle_h, linewidth=1)
    axs[1].axvline(original_p_height, color=color_p_line, linestyle=linestyle_p, linewidth=1)

    plt.tight_layout()  # adjust the layout
    plt.show()
            


