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
    chartsGenerated = {}
    chartsGenerated[chartType] = {}

    args = [chartType]
    lastRecord = dataAccess.loadData('spDataValues_SelectLatestSavedRecord', args, 'MySql')[0]

    args = [chartType, lastRecord[5]]
    chartsToMake = dataAccess.loadData('spChartTracker_SelectChartsToMake', args, 'MySql')

    for chart in chartsToMake:
        if(chart[2] == 'Daily'):
            generatedChartFilenames = []

            # Here we got the last chart made with chart_last_from and chart_last_to
            datetimeDayFrom = chart[5]
            datetimeDayTo = chart[6]
            while (datetimeDayTo < lastRecord[5]):
                fileName = f'{chartType.lower()}-plot-{datetimeDayFrom:%Y-%m-%d}.png'
                # fileName = f'{chartType.lower()}-plot-{datetimeDayFrom:%Y-%m-%d}.svg'

                args = [chartType, datetimeDayFrom, datetimeDayTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectRecordsFromRange', args, 'MySql')
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
                    fileName=(os.path.join(dir, 'Images', 'day', fileName)),
                    majorLocatorAxisX=mdates.HourLocator(interval=3),
                    minorLocatorAxisX=mdates.HourLocator(),
                    majorFormatterAxisX=mdates.DateFormatter('%H:%M')
                )

                generatedChartFilenames.append(fileName)

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

            chartsGenerated[chartType][chart[2]] = generatedChartFilenames

        elif (chart[2] == 'Weekly'):
            generatedChartFilenames = []

            datetimeWeekFrom = chart[5]
            datetimeWeekTo = chart[6]
            titleDayWeekEnd = datetimeWeekFrom + datetime.timedelta(days=6)

            while (datetimeWeekTo < lastRecord[5]):
                fileName = f'{chartType.lower()}-plot-{datetimeWeekFrom:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.png'
                # fileName = f'{chartType.lower()}-plot-{datetimeWeekFrom:%Y-%m-%d}-{titleDayWeekEnd:%Y-%m-%d}.svg'

                args = [chartType, datetimeWeekFrom, datetimeWeekTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectRecordsFromRange', args, 'MySql')
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
                    fileName=(os.path.join(dir, 'Images', 'week', fileName)),
                    majorLocatorAxisX=mdates.DayLocator(),
                    minorLocatorAxisX=mdates.HourLocator(interval=6),
                    majorFormatterAxisX=mdates.DateFormatter('%a %d'),
                    minorFormatterAxisX=mdates.DateFormatter('%H')
                )

                generatedChartFilenames.append(fileName)

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

            chartsGenerated[chartType][chart[2]] = generatedChartFilenames

        elif (chart[2] == 'Monthly'):
            datetimeMonthFrom = chart[5]
            datetimeMonthTo = chart[6]

            datetimePreviousFrom = datetimeMonthFrom

            while (datetimeMonthTo < lastRecord[5]):
                args = [chartType, datetimeMonthFrom, datetimeMonthTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectRecordsFromRange', args, 'MySql')
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
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

                listOfUse = dataAccess.loadData('spDataValues_SelectDailyConsumptionFromRange', args, 'MySql')
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeMonthFrom:%b %Y}"),
                    chartLabelX='Month',
                    chartLabelY=f'{chartType} Daily Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeMonthFrom,
                    plotDateTo=datetimeMonthTo,
                    fileName=(os.path.join(dir, 'Images', 'month', f'{chartType.lower()}-daily-plot-{datetimeMonthFrom:%Y-%m}.png')),
                    # fileName=(os.path.join(dir, 'Images', 'month', f'{chartType.lower()}-daily-plot-{datetimeMonthFrom:%Y-%m}.svg')),
                    majorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    minorLocatorAxisX=mdates.DayLocator(),
                    majorFormatterAxisX=mdates.DateFormatter('%d'),
                    minorFormatterAxisX=mdates.DateFormatter('%d')
                )

                datetimePreviousFrom = datetimeMonthFrom

                datetimeMonthFrom = addMonthsToDatetime(datetimeMonthFrom, 1)
                datetimeMonthTo = addMonthsToDatetime(datetimeMonthTo, 1)

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

            datetimePreviousFrom = datetimeQuaterFrom
            # N = 1 * 24 * 2

            while (datetimeQuaterTo < lastRecord[5]):
                args = [chartType, datetimeQuaterFrom, datetimeQuaterTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectDailyConsumptionFromRange', args, 'MySql')
                # xList, yList = applyRollingAverage(listOfUse, N)
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
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

                datetimeQuaterFrom = addMonthsToDatetime(datetimeQuaterFrom, 3)
                datetimeQuaterTo = addMonthsToDatetime(datetimeQuaterTo, 3)
            
            # save to the charttracker

        elif (chart[2] == 'Yearly'):
            datetimeYearFrom = chart[5]
            datetimeYearTo = chart[6]

            datetimePreviousFrom = datetimeYearFrom
            # N = 1 * 24 * 2

            while (datetimeYearFrom < lastRecord[5]): # Here to generate chart before end of year
            # while (datetimeYearTo < lastRecord[5]):
                args = [chartType, datetimeYearFrom, datetimeYearTo]
                listOfUse = dataAccess.loadData('spDataValues_SelectDailyConsumptionFromRange', args, 'MySql')
                # xList, yList = applyRollingAverage(listOfUse, N)
                xList, yList = GenerateCharts.squareData(listOfUse)

                # Create and save a copy of the montly chart
                GenerateCharts.customChart(
                    valuesX=xList,
                    valuesY=yList,
                    chartTitle=(f"{datetimeYearFrom:%d %b %Y}-{datetimeYearTo:%d %b %Y}"),
                    chartLabelX='Year',
                    chartLabelY=f'{chartType} Daily Consumption (kWh)',
                    plotColorLine=config['Charts'][f'{chartType.lower()}_color_line'],
                    plotColorFill=config['Charts'][f'{chartType.lower()}_color_fill'],
                    plotDateFrom=datetimeYearFrom,
                    plotDateTo=datetimeYearTo,
                    fileName=(os.path.join(dir, 'Images', 'year', f'{chartType.lower()}-plot-{datetimeYearFrom:%Y-%m}.png')),
                    # fileName=(os.path.join(dir, 'Images', 'year', f'{chartType.lower()}-plot-{datetimeYearFrom:%Y-%m}.svg')),
                    majorLocatorAxisX=mdates.MonthLocator(),
                    minorLocatorAxisX=mdates.WeekdayLocator(byweekday=mdates.MO),
                    majorFormatterAxisX=mdates.DateFormatter('%b'),
                    minorFormatterAxisX=mdates.DateFormatter('%d')
                )

                # increase values by three months
                datetimePreviousFrom = datetimeYearFrom

                datetimeYearFrom = addMonthsToDatetime(datetimeYearFrom, 12)
                datetimeYearTo = addMonthsToDatetime(datetimeYearTo, 12)
            
            # save to the charttracker

    print('Finished!')
    print(chartsGenerated)
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