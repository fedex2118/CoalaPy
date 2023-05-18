# CoalaPy
An algorithm that calculates the probability of cophylogeny reconstruction events: it is based on Coala algorithm written in Java, that uses ABC approach for host-parasyte associations.
This is as for now uses python version (3.6.13).It makes use of ETE-3 Toolkit for phylogenetic trees.

In the current version, the algorithm reads a nexus file of "Jane / TreeMap Nexus" format 
(more info about the format in the first section of this document: https://team.inria.fr/erable/files/2020/11/Input-File.pdf)
and after starting from the root of the host tree it generates a parasyte tree based on the probabilities of Cospeciation, Duplication and Loss event.

It then stores the generated trees into a file under the "GenParasytes" folder and after that the results can be also used to calculate absolute distance between the original parasyte tree used, and the generated ones. This could be helpful to retrieve information about the history of the generated trees and observe if those ones are close to the real one in terms of size.

The Host switch event as it is right now has not been implemented yet as for other types of distances.
The main issue at the moment to calculate other type of distances is that both the original parasyte tree and the generated trees are multilabeled trees.

This is still a work in progress.

# How to make it run?

First of all you need to download ETE-3 Toolkit and use python version 3.6 or below and setup an environment for ETE-3, best practice is to use conda.

Coala requires a Nexus file type that must have the same structure of the ones shown here in the "InputFiles/" folder. <br />
Make sure to put your files inside any folder you create in /CoalaPy or just put them inside the one just mentioned before.

To execute CoalaPy inside the terminal or shell activate the environment that uses ete3. <br />
Then just run "executeCoala.py" with the required arguments shown below.

# Example of how to run CoalaPy inside Terminal/Shell:

From the terminal go into CoalaPy path location: .../CoalaPy

(base): conda activate ete3 <br />
(ete3): python executeCoala.py generation InputFiles/Dataset1.nex 0.50 0.40 0.0 0.10 100

There are two main options to run executeCoala.py: <br />

1) generation: Generates the parasyte trees, it requires six other arguments to work: <br />

      argument 1: InputFiles/Dataset1.nex nexus filepath <br />
      argument 2: 0.50 Cospeciation probability <br />
      argument 3: 0.40 Duplication probability <br />
      argument 4: 0.0 Host switch probability Note: in the current version this one must be 0.0 <br />
      argument 5: 0.10 Loss probability <br />
      argument 6: N number of parasyte trees to generate. (N must be <= 300 in the current version). <br />
      
Remember that the sum of the probabilities must be 1.0!

The results will be printed on the terminal.

(ete3): python executeCoala.py plot GenParasytes/gen_results_1d5ia8na.txt

2) plot: Generates the absolute distances in size between original parasyte tree and the generated ones. It requires one other argument: <br />
    
    argument 1: gen_results_1d5ia8na.txt text filepath. The results of a generation. <br />

The results will be printed on the terminal.

# About Random Dataset folder

Random_Dataset folder contains newick files that have newick trees inside of them that were generated randomly with a simpler algorithm. Don't use these files for generation neither plotting since the structure of these files is not the same of Coala datasets. Those files should be used instead for other purposes, as to test your implementations in ete-3.

# More info

More details about the algorithm functionality are showed in the following links below:

Cophylogeny Reconstruction via an Approximate Bayesian Computation: https://academic.oup.com/sysbio/article/64/3/416/1631550?login=true

Cophylogeny Reconstruction Allowing for Multiple Associations Through Approximate Bayesian Computation: https://arxiv.org/abs/2205.11084


AmoCoala.java: https://team.inria.fr/erable/en/software/amocoala/
ETE-3 Toolkit: https://github.com/etetoolkit/ete
