import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import csv
import json

# Electricity
data = 'Python/data2electricBoogaloo.csv'
config_color_line = "#e9f50a"
config_color_fill = "#eff853"
chart_ylabel = 'Electricity Consumption (kWh)'


# # Gas
# data = 'Python/data2gasBoogaloo.csv'
# config_color_line = "#368ee0"
# config_color_fill = "#72afe9"
# chart_ylabel = 'Gas Consumption (kWh)'

query_day_from = datetime.date(2020, 9, 24)
query_day_to = query_day_from + datetime.timedelta(1)

variable_date_from = datetime.datetime.fromisoformat("2020-09-24 00:00:00")
variable_date_to = datetime.datetime.fromisoformat("2020-09-24 23:30:00")

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

energyList = []
timeList = []

for element in listOfUse:
    energyList.append(element[1])
    timeList.append(element[4])

x_indexes = np.arange(len(timeList))

fig, ax = plt.subplots()

ax.plot(timeList, energyList, color=config_color_line)
ax.fill_between(timeList, energyList, color=config_color_fill)

# plt.plot(x_indexes, energyList, color='#0000ff', marker='.')

# plt.xticks(ticks=x_indexes, labels=timeList)

ax.set_ylim(0, max(energyList)*1.2)
ax.set_xlim(query_day_from, query_day_to)

hours = mdates.HourLocator()
hours_fmt = mdates.DateFormatter('%H:%M')
# ax.set_xtics(x_indexes)
ax.xaxis.set_major_formatter(hours_fmt)
ax.xaxis.set_minor_locator(hours)

plt.title('24th Sept 2020')
plt.xlabel('Time of day (h)')
plt.ylabel(chart_ylabel)

# plt.legend()

# plt.grid(True)

# plt.savefig('plot.png')

plt.show()