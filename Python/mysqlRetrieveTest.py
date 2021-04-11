import os
import datetime
import mysql.connector
from mysql.connector import errorcode
from tqdm import tqdm


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from datetime import datetime
# import csv
import json

# ------------------------------------------------------------------------------
def customStepChart(listOfUse, chartTitle, chartLabelX, chartLabelY,
                    plotColorLine, plotColorFill, plotDateFrom, plotDateTo, fileName,
                    majorLocatorAxisX=None, minorLocatorAxisX=None,
                    majorFormatterAxisX=None, minorFormatterAxisX=None):
    '''
    listOfUse: List of consumptions ordered by date as received from the database\n
    chartTitle: Title for the chart\n
    chartLabelX: Label for the x axis label\n
    chartLabelY: Lable for the y axis label\n
    plotColorLine: Color to be used for the line in the chart\n
    plotColorFill: Color to fill the area between the line and the x axis\n
    plotDateFrom: Start date to show in the plot graph\n
    plotDateTo: End date to show in the plot graph\n
    fileName: Full path and filename of where to save the chart\n
    majorLocatorAxisX=None: (Optional) Choose the location of the x axis major
    locators\n
    minorLocatorAxisX=None: (Optional) Choose the location of the x axis minor
    locators\n
    majorFormatterAxisX=None: (Optional) Choose the text format to display on 
    the x axis for the major locators\n
    minorFormatterAxisX=Non: (Optional) Choose the text format to display on 
    the x asis for the minor locators
    '''

    energyUseListPlot = []
    timeListPlot = []

    for element in listOfUse:
        energyUseListPlot.append(element[2])
        timeListPlot.append(element[3])
        energyUseListPlot.append(element[2])
        timeListPlot.append(element[5])

    fig, ax = plt.subplots(figsize=(16,9))

    ax.plot(timeListPlot, energyUseListPlot, color=plotColorLine)
    ax.fill_between(timeListPlot, energyUseListPlot, color=plotColorFill)

    ax.set_xlim(plotDateFrom, plotDateTo)
    if (len(energyUseListPlot) > 0 and max(energyUseListPlot) > 0):
        ax.set_ylim(0, max(energyUseListPlot)*1.1)
    else:
        ax.set_ylim(0, 0.25)

    if (majorLocatorAxisX != None):
        ax.xaxis.set_major_locator(majorLocatorAxisX)
    if (minorLocatorAxisX != None):
        ax.xaxis.set_minor_locator(minorLocatorAxisX)
    if (majorFormatterAxisX != None):
        ax.xaxis.set_major_formatter(majorFormatterAxisX)
    if (minorFormatterAxisX != None):
        ax.xaxis.set_minor_formatter(minorFormatterAxisX)

    ax.tick_params(which='major', width=1.0)
    ax.tick_params(which='major', length=10)
    ax.tick_params(which='minor', width=1.0, labelsize=10)
    ax.tick_params(which='minor', length=5, labelsize=10, labelcolor='0.25')

    ax.set_title(chartTitle)
    ax.set_xlabel(chartLabelX)
    ax.set_ylabel(chartLabelY)

    # ax.legend()

    # ax.grid()
    # ax.grid(axis='y', color='#f5f4d7', linestyle='--')

    plt.savefig(fileName)
    # plt.show()
    plt.close()

# ------------------------------------------------------------------------------
class MySqlDataAccess:
    def __init__(self, config):
        self._config = config

    def callStoredProcedure(self, storedProcedureName, args, connectionStringName):
        try:
            cnx = mysql.connector.connect(
                user=self._config[connectionStringName]['user_name'],
                password=self._config[connectionStringName]['password'],
                host=self._config[connectionStringName]['host'],
                database=self._config[connectionStringName]['database_name'])
            
            cursor = cnx.cursor()

            resultArgs = cursor.callproc(storedProcedureName, args)

            for element in cursor.stored_results():
                listOfResults = element.fetchall()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        finally:
            cursor.close()
            cnx.close()
        
        return listOfResults


