import timeit
from Bio import Phylo
import dendropy
from ete3 import Tree

# preorder function for BioPython
def biopython_preorder(tree_path):
    tree = Phylo.read(tree_path, 'newick')
    for clade in tree.find_clades(order='preorder'):
        pass

# preorder function for DendroPy
def dendropy_preorder(tree_path):
    tree = dendropy.Tree.get(path=tree_path, schema='newick')
    for node in tree.preorder_node_iter():
        pass

# preorder function for ETE3
def ete3_preorder(tree_path):
    tree = Tree(tree_path)
    for node in tree.traverse(strategy='preorder'):
        pass

# inorder  function for DendroPy
def dendropy_inorder(tree_path):
    tree = dendropy.Tree.get(path=tree_path, schema='newick')
    for node in tree.inorder_node_iter():
        pass

# postorder function for BioPython
def biopython_postorder(tree_path):
    tree = Phylo.read(tree_path, 'newick')
    for clade in tree.find_clades(order='postorder'):
        pass

# postorder function for DendroPy
def dendropy_postorder(tree_path):
    tree = dendropy.Tree.get(path=tree_path, schema='newick')
    for node in tree.postorder_node_iter():
        pass

# postorder function for ETE3
def ete3_postorder(tree_path):
    tree = Tree(tree_path)
    for node in tree.traverse(strategy='postorder'):
        pass

# levelorder function for BioPython
def biopython_levelorder(tree_path):
    tree = Phylo.read(tree_path, 'newick')
    for clade in tree.find_clades(order='level'):
        pass

# levelorder function for DendroPy
def dendropy_levelorder(tree_path):
    tree = dendropy.Tree.get(path=tree_path, schema='newick')
    for node in tree.levelorder_node_iter():
        pass

# levelorder function for ETE3
def ete3_levelorder(tree_path):
    tree = Tree(tree_path)
    for node in tree.traverse(strategy='levelorder'):
        pass

# Tree path:
file_10 = "treeEte_10_leaves.newick"
file_100 = "treeEte_100_leaves.newick"
file_1000 = "treeEte_1000_leaves.newick"
file_10000 = "treeEte_10000_leaves.newick"
file_100000 = "treeEte_100000_leaves.newick"

n_tests = 60

# execution time for libraries: with Preorder, remove comments:
# biopython_time = timeit.timeit(lambda: biopython_preorder(file_100000), number=n_tests)
# dendropy_time = timeit.timeit(lambda: dendropy_preorder(file_100000), number=n_tests)
# ete3_time = timeit.timeit(lambda: ete3_preorder(file_100000), number=n_tests)

# execution time for libraries: with Inorder, remove comments:
# dendropy_time = timeit.timeit(lambda: dendropy_inorder(file_100000), number=n_tests)

# execution time for libraries: with Postorder, remove comments:
# biopython_time = timeit.timeit(lambda: biopython_postorder(file_100000), number=n_tests)
# dendropy_time = timeit.timeit(lambda: dendropy_postorder(file_100000), number=n_tests)
# ete3_time = timeit.timeit(lambda: ete3_postorder(file_100000), number=n_tests)

# execution time for libraries: with Levelorder remove comments:
# biopython_time = timeit.timeit(lambda: biopython_levelorder(file_100000), number=n_tests)
dendropy_time = timeit.timeit(lambda: dendropy_levelorder(file_100000), number=n_tests)
# ete3_time = timeit.timeit(lambda: ete3_levelorder(file_100000), number=n_tests)

# print execution time:
# print(f"BioPython time: {biopython_time}")
print(f"DendroPy time: {dendropy_time}")
# print(f"ETE3 time: {ete3_time}")