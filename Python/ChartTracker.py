import os
import datetime
import matplotlib.dates as mdates

import GenerateCharts


# Function to return what charts to make
# Then look through results and check which ones to make
# Foreach:
    # Retrieve data neccesary for chart
    # Generate chart
    # (Tweet)
    # Update database record of charts to make

# def unamedFunctionForNow(dataAccess, config, dir, chartType):
def generateIfAvailable(dataAccess, config, dir, chartType):
    chartsGenerated = []

    args = [chartType]
    lastRecord = dataAccess.loadData('spDataValues_SelectLatestSavedRecord', args, 'MySql')[0]

    args = [chartType, lastRecord[5]]
    chartsToMake = dataAccess.loadData('spChartTracker_SelectChartsToMake', args, 'MySql')

    for chart in chartsToMake:
        if(chart[2] == 'Daily'):
            datetimeDayFrom = chart[5]
            datetimeDayTo = chart[6]

            datetimePreviousFrom = datetimeDayFrom

            while (datetimeDayTo < lastRecord[5]):
                fileName = f'{chartType.lower()}-plot-{datetimeDayFrom:%Y-%m-%d}.png'
                # fileName = f'{chartType.lower()}-plot-{datetimeDayFrom:%Y-%m-%d}.svg'
                fullFilePath = os.path.join(dir, 'Images', 'day', fileName)

                args = [chartType, datetimeDayFrom, datetimeDayTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectRecordsFromRange', args, 'MySql')
                totalConsumptionForInterval = dataAccess.loadData('spDataValues_SelectTotalConsumptionFromRange', args, 'MySql')[0]
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the daily chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeDayFrom:%d %b %Y}"),
                    chartLabelX='Time of day (h)',
                    chartLabelY=f'{chartType} Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeDayFrom,
                    plotDateTo=datetimeDayTo,
                    fileName=fullFilePath,
                    majorLocatorAxisX=mdates.HourLocator(interval=3),
                    minorLocatorAxisX=mdates.HourLocator(),
                    majorFormatterAxisX=mdates.DateFormatter('%H:%M')
                )

                chartsGenerated.append({
                    'EnergySource': chartType,
                    'ChartType': chart[2],
                    'Files': [fullFilePath],
                    'Message': f'{chartType} {datetimeDayFrom:%d-%m-%Y} consumption. \nTotal daily {chartType} consumption: {totalConsumptionForInterval[2]:.3f}kWh\n\n#OctopusSmartDayCharts\n#Octopus{chartType}DayCharts'
                })

                datetimePreviousFrom = datetimeDayFrom

                datetimeDayFrom += datetime.timedelta(days=1)
                datetimeDayTo += datetime.timedelta(days=1)

            updateChartsGenerated(dataAccess, chart[0], datetimePreviousFrom, datetimeDayFrom, datetimeDayTo)

        elif (chart[2] == 'Weekly'):
            datetimeWeekFrom = chart[5]
            datetimeWeekTo = chart[6]
            titleDayWeekEnd = datetimeWeekFrom + datetime.timedelta(days=6)

            datetimePreviousFrom = datetimeWeekFrom

            while (datetimeWeekTo < lastRecord[5]):
                fileName = f'{chartType.lower()}-plot-{datetimeWeekFrom:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.png'
                # fileName = f'{chartType.lower()}-plot-{datetimeWeekFrom:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.svg'
                fullFilePath = os.path.join(dir, 'Images', 'week', fileName)

                args = [chartType, datetimeWeekFrom, datetimeWeekTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectRecordsFromRange', args, 'MySql')
                totalConsumptionForInterval = dataAccess.loadData('spDataValues_SelectTotalConsumptionFromRange', args, 'MySql')[0]
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the weekly chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeWeekFrom:%d %b %Y}-{titleDayWeekEnd:%d %b %Y}"),
                    chartLabelX='Day (h)',
                    chartLabelY=f'{chartType} Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeWeekFrom,
                    plotDateTo=datetimeWeekTo,
                    fileName=fullFilePath,
                    majorLocatorAxisX=mdates.DayLocator(),
                    minorLocatorAxisX=mdates.HourLocator(interval=6),
                    majorFormatterAxisX=mdates.DateFormatter('%a %d'),
                    minorFormatterAxisX=mdates.DateFormatter('%H')
                )

                chartsGenerated.append({
                    'EnergySource': chartType,
                    'ChartType': chart[2],
                    'Files': [fullFilePath],
                    'Message': f'{chartType} {datetimeWeekFrom:%d-%m-%Y} to {titleDayWeekEnd:%d-%m-%Y} consumption. \nTotal weekly {chartType} consumption: {totalConsumptionForInterval[2]:.3f}kWh\n\n#OctopusSmartWeekCharts\n#Octopus{chartType}WeekCharts'
                })

                datetimePreviousFrom = datetimeWeekFrom

                datetimeWeekFrom += datetime.timedelta(weeks=1)
                datetimeWeekTo += datetime.timedelta(weeks=1)
                titleDayWeekEnd = datetimeWeekFrom + datetime.timedelta(days=6)

            updateChartsGenerated(dataAccess, chart[0], datetimePreviousFrom, datetimeWeekFrom, datetimeWeekTo)

        elif (chart[2] == 'Monthly'):
            datetimeMonthFrom = chart[5]
            datetimeMonthTo = chart[6]

            datetimePreviousFrom = datetimeMonthFrom

            while (datetimeMonthTo < lastRecord[5]):
                tempMonthlyGrouping = []

                fileName = f'{chartType.lower()}-plot-{datetimeMonthFrom:%Y-%m}.png'
                # fileName = f'{chartType.lower()}-plot-{datetimeMonthFrom:%Y-%m}.svg'
                fullFilePath = os.path.join(dir, 'Images', 'month', fileName)

                args = [chartType, datetimeMonthFrom, datetimeMonthTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectRecordsFromRange', args, 'MySql')
                totalConsumptionForInterval = dataAccess.loadData('spDataValues_SelectTotalConsumptionFromRange', args, 'MySql')[0]
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeMonthFrom:%b %Y}"),
                    chartLabelX='Day (h)',
                    chartLabelY=f'{chartType} Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeMonthFrom,
                    plotDateTo=datetimeMonthTo,
                    fileName=fullFilePath,
                    majorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    minorLocatorAxisX=mdates.DayLocator(),
                    majorFormatterAxisX=mdates.DateFormatter('%d'),
                    minorFormatterAxisX=mdates.DateFormatter('%d')
                )

                tempMonthlyGrouping.append(fullFilePath)

                fileName = f'{chartType.lower()}-daily-plot-{datetimeMonthFrom:%Y-%m}.png'
                # fileName = f'{chartType.lower()}-daily-plot-{datetimeMonthFrom:%Y-%m}.svg'
                fullFilePath = os.path.join(dir, 'Images', 'month', fileName)

                listOfUse = dataAccess.loadData('spDataValues_SelectDailyConsumptionFromRange', args, 'MySql')
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeMonthFrom:%b %Y}"),
                    chartLabelX='Day',
                    chartLabelY=f'{chartType} Daily Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeMonthFrom,
                    plotDateTo=datetimeMonthTo,
                    fileName=fullFilePath,
                    majorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    minorLocatorAxisX=mdates.DayLocator(),
                    majorFormatterAxisX=mdates.DateFormatter('%d'),
                    minorFormatterAxisX=mdates.DateFormatter('%d')
                )

                tempMonthlyGrouping.append(fullFilePath)
                chartsGenerated.append({
                    'EnergySource': chartType,
                    'ChartType': chart[2],
                    'Files': tempMonthlyGrouping,
                    'Message': f'{chartType} {datetimeMonthFrom:%b %Y} consumption. \nTotal monthly {chartType} consumption: {totalConsumptionForInterval[2]:.3f}kWh\n\n#OctopusSmartMonthCharts\n#Octopus{chartType}MonthCharts'
                })

                datetimePreviousFrom = datetimeMonthFrom

                datetimeMonthFrom = addMonthsToDatetime(datetimeMonthFrom, 1)
                datetimeMonthTo = addMonthsToDatetime(datetimeMonthTo, 1)

            updateChartsGenerated(dataAccess, chart[0], datetimePreviousFrom, datetimeMonthFrom, datetimeMonthTo)

        elif (chart[2] == 'Quarterly'):
            datetimeQuarterFrom = chart[5]
            datetimeQuarterTo = chart[6]

            titleDayQuarterEnd = datetimeQuarterTo - datetime.timedelta(days=1)

            datetimePreviousFrom = datetimeQuarterFrom
            # N = 1 * 24 * 2

            while (datetimeQuarterTo < lastRecord[5]):
                fileName = f'{chartType.lower()}-plot-{datetimeQuarterFrom:%Y-%m-%d}-{titleDayQuarterEnd:%Y-%m-%d}.png'
                # fileName = f'{chartType.lower()}-plot-{datetimeQuarterFrom:%Y-%m-%d}-{titleDayQuarterEnd:%Y-%m-%d}.svg'
                fullFilePath = os.path.join(dir, 'Images', 'quarter', fileName)

                args = [chartType, datetimeQuarterFrom, datetimeQuarterTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectDailyConsumptionFromRange', args, 'MySql')
                totalConsumptionForInterval = dataAccess.loadData('spDataValues_SelectTotalConsumptionFromRange', args, 'MySql')[0]
                # xList, yList = applyRollingAverage(listOfUse, N)
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeQuarterFrom:%d %b %Y}-{titleDayQuarterEnd:%d %b %Y}"),
                    chartLabelX='Month',
                    chartLabelY=f'{chartType} Daily Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeQuarterFrom,
                    plotDateTo=datetimeQuarterTo,
                    fileName=fullFilePath,
                    majorLocatorAxisX=mdates.MonthLocator(),
                    minorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    majorFormatterAxisX=mdates.DateFormatter('%b'),
                    minorFormatterAxisX=mdates.DateFormatter('%d')
                )

                chartsGenerated.append({
                    'EnergySource': chartType,
                    'ChartType': chart[2],
                    'Files': [fullFilePath],
                    'Message': f'{chartType} {datetimeQuarterFrom:%d-%m-%Y} to {titleDayQuarterEnd:%d-%m-%Y} consumption. \nTotal quarter {chartType} consumption: {totalConsumptionForInterval[2]:.3f}kWh\n\n#OctopusSmartQuarterCharts\n#Octopus{chartType}QuarterCharts'
                })

                # increase values by three months
                datetimePreviousFrom = datetimeQuarterFrom

                datetimeQuarterFrom = addMonthsToDatetime(datetimeQuarterFrom, 3)
                datetimeQuarterTo = addMonthsToDatetime(datetimeQuarterTo, 3)

                titleDayQuarterEnd = datetimeQuarterTo - datetime.timedelta(days=1)

            updateChartsGenerated(dataAccess, chart[0], datetimePreviousFrom, datetimeQuarterFrom, datetimeQuarterTo)

        elif (chart[2] == 'Yearly'):
            datetimeYearFrom = chart[5]
            datetimeYearTo = chart[6]

            datetimePreviousFrom = datetimeYearFrom
            # N = 1 * 24 * 2

            # while (datetimeYearFrom < lastRecord[5]): # Here to generate chart before end of year
            while (datetimeYearTo < lastRecord[5]):
                fileName = f'{chartType.lower()}-plot-{datetimeYearFrom:%Y}.png'
                # fileName = f'{chartType.lower()}-plot-{datetimeYearFrom:%Y}.svg'
                fullFilePath = os.path.join(dir, 'Images', 'year', fileName)

                args = [chartType, datetimeYearFrom, datetimeYearTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectDailyConsumptionFromRange', args, 'MySql')
                totalConsumptionForInterval = dataAccess.loadData('spDataValues_SelectTotalConsumptionFromRange', args, 'MySql')[0]
                # xList, yList = applyRollingAverage(listOfUse, N)
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeYearFrom:%Y}"),
                    chartLabelX='Month',
                    chartLabelY=f'{chartType} Daily Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeYearFrom,
                    plotDateTo=datetimeYearTo,
                    fileName=fullFilePath,
                    majorLocatorAxisX=mdates.MonthLocator(),
                    minorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    majorFormatterAxisX=mdates.DateFormatter('%b')
                )

                chartsGenerated.append({
                    'EnergySource': chartType,
                    'ChartType': chart[2],
                    'Files': [fullFilePath],
                    'Message': f'{chartType} {datetimeYearFrom:%Y} consumption. \nTotal year {chartType} consumption: {totalConsumptionForInterval[2]:.3f}kWh\n\n#OctopusSmartYearCharts\n#Octopus{chartType}YearCharts'
                })

                # increase values by twelve months
                datetimePreviousFrom = datetimeYearFrom

                datetimeYearFrom = addMonthsToDatetime(datetimeYearFrom, 12)
                datetimeYearTo = addMonthsToDatetime(datetimeYearTo, 12)

            updateChartsGenerated(dataAccess, chart[0], datetimePreviousFrom, datetimeYearFrom, datetimeYearTo)

    print('Finished!')
    return chartsGenerated

def addMonthsToDatetime(datetimeVariable, months):
    year = datetimeVariable.year
    month = datetimeVariable.month
    
    yearsToAdd = months // 12
    monthsToAdd = months % 12
    
    month += monthsToAdd
    year += yearsToAdd

    if (month > 12):
        month -= 12
        year +=1
    
    return datetime.datetime(year, month, 1)

def updateChartsGenerated(dataAccess, chartTrackerId, datetimePreviousFrom, datetimeFrom, datetimeTo):
    # What are passed in as datetimeFrom and datetimeTo are in fact the values 
    # of the next charts to be generated
    datetimeFromNext = datetimeFrom
    datetimeToNext = datetimeTo

    # To get the values of the last chart generated use the datetimePreviousFrom
    # and the fact that the end timeframe is the start timeframe for the next
    # chart.
    datetimeFrom = datetimePreviousFrom
    datetimeTo = datetimeFromNext

    args = [chartTrackerId, datetimeFrom, datetimeTo, datetimeFromNext, datetimeToNext]
    dataAccess.saveData('spChartTracker_UpdateTimePeriods', args, 'MySql')
