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
def squareData(listOfUse):
    '''
    Take in a list of consumption values and return two lists for\n
    the x and y values so that when charted it appears as steps
    '''
    returnValuesX = []
    returnValuesY = []

    for element in listOfUse:
        returnValuesX.append(element[3])
        returnValuesY.append(element[2])
        returnValuesX.append(element[5])
        returnValuesY.append(element[2])

    return returnValuesX, returnValuesY

def addMonthToDatetime(datetimeVariable):
    year = datetimeVariable.year
    month = datetimeVariable.month
    
    month +=1
    if (month > 12):
        month = 1
        year +=1
    return datetime.datetime(year, month, 1)

def applyRollingAverage(listOfUse, N):
    '''
    Take in a list of consumption values and return two lists for\n
    the x and y values where the y values have a rolling average \n
    the size of N applied to them
    '''
    returnValuesX = []
    tempValuesY = []
    returnValuesY = []
    
    for element in listOfUse:
        returnValuesX.append(element[5])
        tempValuesY.append(element[2])
    
    returnValuesY = np.convolve(tempValuesY, np.ones(N)/N, mode='same')
    
    return returnValuesX, returnValuesY

def customChart(valuesX, valuesY, chartTitle, chartLabelX, chartLabelY,
                    plotColorLine, plotColorFill, plotDateFrom, plotDateTo, fileName,
                    majorLocatorAxisX=None, minorLocatorAxisX=None,
                    majorFormatterAxisX=None, minorFormatterAxisX=None):
    '''
    valuesX: List of time period for consumption values\n
    valuesY: List of consumption values\n
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

    fig, ax = plt.subplots(figsize=(16,9))

    ax.plot(valuesX, valuesY, color=plotColorLine)
    ax.fill_between(valuesX, valuesY, color=plotColorFill)

    ax.set_xlim(plotDateFrom, plotDateTo)
    if (len(valuesY) > 0 and max(valuesY) > 0):
        ax.set_ylim(0, max(valuesY)*1.1)
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
    
    def saveData(self, storedProcedureName, args, connectionStringName):
        try:
            cnx = mysql.connector.connect(
                user=self._config[connectionStringName]['user_name'],
                password=self._config[connectionStringName]['password'],
                host=self._config[connectionStringName]['host'],
                database=self._config[connectionStringName]['database_name'])
            
            cursor = cnx.cursor()

            cursor.callproc(storedProcedureName, args)
            cnx.commit()

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

def makeImagesFoldersIfMissing(baseDir):
    listOfDirs = ['day', 'week', 'month', 'quarter', 'year']
    for folder in listOfDirs:
        path = os.path.join(baseDir, 'Images', folder)
        if(not os.path.exists(path)):
            os.makedirs(path)

# Function to return what charts to make
# Then look through results and check which ones to make
# Foreach:
    # Retrieve data neccesary for chart
    # Generate chart
    # (Tweet)
    # Update database record of charts to make

def unamedFunctionForNow(dataAccess, config, dir, chartType):
    # For now have to do this 
    # args = [chartType]
    # dataSourceRecord = dataAccess.callStoredProcedure('spDataSources_SelectByName', args, 'MySql')

    args = [chartType]
    lastRecord = dataAccess.callStoredProcedure('spDataValues_SelectLatestSavedRecord', args, 'MySql')[0]

    args = [chartType, lastRecord[5]]
    chartsToMake = dataAccess.callStoredProcedure('spChartTracker_SelectChartsToMake', args, 'MySql')

    # End of temp to debug

    for chart in chartsToMake:
        if(chart[2] == 'Daily'):
            # Here we got the last chart made with chart_last_from and chart_last_to
            datetimeDayFrom = chart[5]
            datetimeDayTo = chart[6]
            while (datetimeDayTo < lastRecord[5]):
                args = [chartType, datetimeDayFrom, datetimeDayTo]
                listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')
                xList, yList = squareData(listOfUse)

                # Create and save a copy of the daily chart
                customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeDayFrom:%d %b %Y}"),
                    chartLabelX='Time of day (h)',
                    chartLabelY=f'{chartType} Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeDayFrom,
                    plotDateTo=datetimeDayTo,
                    fileName=(os.path.join(dir, 'Images', 'day', f'{chartType.lower()}-plot-{datetimeDayFrom:%Y-%m-%d}.png')),
                    # fileName=(os.path.join(dir, 'Images', 'day', f'{chartType.lower()}-plot-{datetimeDayFrom:%Y-%m-%d}.svg')),
                    majorLocatorAxisX=mdates.HourLocator(interval=3),
                    minorLocatorAxisX=mdates.HourLocator(),
                    majorFormatterAxisX=mdates.DateFormatter('%H:%M')
                )

                datetimeDayFrom += datetime.timedelta(days=1)
                datetimeDayTo += datetime.timedelta(days=1)

            datetimeDayFromNext = datetimeDayFrom
            datetimeDayToNext = datetimeDayTo

            # Decrease as after generating the last chart the datetime values 
            # would be for the next chart and not the generated ones
            datetimeDayFrom -= datetime.timedelta(days=1)
            datetimeDayTo -= datetime.timedelta(days=1)

            args = [chart[0], datetimeDayFrom, datetimeDayTo, datetimeDayFromNext, datetimeDayToNext]
            dataAccess.saveData('spChartTracker_UpdateTimePeriods', args, 'MySql')

        elif (chart[2] == 'Weekly'):
            datetimeWeekFrom = chart[5]
            datetimeWeekTo = chart[6]
            titleDayWeekEnd = datetimeWeekFrom + datetime.timedelta(days=6)

            while (datetimeWeekTo < lastRecord[5]):
                args = [chartType, datetimeWeekFrom, datetimeWeekTo]
                listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')
                xList, yList = squareData(listOfUse)

                # Create and save a copy of the weekly chart
                customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeWeekFrom:%d %b %Y}-{titleDayWeekEnd:%d %b %Y}"),
                    chartLabelX='Day (h)',
                    chartLabelY=f'{chartType} Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeWeekFrom,
                    plotDateTo=datetimeWeekTo,
                    fileName=(os.path.join(dir, 'Images', 'week', f'{chartType.lower()}-plot-{datetimeWeekFrom:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.png')),
                    # fileName=(os.path.join(dir, 'Images', 'week', f'{chartType.lower()}-plot-{datetimeWeekFrom:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.svg')),
                    majorLocatorAxisX=mdates.DayLocator(),
                    minorLocatorAxisX=mdates.HourLocator(interval=6),
                    majorFormatterAxisX=mdates.DateFormatter('%a %d'),
                    minorFormatterAxisX=mdates.DateFormatter('%H')
                )

                datetimeWeekFrom += datetime.timedelta(weeks=1)
                datetimeWeekTo += datetime.timedelta(weeks=1)
                titleDayWeekEnd = datetimeWeekFrom + datetime.timedelta(days=6)

            datetimeWeekFromNext = datetimeWeekFrom
            datetimeWeekToNext = datetimeWeekTo

            # Decrease as after generating the last chart the datetime values 
            # would be for the next chart and not the generated ones
            datetimeWeekFrom -= datetime.timedelta(weeks=1)
            datetimeWeekTo -= datetime.timedelta(weeks=1)

            args = [chart[0], datetimeWeekFrom, datetimeWeekTo, datetimeWeekFromNext, datetimeWeekToNext]
            dataAccess.saveData('spChartTracker_UpdateTimePeriods', args, 'MySql')

        elif (chart[2] == 'Monthly'):
            datetimeMonthFrom = chart[5]
            datetimeMonthTo = chart[6]
            year = datetimeMonthFrom.year
            month = datetimeMonthFrom.month

            datetimePreviousFrom = datetimeMonthFrom

            while (datetimeMonthTo < lastRecord[5]):
                args = [chartType, datetimeMonthFrom, datetimeMonthTo]
                listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')
                xList, yList = squareData(listOfUse)

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
                    fileName=(os.path.join(dir, 'Images', 'month', f'{chartType.lower()}-plot-{datetimeMonthFrom:%Y-%m}.png')),
                    # fileName=(os.path.join(dir, 'Images', 'month', f'{chartType.lower()}-plot-{datetimeMonthFrom:%Y-%m}.svg')),
                    majorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    minorLocatorAxisX=mdates.DayLocator(),
                    majorFormatterAxisX=mdates.DateFormatter('%d'),
                    minorFormatterAxisX=mdates.DateFormatter('%d')
                )

                datetimePreviousFrom = datetimeMonthFrom

                month +=1
                datetimeMonthFrom = datetime.datetime(year, month, 1)
                if (month >= 12):
                    month = 0
                    year +=1
                datetimeMonthTo = datetime.datetime(year, month+1, 1)

            datetimeMonthFromNext = datetimeMonthFrom
            datetimeMonthToNext = datetimeMonthTo

            # Decrease as after generating the last chart the datetime values 
            # would be for the next chart and not the generated ones
            datetimeMonthFrom = datetimePreviousFrom
            datetimeMonthTo = datetimeMonthFromNext

            args = [chart[0], datetimeMonthFrom, datetimeMonthTo, datetimeMonthFromNext, datetimeMonthToNext]
            dataAccess.saveData('spChartTracker_UpdateTimePeriods', args, 'MySql')

        elif (chart[2] == 'Quarterly'):
            datetimeQuaterFrom = chart[5]
            datetimeQuaterTo = chart[6]

            year = datetimeQuaterFrom.year
            month = datetimeQuaterFrom.month

            datetimePreviousFrom = datetimeQuaterFrom
            # N = 1 * 24 * 2

            while (datetimeQuaterTo < lastRecord[5]):
                args = [chartType, datetimeQuaterFrom, datetimeQuaterTo]
                listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectDailyConsumptionFromRange', args, 'MySql')
                # xList, yList = applyRollingAverage(listOfUse, N)
                xList, yList = squareData(listOfUse)

                # Create and save a copy of the montly chart
                customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeQuaterFrom:%d %b %Y}-{datetimeQuaterTo:%d %b %Y}"),
                    chartLabelX='Quater',
                    chartLabelY=f'{chartType} Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeQuaterFrom,
                    plotDateTo=datetimeQuaterTo,
                    fileName=(os.path.join(dir, 'Images', 'quarter', f'{chartType.lower()}-plot-{datetimeQuaterFrom:%Y-%m}.png')),
                    # fileName=(os.path.join(dir, 'Images', 'quarter', f'{chartType.lower()}-plot-{datetimeQuaterFrom:%Y-%m}.svg')),
                    majorLocatorAxisX=mdates.MonthLocator(),
                    minorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    majorFormatterAxisX=mdates.DateFormatter('%b'),
                    minorFormatterAxisX=mdates.DateFormatter('%d')
                )

                # increase values by three months
                datetimePreviousFrom = datetimeQuaterFrom

                datetimeQuaterFrom = datetimeQuaterTo
                month +=3
                if (month >= 10):
                    month = -2
                    year +=1
                datetimeQuaterTo = datetime.datetime(year, month+3, 1)
            
            # save to the charttracker

    print('Finished!')

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
    listOfUse = dataAccess.callStoredProcedure('spDataValues_SelectRecordsFromRange', args, 'MySql')
    
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