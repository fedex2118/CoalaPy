import nexusReader as nr
import parasyteTreeGenerator as ptg
import argparse as arg

def fetch_arguments():
    parser = arg.ArgumentParser()
    parser.add_argument("path", help=" Path of your filename that must be like this InputFiles/yourfilename.nex", type=str)
    parser.add_argument("pC", help=" Cospeciation probability", type=float)
    parser.add_argument("pD", help=" Duplication probability", type=float)
    parser.add_argument("pH", help=" Host Switch probability", type=float)
    parser.add_argument("pL", help=" Loss probability", type=float)
    args = parser.parse_args()
    print(args)
    return args

def execute_coalaPy():
    input = fetch_arguments()
    
    tup = nr.nexusReader(input.path)
    treeList = tup[0]
    dictionary = tup[1]

    hostTree = treeList[0]
    parasyteTree = treeList[1]
    
    print("Host Tree")
    print(hostTree)
    
    prob_vector = [input.pC, input.pD, input.pH, input.pL]
    ptg.parasyteTreeGenerator(hostTree, parasyteTree, prob_vector)

def main():
    execute_coalaPy()

if __name__ == "__main__":    
    main()
