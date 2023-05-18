import tracemalloc
import timeit
from Bio import Phylo
import dendropy
from ete3 import Tree

file_10 = "treeEte_10_leaves.newick"
file_100 = "treeEte_100_leaves.newick"
file_1000 = "treeEte_1000_leaves.newick"
file_10000 = "treeEte_10000_leaves.newick"
file_100000 = "treeEte_100000_leaves.newick"

n_tests = 60

times = {'BioPython': [], 'DendroPy': [], 'ETE3': []}
memories = {'BioPython': [], 'DendroPy': [], 'ETE3': []}

for _ in range(n_tests):

    # time and memory for BioPython
    # tracemalloc.start()
    # start = timeit.default_timer()
    # tree = Phylo.read(file_100000, 'newick')
    # end = timeit.default_timer()
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    # times['BioPython'].append(end - start)
    # memories['BioPython'].append(current)

    # time and memory for DendroPy
    # tracemalloc.start()
    # start = timeit.default_timer()
    # tree = dendropy.Tree.get(path=file_100000, schema="newick")
    # end = timeit.default_timer()
    # current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    # times['DendroPy'].append(end - start)
    # memories['DendroPy'].append(current)

    # time and memory for ETE3
    tracemalloc.start()
    start = timeit.default_timer()
    tree = Tree(file_100000)
    end = timeit.default_timer()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    times['ETE3'].append(end - start)
    memories['ETE3'].append(current)

# Calcola e stampa i tempi medi e l'uso medio della memoria
for library in ['BioPython', 'DendroPy', 'ETE3']:
    avg_time = sum(times[library]) / n_tests
    avg_memory = sum(memories[library]) / n_tests
    print(f"{library} average load time: {avg_time} seconds")
    print(f"{library} average memory usage: {avg_memory / 10**6}MB")