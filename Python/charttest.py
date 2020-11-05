# import matplotlib
import numpy as np
from matplotlib import pyplot, dates
from datetime import datetime
import csv

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

        listOfUse.append([row[0], row[1], datetimeFrom, datetimeTo])

energyList = []
timeList = []

for element in listOfUse:
    energyList.append(float(element[1]))
    timeList.append(element[2])

# datetimeFromTimestamp = datetime.fromisoformat("2020-09-23 01:00:00+00:00:00")
# print(datetimeFromTimestamp)

x_indexes = np.arange(len(timeList))

pyplot.plot(timeList, energyList, color='#babae8')
# pyplot.plot(x_indexes, energyList, color='#0000ff', marker='.')

# pyplot.xticks(ticks=x_indexes, labels=timeList)

ax = pyplot.axes()

xfmt = dates.DateFormatter('%H:%M')
# ax.set_xtics(x_indexes)
ax.xaxis.set_major_formatter(xfmt)

pyplot.title('24th Sept 2020')
pyplot.xlabel('Time of day (h)')
pyplot.ylabel('Energy Consumption (kWh)')

# pyplot.legend()

# pyplot.grid(True)

pyplot.savefig('plot.png')

pyplot.show()
