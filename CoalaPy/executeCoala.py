import executeGeneration as gen
import plotResults as plot
import myParser as mp

def execute_coala():
    parser = mp.MyParser()
    subparsers = parser.add_subparsers(dest="subparser_name")
    
    generation_str = "generation"
    plot_str = "plot"
    
    # parser for generation:
    parser_gen = subparsers.add_parser(generation_str, help="Executes the generation of the parasyte trees.")
    parser_gen.add_argument("path", help="executeGeneration.py needs a path: path of your filename that must be like this 'InputFiles/yourfilename.nex'", type=str)
    parser_gen.add_argument("pC", help="executeGeneration.py needs a Cospeciation probability: a float number that must range from 0.0 to 1.0", type=float)
    parser_gen.add_argument("pD", help="executeGeneration.py needs a Duplication probability: a float number that must range from 0.0 to 1.0", type=float)
    parser_gen.add_argument("pH", help="executeGeneration.py needs a Host Switch probability: a float number that must range from 0.0 to 1.0", type=float)
    parser_gen.add_argument("pL", help="executeGeneration.py needs a Loss probability: a float number that must range from 0.0 to 1.0", type=float)
    parser_gen.add_argument("N", nargs='?', help="executeGeneration.py has a number of Parasyte trees to generate, default value if omitted = 1", default=1, type=int)
    
    # parser for plot:
    parser_plot = subparsers.add_parser(plot_str, help="Executes the plot of the distances between original parasyte tree and generated ones.")
    parser_plot.add_argument("path", help="plotResults.py needs a path: path of your filename that must be like this 'GenParasytes/generatedparasytefilename.txt'", type=str)
    
    args = parser.parse_args()
    
    subparser = args.subparser_name
    
    if subparser == generation_str:
        gen.execute_generation(args.path, args.pC, args.pD, args.pH, args.pL, args.N)
    elif subparser == plot_str:
        plot.execute_plot(args.path)
    else:
        print("executeCoala.py needs an option between {generation} or {plot} to execute properly: try 'python executeCoala.py generation'...")
        parser.print_help() # print help if no parser is passed

def main():
    execute_coala()

if __name__ == "__main__":
    main()