# import matplotlib
from matplotlib import pyplot, dates
from datetime import datetime
import csv

listOfUse = []
with open('data2electricBoogaloo.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    for row in csv_reader:
        # Test to see if the datetime is in a timezone before UTC
        #  (not really applicable for my use case but thought it would be nice to
        #  cover all edge cases)
        if row[3][0] != "-":
            extraChar = "+"
        else:
            extraChar = ""
        datetimeFrom = datetime.fromisoformat(row[2]+extraChar+row[3])

        if row[5][0] != "-":
            extraChar = "+"
        else:
            extraChar = ""
        datetimeTo = datetime.fromisoformat(row[4]+extraChar+row[5])

        listOfUse.append([row[0], row[1], datetimeFrom, datetimeTo])

energyList = []
counterList = []

for element in listOfUse:
    energyList.append(float(element[1]))
    counterList.append(dates.date2num(element[2]))

# datetimeFromTimestamp = datetime.fromisoformat("2020-09-23 01:00:00+00:00:00")
# print(datetimeFromTimestamp)

pyplot.bar(counterList, energyList, color='#444444')
pyplot.plot(counterList, energyList, color='#0000ff', marker='.')

pyplot.xlabel('Time of day (h)')
pyplot.ylabel('Energy Consumption (kWh)')
pyplot.title('24th Sept 2020')

# pyplot.legend()

pyplot.grid(True)

pyplot.savefig('plot.png')

pyplot.show()
