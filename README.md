# CoalaPy
An algorithm that calculates the probability of cophylogeny reconstruction events: it is based on Coala algorithm written in Java, that uses ABC approach for host-parasyte associations.
This is as for now uses python version (3.6.13).It makes use of ETE-3 Toolkit version 1.7.9 for phylogenetic trees.

In the current version, the algorithm reads a nexus file of "Jane / TreeMap Nexus" format 
(more info about the format in the first section of this document: https://team.inria.fr/erable/files/2020/11/Input-File.pdf)
and after starting from the root of the host tree it generates a parasyte tree based on the probabilities of Cospeciation, Duplication and Loss event.

It then stores the generated trees into a file under the "GenParasytes" folder and after that the results can be also used to calculate absolute distance between the original parasyte tree used, and the generated ones. This could be helpful to retrieve information about the history of the generated trees and observe if those ones are close to the real one in terms of size.

The Host switch event as it is right now has not been implemented, so it is for other types of distances. For this reason it can be better described as a DL or Dup-Loss (Duplication-Loss) model instead of a DTL one (Duplication-Transfer-Loss).
The main issue at the moment to calculate other type of distances is that both the original parasyte tree and the generated trees are multilabeled trees.

This is still a work in progress.

# How to make it run?

First of all you need to download ETE-3 Toolkit and use python version 3.6 or below and setup an environment for ETE-3, best practice is to use conda.
Then you need to have matplotlib and numpy libraries installed in order to make the program work.

Coala requires a Nexus file type that must have the same structure of the ones shown here in the "InputFiles/" folder. <br />
Make sure to put your files inside any folder you create in /CoalaPy or just put them inside the one just mentioned before.

To execute CoalaPy inside the terminal or shell activate the environment that uses ete3. <br />
Then just run "executeCoala.py" with the required arguments shown below.

# Example of how to run CoalaPy inside Terminal/Shell:

From the terminal go into CoalaPy path location: .../CoalaPy

(base): conda activate ete3 <br />
(ete3): python executeCoala.py generation InputFiles/Dataset1.nex 0.50 0.40 0.0 0.10 100

There are two main options to run executeCoala.py: <br />

1) generation: Generates the parasyte trees and saves all data of the generation inside a new text file. It requires six other arguments to work: <br />

      argument 1: InputFiles/Dataset1.nex nexus filepath <br />
      argument 2: 0.50 Cospeciation probability <br />
      argument 3: 0.40 Duplication probability <br />
      argument 4: 0.0 Host switch probability Note: in the current version this one must be 0.0 <br />
      argument 5: 0.10 Loss probability <br />
      argument 6: N number of parasyte trees to generate. (N must be <= 300 in the current version). <br />
      
Remember that the sum of the probabilities must be 1.0!

The results will be printed on the terminal and will be placed inside a generated text file that you can later find under GenParasytes folder, so don't delete it.
You can rename the file as you want, don't change the extension of the file.

(ete3): python executeCoala.py plot GenParasytes/data4vect01.txt

2) plot: it shows the results of a simulation with two histograms. The first shows the distribution of the leaves, the second one the distribution of heights of the generated trees. Two vertical lines are used to see how much the generated trees correspond to the ones in input. It requires one argument: <br />
    
    argument 1: gen_results_1d5ia8na.txt text filepath. The results of a generation. <br />

The results will be printed on the terminal and an histogram will be created. It wil show the distribution of difference in the number of leaves from the original parasyte tree and the generated ones.

# About Benchmark folder

The Benchmark folder contains a randomly generated set of trees that have 10, 100, 1000, 10000, 100000 leaves, scripts and results of a comparison between operations of load tree, preorder, postorder, inorder, levelorder for biopython biophylo module, DendroPy and ETE3 executed 60 times per each tree. The more accurate details of such benchmark will be avaible soon... 
You can download this folder if you want to test it yourself on your operating system and see how your results compare to the ones posted here.

# References

Cophylogeny Reconstruction via an Approximate Bayesian Computation: https://academic.oup.com/sysbio/article/64/3/416/1631550?login=true

Cophylogeny Reconstruction Allowing for Multiple Associations Through Approximate Bayesian Computation: https://arxiv.org/abs/2205.11084


AmoCoala.java: https://team.inria.fr/erable/en/software/amocoala/
ETE-3 Toolkit: https://github.com/etetoolkit/ete
