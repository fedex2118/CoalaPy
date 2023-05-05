import nexusReader as nr
import parasyteTreeGenerator as ptg

def execute_generation(path, pC, pD, pH, pL, N):
    tup = nr.nexus_reader(path)
    tree_list = tup[0]
    dictionary = tup[1]

    host_tree = tree_list[0]
    parasyte_tree = tree_list[1]
    
    print("Host Tree")
    print(host_tree)
    
    prob_vector = [pC, pD, pH, pL]
    ptg.parasyteTreeGenerator(host_tree, parasyte_tree, prob_vector, N, dictionary)