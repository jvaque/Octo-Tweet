import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import csv
import json

# Retrieve values from config file
with open('appsettings.json', 'r') as f:
    config = json.load(f)

listOfUse = []
with open('data2electricBoogaloo.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    for row in csv_reader:
        # Datetime is stored as current timezone datetime + offset to UTC
        #  from that timezone

        ## No need for taing into acount the offset because the datetime is in local time
        ##  offset only tells what timezone the datetime was taken
        # if row[3][0] != "-":
        #     extraChar = "+"
        # else:
        #     extraChar = ""
        # datetimeFrom = datetime.fromisoformat(row[2]+extraChar+row[3])
        datetimeFrom = datetime.fromisoformat(row[2])

        # if row[5][0] != "-":
        #     extraChar = "+"
        # else:
        #     extraChar = ""
        # datetimeTo = datetime.fromisoformat(row[4]+extraChar+row[5])
        datetimeTo = datetime.fromisoformat(row[4])

        listOfUse.append([row[0], float(row[1]), datetimeFrom, datetimeTo])

energyList = []
timeList = []

for element in listOfUse:
    energyList.append(element[1])
    timeList.append(element[2])

# datetimeFromTimestamp = datetime.fromisoformat("2020-09-23 01:00:00+00:00:00")
# print(datetimeFromTimestamp)

x_indexes = np.arange(len(timeList))

plt.plot(timeList, energyList, color=config['Charts']['electricity_color_line'])
plt.fill_between(timeList, energyList, color=config['Charts']['electricity_color_fill'])

# plt.plot(x_indexes, energyList, color='#0000ff', marker='.')

# plt.xticks(ticks=x_indexes, labels=timeList)

ax = plt.axes()

hours = mdates.HourLocator()
hours_fmt = mdates.DateFormatter('%H:%M')
# ax.set_xtics(x_indexes)
ax.xaxis.set_major_formatter(hours_fmt)
ax.xaxis.set_minor_locator(hours)

plt.title('24th Sept 2020')
plt.xlabel('Time of day (h)')
plt.ylabel('Energy Consumption (kWh)')

# plt.legend()

# plt.grid(True)

plt.savefig('plot.png')

plt.show()



# ---------------------------------
listOfUse = []
with open('data2gasBoogaloo.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    for row in csv_reader:
        # Datetime is stored as current timezone datetime + offset to UTC
        #  from that timezone

        ## No need for taing into acount the offset because the datetime is in local time
        ##  offset only tells what timezone the datetime was taken
        # if row[3][0] != "-":
        #     extraChar = "+"
        # else:
        #     extraChar = ""
        # datetimeFrom = datetime.fromisoformat(row[2]+extraChar+row[3])
        datetimeFrom = datetime.fromisoformat(row[2])

        # if row[5][0] != "-":
        #     extraChar = "+"
        # else:
        #     extraChar = ""
        # datetimeTo = datetime.fromisoformat(row[4]+extraChar+row[5])
        datetimeTo = datetime.fromisoformat(row[4])

        listOfUse.append([row[0], float(row[1]), datetimeFrom, datetimeTo])

gasList = []
timeList = []

for element in listOfUse:
    gasList.append(element[1])
    timeList.append(element[2])

# datetimeFromTimestamp = datetime.fromisoformat("2020-09-23 01:00:00+00:00:00")
# print(datetimeFromTimestamp)

x_indexes = np.arange(len(timeList))

plt.plot(timeList, gasList, color=config['Charts']['gas_color_line'])
plt.fill_between(timeList, gasList, color=config['Charts']['gas_color_fill'])

# plt.plot(x_indexes, energyList, color='#0000ff', marker='.')

# plt.xticks(ticks=x_indexes, labels=timeList)

ax = plt.axes()

hours = mdates.HourLocator()
hours_fmt = mdates.DateFormatter('%H:%M')
# ax.set_xtics(x_indexes)
ax.xaxis.set_major_formatter(hours_fmt)
ax.xaxis.set_minor_locator(hours)

plt.title('24th Sept 2020')
plt.xlabel('Time of day (h)')
plt.ylabel('Gas Consumption (kWh)')

# plt.legend()

# plt.grid(True)

plt.savefig('plot2.png')

plt.show()