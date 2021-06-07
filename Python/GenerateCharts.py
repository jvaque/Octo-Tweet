# Mental note, probably won't work first try as there will be missing
# imports, check from the file you copied the experimenting code from
import os
import datetime
# from tqdm import tqdm


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# from datetime import datetime
# import csv
# import json

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

def makeImagesFoldersIfMissing(baseDir):
    listOfDirs = ['day', 'week', 'month', 'quarter', 'year']
    for folder in listOfDirs:
        path = os.path.join(baseDir, 'Images', folder)
        if(not os.path.exists(path)):
            os.makedirs(path)
