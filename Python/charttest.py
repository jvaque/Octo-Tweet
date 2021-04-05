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

chart_title = '24th Sept 2020'

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

energyUseListDisplay = []
timeListDisplay = []

for element in listOfUse:
    energyUseListDisplay.append(element[1])
    timeListDisplay.append(element[2])
    energyUseListDisplay.append(element[1])
    timeListDisplay.append(element[4])

fig, ax = plt.subplots()

ax.plot(timeListDisplay, energyUseListDisplay, color=config_color_line)
ax.fill_between(timeListDisplay, energyUseListDisplay, color=config_color_fill)

ax.set_xlim(query_day_from, query_day_to)
ax.set_ylim(0, max(energyUseListDisplay)*1.1)

hours = mdates.HourLocator()
hours_fmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hours_fmt)
ax.xaxis.set_minor_locator(hours)

ax.set_xlabel('Time of day (h)')
ax.set_ylabel(chart_ylabel)
ax.set_title(chart_title)

# ax.legend()

# ax.grid()
# ax.grid(axis='y', color='#f5f4d7', linestyle='--')

# plt.savefig('plot.svg')
# plt.savefig('plot.png')

plt.show()