def makeImagesFoldersIfMissing(baseDir):
    listOfDirs = ['day', 'week', 'month', 'quarter', 'year']
    for folder in listOfDirs:
        path = os.path.join(baseDir, 'Images', folder)
        if(not os.path.exists(path)):
            os.makedirs(path)
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

    dataAccess = MySqlDataAccess(config)

    # Generate daily charts
    days = 200
    # days = 0 # To easily skip when debugging
    # queryDayStart = datetime.date(2020, 9, 23)
    queryDayStart = datetime.date(2020, 9, 25)
    # queryDayStart = datetime.date(2020, 10, 23)
    # queryDayStart = datetime.date(2021, 3, 22)
    queryDayEnd = queryDayStart + datetime.timedelta(days=1)

    print('Generating batch of day charts')
    for day in tqdm(range(days)):
        # Electricity chart for the day
        listOfUse = []
        
        args = ['Electricity', queryDayStart, queryDayEnd]
        listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryDayStart:%d %b %Y}"),
            chartLabelX='Time of day (h)',
            chartLabelY='Electricity Consumption (kWh)',
            plotColorLine=config['Charts']['electricity_color_line'],
            plotColorFill=config['Charts']['electricity_color_fill'],
            plotDateFrom=queryDayStart,
            plotDateTo=queryDayEnd,
            fileName=(os.path.join(dir, 'Images', 'day', f'electricity-plot-{queryDayStart:%Y-%m-%d}.png')),
            # fileName=(os.path.join(dir, 'Images', 'day', f'electricity-plot-{queryDayStart:%Y-%m-%d}.svg')),
            majorLocatorAxisX=mdates.HourLocator(interval=3),
            minorLocatorAxisX=mdates.HourLocator(),
            majorFormatterAxisX=mdates.DateFormatter('%H:%M')
        )

        # Gas chart for the day
        listOfUse = []
        
        args = ['Gas', queryDayStart, queryDayEnd]
        listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryDayStart:%d %b %Y}"),
            chartLabelX='Time of day (h)',
            chartLabelY='Gas Consumption (kWh)',
            plotColorLine=config['Charts']['gas_color_line'],
            plotColorFill=config['Charts']['gas_color_fill'],
            plotDateFrom=queryDayStart,
            plotDateTo=queryDayEnd,
            fileName=(os.path.join(dir, 'Images', 'day', f'gas-plot-{queryDayStart:%Y-%m-%d}.png')),
            # fileName=(os.path.join(dir, 'Images', 'day', f'gas-plot-{queryDayStart:%Y-%m-%d}.svg')),
            majorLocatorAxisX=mdates.HourLocator(interval=3),
            minorLocatorAxisX=mdates.HourLocator(),
            majorFormatterAxisX=mdates.DateFormatter('%H:%M')
        )

        queryDayStart = queryDayStart + datetime.timedelta(days=1)
        queryDayEnd = queryDayStart + datetime.timedelta(days=1)

    # Generate weekly charts
    weeks = 30
    # weeks = 0 # To easily skip when debugging
    queryWeekStart = datetime.date(2020, 9, 21)
    # queryWeekStart = datetime.date(2020, 10, 23)
    # queryWeekStart = datetime.date(2021, 3, 22)
    queryWeekEnd = queryWeekStart + datetime.timedelta(weeks=1)
    titleDayWeekEnd = queryWeekStart + datetime.timedelta(days=6)

    print('Generating batch of weekly charts')
    for week in tqdm(range(weeks)):
        # Electricity chart for the week
        listOfUse = []
        
        args = ['Electricity', queryWeekStart, queryWeekEnd]
        listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryWeekStart:%d %b %Y}-{titleDayWeekEnd:%d %b %Y}"),
            chartLabelX='Day (h)',
            chartLabelY='Electricity Consumption (kWh)',
            plotColorLine=config['Charts']['electricity_color_line'],
            plotColorFill=config['Charts']['electricity_color_fill'],
            plotDateFrom=queryWeekStart,
            plotDateTo=queryWeekEnd,
            fileName=(os.path.join(dir, 'Images', 'week', f'electricity-plot-{queryWeekStart:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.png')),
            # fileName=(os.path.join(dir, 'Images', 'week', f'electricity-plot-{queryWeekStart:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.svg')),
            majorLocatorAxisX=mdates.DayLocator(),
            minorLocatorAxisX=mdates.HourLocator(interval=6),
            majorFormatterAxisX=mdates.DateFormatter('%a %d'),
            minorFormatterAxisX=mdates.DateFormatter('%H')
        )

        # Gas chart for the week
        listOfUse = []
        
        args = ['Gas', queryWeekStart, queryWeekEnd]
        listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryWeekStart:%d %b %Y}-{titleDayWeekEnd:%d %b %Y}"),
            chartLabelX='Day (h)',
            chartLabelY='Gas Consumption (kWh)',
            plotColorLine=config['Charts']['gas_color_line'],
            plotColorFill=config['Charts']['gas_color_fill'],
            plotDateFrom=queryWeekStart,
            plotDateTo=queryWeekEnd,
            fileName=(os.path.join(dir, 'Images', 'week', f'gas-plot-{queryWeekStart:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.png')),
            # fileName=(os.path.join(dir, 'Images', 'week', f'gas-plot-{queryWeekStart:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.svg')),
            majorLocatorAxisX=mdates.DayLocator(),
            minorLocatorAxisX=mdates.HourLocator(interval=6),
            majorFormatterAxisX=mdates.DateFormatter('%a %d'),
            minorFormatterAxisX=mdates.DateFormatter('%H')
        )

        queryWeekStart = queryWeekStart + datetime.timedelta(weeks=1)
        queryWeekEnd = queryWeekStart + datetime.timedelta(weeks=1)
        titleDayWeekEnd = queryWeekStart + datetime.timedelta(days=6)

    # Generate monthly charts
    months = 12
    # months = 0 # To easily skip when debugging
    currentYear = 2020
    currentMonth = 9
    queryMonthStart = datetime.date(currentYear, currentMonth, 1)
    queryMonthEnd = datetime.date(currentYear, currentMonth+1, 1)
    # queryMonthStart = datetime.date(2020, 10, 1)
    # queryMonthStart = datetime.date(2021, 3, 1)

    print('Generating batch of monthly charts')
    for month in tqdm(range(months)):
        # Electricity chart for the month
        listOfUse = []
        
        args = ['Electricity', queryMonthStart, queryMonthEnd]
        listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryMonthStart:%b %Y}"),
            chartLabelX='Month',
            chartLabelY='Electricity Consumption (kWh)',
            plotColorLine=config['Charts']['electricity_color_line'],
            plotColorFill=config['Charts']['electricity_color_fill'],
            plotDateFrom=queryMonthStart,
            plotDateTo=queryMonthEnd,
            fileName=(os.path.join(dir, 'Images', 'month', f'electricity-plot-{queryMonthStart:%Y-%m}.png')),
            # fileName=(os.path.join(dir, 'Images', 'month', f'electricity-plot-{queryMonthStart:%Y-%m}.svg')),
            majorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
            minorLocatorAxisX=mdates.DayLocator(),
            majorFormatterAxisX=mdates.DateFormatter('%d'),
            minorFormatterAxisX=mdates.DateFormatter('%d')
        )

        # Gas chart for the month
        listOfUse = []
        
        args = ['Gas', queryMonthStart, queryMonthEnd]
        listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryMonthStart:%b %Y}"),
            chartLabelX='Month',
            chartLabelY='Gas Consumption (kWh)',
            plotColorLine=config['Charts']['gas_color_line'],
            plotColorFill=config['Charts']['gas_color_fill'],
            plotDateFrom=queryMonthStart,
            plotDateTo=queryMonthEnd,
            fileName=(os.path.join(dir, 'Images', 'month', f'gas-plot-{queryMonthStart:%Y-%m}.png')),
            # fileName=(os.path.join(dir, 'Images', 'month', f'gas-plot-{queryMonthStart:%Y-%m}.svg')),
            majorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
            minorLocatorAxisX=mdates.DayLocator(),
            majorFormatterAxisX=mdates.DateFormatter('%d'),
            minorFormatterAxisX=mdates.DateFormatter('%d')
        )

        currentMonth +=1
        queryMonthStart = datetime.date(currentYear, currentMonth, 1)
        if (currentMonth >= 12):
            currentMonth = 0
            currentYear +=1
        queryMonthEnd = datetime.date(currentYear, currentMonth+1, 1)



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