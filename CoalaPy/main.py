import nexusReader as nr
import parasyteTreeGenerator as ptg

def main(filename: str):
    tup = nr.nexusReader(filename)
    treeList = tup[0]
    dictionary = tup[1]

    hostTree = treeList[0]
    parasyteTree = treeList[1]

    print("Host Tree")
    print(hostTree)
    ptg.parasyteTreeGenerator(hostTree, parasyteTree, ptg.PROB_VECTOR)


if __name__ == "__main__":
    # how this works: 
    #
    # main("CoalaPy/InputFiles/AP_coala.nex")
    
    main("Write here your nexus file path")
