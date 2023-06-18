# CoalaPy
A software for co-philogeny recostruction. This is a first prototype of Coala, as such it doesn't implements all the features Coala has.
This program uses python version (3.6.13) and ETE-3 Toolkit version 1.7.9.

CoalaPy is based on a semplified version of the co-evolutionary model of Coala that doesn't have Host-Switch events. It needs a Nexus file in input containing two philogenetic trees, one for hosts and one for parasytes, and current associations for taxa of the two trees (more info on the "How to make it run" section below). It also requires a set of probability for the events of Co-speciation, Duplication and Loss, previously established from the co-evolutionary model. It simulates the evolution of the parasytes species following the evolution of the hosts. The results of such simulation is a finite number of generated parasyte trees that are stored into a text file under the "GenParasytes" folder. The results of such simulation can be used to plot the distributions of leaves and height of generated trees. The plot of such distributions could be useful to see how the generated trees were created for the set of probabilties used.

The Host switch event for this prototype has not been implemented yet. For this reason this software can be used only for DL or Dup-Loss (Duplication-Loss) models and not for DTL ones (Duplication-Transfer-Loss).

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

The results will be printed on the terminal and two istograms will be shown.

# About Benchmark folder

The Benchmark folder contains a randomly generated set of trees that have 10, 100, 1000, 10000, 100000 leaves, scripts and results of a comparison between operations of load tree, preorder, postorder, inorder, levelorder for biopython biophylo module, DendroPy and ETE3 executed 60 times per each tree. The more accurate details of such benchmark will be avaible soon... 
You can download this folder if you want to test it yourself on your operating system and see how your results compare to the ones posted here.

# References

Cophylogeny Reconstruction via an Approximate Bayesian Computation: https://academic.oup.com/sysbio/article/64/3/416/1631550?login=true

Cophylogeny Reconstruction Allowing for Multiple Associations Through Approximate Bayesian Computation: https://arxiv.org/abs/2205.11084


AmoCoala.java: https://team.inria.fr/erable/en/software/amocoala/
ETE-3 Toolkit: https://github.com/etetoolkit/ete
