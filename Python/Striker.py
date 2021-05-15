import os
import json
import sys
import argparse
import datetime

from MySqlDataAccess import MySqlDataAccess

import mysqlRetrieveTest # This name is only temporary

def manualCharts(config, dir, args):
    if(args.charts != None):
        for chart in args.charts:
            print(chart)

def automaticCharts(config, dir, args):
    if(args.lazy):
        print("Will skip generating or tweeting charts")
    elif(args.tweet):
        print("Will tweet the charts after generated")
    else:
        print("Will just generate the charts")
        mysqlRetrieveTest.makeImagesFoldersIfMissing(dir)
        # Maybe only run this if a specific flag is passed in so that it isn't 
        #  constantly checking every time the script is run

        dataAccess = MySqlDataAccess(config)

        mysqlRetrieveTest.unamedFunctionForNow(dataAccess, config, dir, 'Electricity')
        mysqlRetrieveTest.unamedFunctionForNow(dataAccess, config, dir, 'Gas')

def parseArguments():
    # Create the parser
    parser = argparse.ArgumentParser(description='Generate and Tweet charts.',
                                     allow_abbrev=False)
    subparser = parser.add_subparsers()

    parser.version = '1.0.0'

    parser.add_argument(
        '-v',
        '--version',
        action='version')

    # charts
    manual_parser = subparser.add_parser('charts')

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


    # generate
    data_parser = subparser.add_parser('generate')

    data_group = data_parser.add_mutually_exclusive_group()

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

    # Execute the parse_args() method
    args = parser.parse_args()
    print(vars(args)) # Just here for placing a breakpoint

    return args

def main():
    # Get path to the python script being run
    dir = os.path.abspath(os.path.dirname(__file__))

    # Retrieve values from config file
    with open(os.path.join(dir, 'appsettings.json'), 'r') as f:
        config = json.load(f)

    args = parseArguments()
    args.func(config, dir, args)

if __name__ == "__main__":
    main()