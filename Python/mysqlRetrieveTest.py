import os
import datetime
from tqdm import tqdm


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from datetime import datetime
# import csv
import json

# ------------------------------------------------------------------------------

def dailyChart(dataAccess, config, dir):
    pass

def weeklyCharts(dataAccess, config, dir):
    pass

def montlyCharts(dataAccess, config, dir):
    chartType = 'Gas'
    rollingAverageLenght = 1
    N = rollingAverageLenght * 24 * 2
    N = 4 * 2

    datetimeMonthFrom = datetime.datetime(2020, 11, 1)
    datetimeMonthTo = datetime.datetime(2020, 12, 1)

    args = [chartType, datetimeMonthFrom - datetime.timedelta(days=rollingAverageLenght), datetimeMonthTo + datetime.timedelta(days=rollingAverageLenght)]
    listOfUse = dataAccess.loadData('spDataValues_SelectRecordsFromRange', args, 'MySql')
    
    xList, yList = applyRollingAverage(listOfUse, N)


    # xList, yList = squareData(listOfUse)

    # Create and save a copy of the montly chart
    customChart(
        valuesX=xList,
        valuesY=yList,
        chartTitle=(f"{datetimeMonthFrom:%b %Y}"),
        chartLabelX='Month',
        chartLabelY=f'{chartType} Consumption (kWh)',
        plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
        plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
        plotDateFrom=datetimeMonthFrom,
        plotDateTo=datetimeMonthTo,
        fileName=(os.path.join(dir, 'Images', 'month', f'{chartType.lower()}-plot-4h-rolling-average-{datetimeMonthFrom:%Y-%m}.png')),
        # fileName=(os.path.join(dir, 'Images', 'month', f'{chartType.lower()}-plot-4h-rolling-average-{datetimeMonthFrom:%Y-%m}.svg')),
        majorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
        minorLocatorAxisX=mdates.DayLocator(),
        majorFormatterAxisX=mdates.DateFormatter('%d'),
        minorFormatterAxisX=mdates.DateFormatter('%d')
    )
# ------------------------------------------------------------------------------

def main():
    # Get path to the python script being run
    dir = os.path.abspath(os.path.dirname(__file__))

    # Retrieve values from config file
    with open(os.path.join(dir, 'appsettings.json'), 'r') as f:
        config = json.load(f)
    # This used to be a global variable and now the function doesn't have access
    #  to it, maybe making it into a class might solve it

    makeImagesFoldersIfMissing(dir)
    # Maybe only run this if a specific flag is passed in so that it isn't 
    #  constantly checking every time the script is run

    dataAccess = MySqlDataAccess(config)

    unamedFunctionForNow(dataAccess, config, dir, 'Electricity')
    unamedFunctionForNow(dataAccess, config, dir, 'Gas')

    # dailyCharts(dataAccess, config, dir)
    # weeklyCharts(dataAccess, config, dir)
    # montlyCharts(dataAccess, config, dir)

if __name__ == "__main__":
    main()


# Go through the data and produce a daily chart
#
# select the latest date done from the yet to be done table
# 
# retrieve the next day's worth of data
#
# make chart
# 
# tweet
# 
# update the letest date done in the database
# 
# finish 