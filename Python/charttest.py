# Syncronize with mysqlRetrieveTest as that graph is currently slightly ahead
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import csv
import json

# Electricity
data = 'Python/data2electricBoogaloo.csv'
plotColorLine = "#e9f50a"
plotColorFill = "#eff853"
chartLabelX = 'Time of day (h)'
chartLabelY = 'Electricity Consumption (kWh)'

# # Gas
# data = 'Python/data2gasBoogaloo.csv'
# plotColorLine = "#368ee0"
# plotColorFill = "#72afe9"
# chartLabelX = 'Time of day (h)'
# chartLabelY = 'Gas Consumption (kWh)'

chartTitle = '24th Sept 2020'

plotDateFrom = datetime.date(2020, 9, 24)
plotDateTo = plotDateFrom + datetime.timedelta(1)

variable_date_from = datetime.datetime.fromisoformat("2020-09-24 00:00:00")
variable_date_to = datetime.datetime.fromisoformat("2020-09-24 23:30:00")

# ------------------------------- Retrieve data -------------------------------
listOfUse = []
with open(data) as csv_file:
    csv_reader = csv.reader(csv_file)
    
    for row in csv_reader:
        # Datetime is stored as current timezone datetime + offset to UTC
        #  from that timezone

        # This is an attempt to get the datetime + timezone information into
        #  the same datetime python structure but it is so far 
        #  unsuccessful/unnecessary as the datetime stored is in the local time
        #  and the offset would only tell what timezone the datetime measurement
        #  was taken
        # if row[3][0] != "-":
        #     extraChar = "+"
        # else:
        #     extraChar = ""
        # datetimeFrom = datetime.fromisoformat(row[2]+extraChar+row[3])
        # # datetimeFromTimestamp = datetime.fromisoformat("2020-09-23 01:00:00+00:00:00")
        # # print(datetimeFromTimestamp)

        datetimeFrom = datetime.datetime.fromisoformat(row[2])
        datetimeTo = datetime.datetime.fromisoformat(row[4])

        listOfUse.append([int(row[0]), float(row[1]), datetimeFrom, row[3], datetimeTo, row[5]])

# --------------------------------- Plot data----------------------------------
energyUseListPlot = []
timeListPlot = []

for element in listOfUse:
    energyUseListPlot.append(element[1])
    timeListPlot.append(element[2])
    energyUseListPlot.append(element[1])
    timeListPlot.append(element[4])

fig, ax = plt.subplots(figsize=(16,9))

ax.plot(timeListPlot, energyUseListPlot, color=plotColorLine)
ax.fill_between(timeListPlot, energyUseListPlot, color=plotColorFill)

ax.set_xlim(plotDateFrom, plotDateTo)
if (len(energyUseListPlot) > 0):
    ax.set_ylim(0, max(energyUseListPlot)*1.1)

ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
ax.xaxis.set_minor_locator(mdates.HourLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# ax.xaxis.set_minor_formatter()

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

# plt.savefig('plot.svg')
# plt.savefig('plot.png')
plt.show()
plt.close()
