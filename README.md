# CoalaPy
An algorithm that calculates the probability of cophylogeny reconstruction events based on ABC approach for host-parasyte associations.
This is a python version (3.6.13) of an already existing algorithm written in java. It makes use of ETE-3 Toolkit for phylogenetic trees.

In the current version, the algorithm reads a nexus file of "Jane / TreeMap Nexus" format 
(more info about the format in the first section of this document: https://team.inria.fr/erable/files/2020/11/Input-File.pdf)
and after starting from the root of the host tree it generates a parasyte tree based on the probabilities of Cospeciation, Duplication and Loss event.

The Host switch event as it is right now has not been implemented yet.

This is still a work in progress.

# How to make it run?

First of all you need to download ETE-3 Toolkit and use python version 3.6 or below and setup an environment for ETE-3, best practice is to use conda.

Coala requires a Nexus file type that must have the same structure of the ones shown here in the "InputFiles/" folder. <br />
Make sure to put your files inside any folder you create in /CoalaPy or just put them inside the one just mentioned before.

To execute coalaPy inside the terminal or shell activate the environment that uses ete3. <br />
Then just run "executeCoala.py" with the required arguments shown below.

# Example of how to run CoalaPy inside Terminal/Shell:

(base): conda activate ete3 <br />
(ete3): python executeCoala.py InputFiles/AP_coala.nex 0.50 0.40 0.0 0.10

argument 1: InputFiles/AP_coala.nex nexus filepath <br />
argument 2: 0.50 Cospeciation probability <br />
argument 3: 0.40 Duplication probability <br />
argument 4: 0.0 Host switch probability Note: in the current version this one must be 0.0 <br />
argument 5: 0.10 Loss probability

The results will be printed on the terminal. 

# More info

More details about the algorithm functionality are showed in the following links below:

Cophylogeny Reconstruction via an Approximate Bayesian Computation: https://academic.oup.com/sysbio/article/64/3/416/1631550?login=true

Cophylogeny Reconstruction Allowing for Multiple Associations Through Approximate Bayesian Computation: https://arxiv.org/abs/2205.11084


AmoCoala.java: https://team.inria.fr/erable/en/software/amocoala/
ETE-3 Toolkit: https://github.com/etetoolkit/ete
