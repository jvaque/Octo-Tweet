import matplotlib
from datetime import datetime
import csv

listOfUse = []
with open('data.csv') as csv_file:
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

print(listOfUse)

# datetimeFromTimestamp = datetime.fromisoformat("2020-09-23 01:00:00+00:00:00")
# print(datetimeFromTimestamp)