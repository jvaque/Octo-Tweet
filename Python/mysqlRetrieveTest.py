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

# Get path to the python script being run
dir = os.path.abspath(os.path.dirname(__file__))

# Retrieve values from config file
with open(f'{dir}/appsettings.json', 'r') as f:
    config = json.load(f)

# ------------------------------------------------------------------------------
# chartTitle = f"{queryDayStart:%d %b %Y}"
# plotLineColor = config['Charts']['electricity_color_line'])
# plotFillColor = config['Charts']['electricity_color_fill'])
# fileName = f"{dir}/images/electricity-plot-{queryDayStart:%Y-%m-%d}.png"

def dailyChart(dailyListOfUse, chartTitle, plotLineColor, plotFillColor, fileName):
    energyList = []
    timeList = []

    for timePeriod in dailyListOfUse:
        energyList.append(timePeriod[1])
        timeList.append(timePeriod[2])

    x_indexes = np.arange(len(timeList))

    plt.plot(timeList, energyList, color=plotLineColor)
    plt.fill_between(timeList, energyList, color=plotFillColor)

    # plt.plot(x_indexes, energyList, color='#0000ff', marker='.')

    # plt.xticks(ticks=x_indexes, labels=timeList)

    ax = plt.axes()

    hours = mdates.HourLocator()
    hours_fmt = mdates.DateFormatter('%H:%M')
    # ax.set_xtics(x_indexes)
    ax.xaxis.set_major_formatter(hours_fmt)
    ax.xaxis.set_minor_locator(hours)

    plt.title(chartTitle)
    plt.xlabel('Time of day (h)')
    plt.ylabel('Energy Consumption (kWh)')

    # plt.legend()

    # plt.grid(True)

    plt.savefig(fileName)
    # plt.show() # commented out when not being tested
    plt.close()
# ------------------------------------------------------------------------------

days = 75
queryDayStart = datetime.date(2020, 9, 23)
# queryDayStart = datetime.date(2020, 10, 23)
queryDayEnd = queryDayStart + datetime.timedelta(1)

for day in range(days):
    # Electricity chart for the day
    listOfUse = []
    
    try:
        cnx = mysql.connector.connect(user=config['MySql']['user_name'], 
                                      password=config['MySql']['password'],
                                      host=config['MySql']['host'],
                                      database=config['MySql']['database_name'])
        
        cursor = cnx.cursor()

        query = "select * from electricity where electricity_interval_start_datetime >= %s and electricity_interval_end_datetime <= %s order by electricity_interval_start_datetime;"
        
        cursor.execute(query, (queryDayStart, queryDayEnd))

        for element in cursor:
            listOfUse.append(element)

        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


    # chartTitle = f"{queryDayStart:%d %b %Y}"
    # plotLineColor = config['Charts']['electricity_color_line'])
    # plotFillColor = config['Charts']['electricity_color_fill'])
    # fileName = f"{dir}/images/electricity-plot-{queryDayStart:%Y-%m-%d}.png"

    # Create and save a copy of the daily chart
    dailyChart(dailyListOfUse=listOfUse, 
               chartTitle=(f"{queryDayStart:%d %b %Y}"), 
               plotLineColor=config['Charts']['electricity_color_line'], 
               plotFillColor=config['Charts']['electricity_color_fill'], 
               fileName=(f"{dir}/images/electricity-plot-{queryDayStart:%Y-%m-%d}.png"))


    # -----------------------------------------------------------------------------------------------------------------------
    # Gas chart for the day
    listOfUse = []
    
    try:
        cnx = mysql.connector.connect(user=config['MySql']['user_name'], 
                                      password=config['MySql']['password'],
                                      host=config['MySql']['host'],
                                      database=config['MySql']['database_name'])
        
        cursor = cnx.cursor()

        query = "select * from gas where gas_interval_start_datetime >= %s and gas_interval_end_datetime <= %s order by gas_interval_start_datetime;"
        
        cursor.execute(query, (queryDayStart, queryDayEnd))

        for element in cursor:
            listOfUse.append(element)

        cursor.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()


    # chartTitle = f"{queryDayStart:%d %b %Y}"
    # plotLineColor = config['Charts']['gas_color_line'])
    # plotFillColor = config['Charts']['gas_color_fill'])
    # fileName = f"{dir}/images/gas-plot-{queryDayStart:%Y-%m-%d}.png"

    # Create and save a copy of the daily chart
    dailyChart(dailyListOfUse=listOfUse, 
               chartTitle=(f"{queryDayStart:%d %b %Y}"), 
               plotLineColor=config['Charts']['gas_color_line'], 
               plotFillColor=config['Charts']['gas_color_fill'], 
               fileName=(f"{dir}/images/gas-plot-{queryDayStart:%Y-%m-%d}.png"))
               

    # -----------------------------------------------------------------------------------------------------------------------
    queryDayStart = queryDayStart + datetime.timedelta(1)
    queryDayEnd = queryDayStart + datetime.timedelta(1)





# Go through the data and produce a daily chart
#
# select the latest date done from the yet to be done table
# 
# retrieve the next day's worth of data
#  select * from electricity where electricity_interval_start_datetime >= '2020-10-23' and electricity_interval_end_datetime <= '2020-10-24' order by electricity_interval_start_datetime;
# make chart
# 
# tweet
# 
# update the letest date done in the database
# 
# finish 

