import sys
import argparse
import datetime

def manualCharts(args):
    if(args.charts != None):
        for chart in args.charts:
            print(chart)

def automaticCharts(args):
    if(args.lazy):
        print("Will skip generating or tweeting charts")
    elif(args.tweet):
        print("Will tweet the charts after generated")
    else:
        print("Will just generate the charts")

def parseArguments():
    # Create the parser
    parser = argparse.ArgumentParser(description='Generate and Tweet charts.',
                                     allow_abbrev=False)

    subparser = parser.add_subparsers()

    manual_parser = subparser.add_parser('charts')
    data_parser = subparser.add_parser('generate')

    data_group = data_parser.add_mutually_exclusive_group()

    # Add the arguments
    parser.version = '1.0.0'

    manual_parser.add_argument(
        'datetime_from',
        action='store',
        type=datetime.datetime.fromisoformat,
        help='datetime from for chart in ISO format')

    manual_parser.add_argument(
        'datetime_to',
        action='store',
        type=datetime.datetime.fromisoformat,
        help='datetime to for chart in ISO format')

    manual_parser.add_argument(
        'charts',
        action='store',
        nargs='+',
        choices=['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly'],
        help='select the type of charts to generate between the given dates')

    manual_parser.set_defaults(func=manualCharts)

    data_group.add_argument(
        '-t',
        '--tweet',
        action='store_true',
        help='tweet the generated charts')

    data_group.add_argument(
        '-l',
        '--lazy',
        action='store_true',
        help='skip generating charts, only update database')

    data_parser.set_defaults(func=automaticCharts)

    parser.add_argument(
        '-v',
        '--version',
        action='version')

    # parser.add_argument()
    # parser.add_argument_group()

    # Execute the parse_args() method
    args = parser.parse_args()
    
    print(vars(args)) # Just here for placing a breakpoint

    return args

# def main(*args):
#     # Take in arguments to select what type of graphs to make and tweet
#     for arg in args:
#         print(arg)

#     # Retrieve the data for the desired graph to be made
#     print("You have retrieved the data for ...")

#     # Create graph from graph library
#     print("Generated the graph with the given data")

#     # Tweet using the twitter api
#     print("Tweeted to your profile")

#     # Log when the program was run and if it was successful

def main():
    args = parseArguments()
    args.func(args)

if __name__ == "__main__":
    main()