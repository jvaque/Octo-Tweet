import sys
import argparse
import datetime


def parseArguments(args_in):
    # Create the parser
    parser = argparse.ArgumentParser(description='Generate and Tweet charts.',
                                     allow_abbrev=False)

    group = parser.add_mutually_exclusive_group()

    # Add the arguments
    parser.version = '1.0.0'

    parser.add_argument('datetime_from',
                        action='store',
                        type=datetime.datetime.fromisoformat,
                        help='datetime from for chart in ISO format')

    parser.add_argument('datetime_to',
                        action='store',
                        type=datetime.datetime.fromisoformat,
                        help='datetime to for chart in ISO format')

    parser.add_argument('-c',
                        '--charts',
                        action='store',
                        nargs='+',
                        choices=['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly'],
                        help='select the type of charts to generate between the given dates')

    group.add_argument('-t',
                        '--tweet',
                        action='store_true',
                        help='tweet the generated charts')

    group.add_argument('-l',
                        '--lazy',
                        action='store_true',
                        help='skip generating charts, only update database')

    parser.add_argument('-v',
                        '--version',
                        action='version')

    # parser.add_argument()
    # parser.add_argument_group()

    # Execute the parse_args() method
    args = parser.parse_args()
    
    print(vars(args)) # Just here for placing a breakpoint

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

if __name__ == "__main__":
    # print("So far the arguments I want to be able to take in are as follow:")
    # print("--day --week --month --year -d -w -m -y")
    # "args": ["--day", "--week", "--month", "--year", "-d", "-w", "-m", "-y"]
    # print("And if I think of more I will add them in the future")
    # print("You have started the app")
    # print()
    parseArguments(sys.argv)
    # main(*sys.argv[1:])