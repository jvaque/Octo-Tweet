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
# chartTitle = f"{queryDayStart:%d %b %Y}"
# plotLineColor = config['Charts']['electricity_color_line'])
# plotFillColor = config['Charts']['electricity_color_fill'])
# fileName = f"{dir}/images/day/electricity-plot-{queryDayStart:%Y-%m-%d}.png"

def dailyChart(dailyListOfUse, chartTitle, plotLineColor, plotFillColor, fileName):
    energyList = []
    timeList = []

    for timePeriod in dailyListOfUse:
        energyList.append(timePeriod[1])
        timeList.append(timePeriod[2])

    x_indexes = np.arange(len(timeList))

    fig, ax = plt.subplots()

    ax.plot(timeList, energyList, color=plotLineColor)
    ax.fill_between(timeList, energyList, color=plotFillColor)

    # plt.plot(x_indexes, energyList, color='#0000ff', marker='.')

    # plt.xticks(ticks=x_indexes, labels=timeList)


    hours = mdates.HourLocator()
    hours_fmt = mdates.DateFormatter('%H:%M')
    # ax.set_xtics(x_indexes)
    ax.xaxis.set_major_formatter(hours_fmt)
    ax.xaxis.set_minor_locator(hours)

    # Commented out the addition of margins as found them ugly
    # ax.margins(x=0, y=0)
    ax.set_ylim(0, max(energyList)*1.2)
    ax.set_xlim(min(timeList),max(timeList))

    plt.title(chartTitle)
    plt.xlabel('Time of day (h)')
    plt.ylabel('Energy Consumption (kWh)')

    # plt.legend()

    # plt.grid(True)

    plt.savefig(fileName)
    # plt.show() # commented out when not being tested
    plt.close()
# ------------------------------------------------------------------------------
# chartTitle = f"{queryWeekStart:%d %b %Y}"
# plotLineColor = config['Charts']['electricity_color_line'])
# plotFillColor = config['Charts']['electricity_color_fill'])
# fileName = f"{dir}/images/week/electricity-plot-{queryWeekStart:%Y-%m-%d}-{queryWeekEnd:%Y-%m-%d}.png"

def weeklyChart(weeklyListOfUse, chartTitle, plotLineColor, plotFillColor, fileName):
    energyList = []
    timeList = []

    for timePeriod in weeklyListOfUse:
        energyList.append(timePeriod[1])
        timeList.append(timePeriod[2])

    x_indexes = np.arange(len(timeList))

    plt.plot(timeList, energyList, color=plotLineColor)
    plt.fill_between(timeList, energyList, color=plotFillColor)

    # plt.plot(x_indexes, energyList, color='#0000ff', marker='.')

    # plt.xticks(ticks=x_indexes, labels=timeList)

    ax = plt.axes()

    hours = mdates.HourLocator(interval=6)
    hour_fmt = mdates.DateFormatter('%H')
    days = mdates.DayLocator()
    day_fmt = mdates.DateFormatter('%a %d')
    # ax.set_xtics(x_indexes)
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_minor_locator(hours)
    ax.xaxis.set_major_formatter(day_fmt)
    ax.xaxis.set_minor_formatter(hour_fmt)

    # Commented out the addition of margins as found them ugly
    # ax.margins(x=0, y=0)

    plt.title(chartTitle)
    plt.xlabel('Time of day (h)')
    plt.ylabel('Energy Consumption (kWh)')

    # plt.legend()

    # plt.grid(True)

    plt.savefig(fileName)
    # plt.show() # commented out when not being tested
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
    queryDayStart = datetime.date(2020, 9, 23)
    # queryDayStart = datetime.date(2020, 10, 23)
    # queryDayStart = datetime.date(2021, 3, 22)
    queryDayEnd = queryDayStart + datetime.timedelta(1)

    for day in range(days):
        # Electricity chart for the day
        listOfUse = []
        
        args = [queryDayStart, queryDayEnd]
        listOfUse = dataAccess.callStoredProcedure('spElectricity_GetRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        dailyChart(dailyListOfUse=listOfUse, 
                chartTitle=(f"{queryDayStart:%d %b %Y}"), 
                plotLineColor=config['Charts']['electricity_color_line'], 
                plotFillColor=config['Charts']['electricity_color_fill'], 
                fileName=(os.path.join(dir, 'Images', 'day', f'electricity-plot-{queryDayStart:%Y-%m-%d}.png')))

        # Gas chart for the day
        listOfUse = []
        
        args = [queryDayStart, queryDayEnd]
        listOfUse = dataAccess.callStoredProcedure('spGas_GetRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        dailyChart(dailyListOfUse=listOfUse, 
                chartTitle=(f"{queryDayStart:%d %b %Y}"), 
                plotLineColor=config['Charts']['gas_color_line'], 
                plotFillColor=config['Charts']['gas_color_fill'], 
                fileName=(os.path.join(dir, 'Images', 'day', f'gas-plot-{queryDayStart:%Y-%m-%d}.png')))

        queryDayStart = queryDayStart + datetime.timedelta(1)
        queryDayEnd = queryDayStart + datetime.timedelta(1)

    # Generate weekly charts
    weeks = 21
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
        weeklyChart(weeklyListOfUse=listOfUse, 
                chartTitle=(f"{queryWeekStart:%d %b %Y}-{queryWeekEnd:%d %b %Y}"), 
                plotLineColor=config['Charts']['electricity_color_line'], 
                plotFillColor=config['Charts']['electricity_color_fill'], 
                fileName=(os.path.join(dir, 'Images', 'week', f'electricity-plot-{queryWeekStart:%Y-%m-%d}-{queryWeekEnd:%Y-%m-%d}.png')))

        # Gas chart for the week
        listOfUse = []
        
        args = [queryWeekStart, queryWeekEnd]
        listOfUse = dataAccess.callStoredProcedure('spGas_GetRecordsFromRange', args, 'MySql')

        # Create and save a copy of the daily chart
        weeklyChart(weeklyListOfUse=listOfUse, 
                chartTitle=(f"{queryWeekStart:%d %b %Y}-{queryWeekEnd:%d %b %Y}"), 
                plotLineColor=config['Charts']['gas_color_line'], 
                plotFillColor=config['Charts']['gas_color_fill'], 
                fileName=(os.path.join(dir, 'Images', 'week', f'gas-plot-{queryWeekStart:%Y-%m-%d}-{queryWeekEnd:%Y-%m-%d}.png')))

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