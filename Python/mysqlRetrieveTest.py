import os
import datetime
import mysql.connector
from mysql.connector import errorcode


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
        energyUseListPlot.append(element[1])
        timeListPlot.append(element[2])
        energyUseListPlot.append(element[1])
        timeListPlot.append(element[4])

    fig, ax = plt.subplots()

    ax.plot(timeListPlot, energyUseListPlot, color=plotColorLine)
    ax.fill_between(timeListPlot, energyUseListPlot, color=plotColorFill)

    ax.set_xlim(plotDateFrom, plotDateTo)
    if (len(energyUseListPlot) > 0):
        ax.set_ylim(0, max(energyUseListPlot)*1.1)

    if (majorLocatorAxisX != None):
        ax.xaxis.set_major_locator(majorLocatorAxisX)
    if (minorLocatorAxisX != None):
        ax.xaxis.set_minor_locator(minorLocatorAxisX)
    if (majorFormatterAxisX != None):
        ax.xaxis.set_major_formatter(majorFormatterAxisX)
    if (minorFormatterAxisX != None):
        ax.xaxis.set_minor_formatter(minorFormatterAxisX)

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
    days = 140
    # queryDayStart = datetime.date(2020, 9, 23)
    queryDayStart = datetime.date(2020, 9, 25)
    # queryDayStart = datetime.date(2020, 10, 23)
    # queryDayStart = datetime.date(2021, 3, 22)
    queryDayEnd = queryDayStart + datetime.timedelta(1)

    for day in range(days):
        # Electricity chart for the day
        listOfUse = []
        
        args = [queryDayStart, queryDayEnd]
        listOfUse = dataAccess.callStoredProcedure('spElectricity_GetRecordsFromRange', args, 'MySql')

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
            minorLocatorAxisX=mdates.HourLocator(),
            majorFormatterAxisX=mdates.DateFormatter('%H:%M')
        )

        # Gas chart for the day
        listOfUse = []
        
        args = [queryDayStart, queryDayEnd]
        listOfUse = dataAccess.callStoredProcedure('spGas_GetRecordsFromRange', args, 'MySql')

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
            minorLocatorAxisX=mdates.HourLocator(),
            majorFormatterAxisX=mdates.DateFormatter('%H:%M')
        )

        queryDayStart = queryDayStart + datetime.timedelta(1)
        queryDayEnd = queryDayStart + datetime.timedelta(1)

    # Generate weekly charts
    weeks = 30
    queryWeekStart = datetime.date(2020, 9, 21)
    # queryWeekStart = datetime.date(2020, 10, 23)
    # queryWeekStart = datetime.date(2021, 3, 22)
    queryWeekEnd = queryWeekStart + datetime.timedelta(6)

    for week in range(weeks):
        # Electricity chart for the week
        listOfUse = []
        
        args = [queryWeekStart, queryWeekEnd]
        listOfUse = dataAccess.callStoredProcedure('spElectricity_GetRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryWeekStart:%d %b %Y}-{queryWeekEnd:%d %b %Y}"),
            chartLabelX='Day (h)',
            chartLabelY='Electricity Consumption (kWh)',
            plotColorLine=config['Charts']['electricity_color_line'],
            plotColorFill=config['Charts']['electricity_color_fill'],
            plotDateFrom=queryWeekStart,
            plotDateTo=queryWeekEnd,
            fileName=(os.path.join(dir, 'Images', 'week', f'electricity-plot-{queryWeekStart:%Y-%m-%d}-{queryWeekEnd:%Y-%m-%d}.png')),
            # fileName=(os.path.join(dir, 'Images', 'week', f'electricity-plot-{queryWeekStart:%Y-%m-%d}-{queryWeekEnd:%Y-%m-%d}.svg')),
            majorLocatorAxisX=mdates.DayLocator(),
            minorLocatorAxisX=mdates.HourLocator(interval=6),
            majorFormatterAxisX=mdates.DateFormatter('%a %d'),
            minorFormatterAxisX=mdates.DateFormatter('%H')
        )

        # Gas chart for the week
        listOfUse = []
        
        args = [queryWeekStart, queryWeekEnd]
        listOfUse = dataAccess.callStoredProcedure('spGas_GetRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        customStepChart(
            listOfUse=listOfUse,
            chartTitle=(f"{queryWeekStart:%d %b %Y}-{queryWeekEnd:%d %b %Y}"),
            chartLabelX='Day (h)',
            chartLabelY='Gas Consumption (kWh)',
            plotColorLine=config['Charts']['gas_color_line'],
            plotColorFill=config['Charts']['gas_color_fill'],
            plotDateFrom=queryWeekStart,
            plotDateTo=queryWeekEnd,
            fileName=(os.path.join(dir, 'Images', 'week', f'gas-plot-{queryWeekStart:%Y-%m-%d}-{queryWeekEnd:%Y-%m-%d}.png')),
            # fileName=(os.path.join(dir, 'Images', 'week', f'gas-plot-{queryWeekStart:%Y-%m-%d}-{queryWeekEnd:%Y-%m-%d}.svg')),
            majorLocatorAxisX=mdates.DayLocator(),
            minorLocatorAxisX=mdates.HourLocator(interval=6),
            majorFormatterAxisX=mdates.DateFormatter('%a %d'),
            minorFormatterAxisX=mdates.DateFormatter('%H')
        )

        queryWeekStart = queryWeekStart + datetime.timedelta(7)
        queryWeekEnd = queryWeekStart + datetime.timedelta(6)

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