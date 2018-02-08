""" 
Converts GHCN DLY Data from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ to JSON file structured by Year/Month/Day
Usage python convert_to_json.py stationname.dly
"""


import sys
import json
import datetime
from calendar import monthrange


if len(sys.argv) > 3:
    if sys.argv[1].find('.dly') == -1:
        print "Please specify a .dly station file, a key and a year Range as YYYY-YYYY"
        quit()
else:
    print "Please specify a .dly station file, a key and a year Range as YYYY-YYYY"
    quit()

csvfile = sys.argv[1]
yearInput = map(int, sys.argv[3].split('-'))
yearInputRange = range(yearInput[0], yearInput[1]+1)
valKey = sys.argv[2]

weeksprcp = {}
weeksprcp["years"] = []
rowData = {}
# weeks = []


def addMeasurement(measureType, measurement):
    return [measureType.strip(), measurement[0:5].strip(), measurement[5:6].strip(), measurement[6:7].strip(), measurement[7:8].strip()]


def addToYear(lineOfData):
    year = rowData["year"]
    month = rowData["month"]
    date = datetime.datetime(int(year), int(month), 1)

    currentYearPos = -1
    
    element = lineOfData[17:21]
    monthlength = monthrange(int(year), int(month))[1]

    weeknum = -1

    # Do for every day
    for x in range(0, monthlength):
        dayOM = x + 1
        offsetStart = (x*8)+21
        offsetEnd = offsetStart + 8
        dayDat = addMeasurement(element, lineOfData[offsetStart:offsetEnd])

        #  Just look at asked Values (PRCP for example)
        if dayDat[0] == valKey:
            date = datetime.datetime(int(year), int(month), dayOM)
            yearStr = str(date.isocalendar()[0])
            
            # Look if there is already a year for this current day
            if not any(d["key"] == yearStr for d in weeksprcp['years']):
                weeksprcp["years"].append({'key': yearStr, 'weeks': []})
                weeks = []

            # Save the position of the current year
            for num, yy in enumerate(weeksprcp["years"]):
                if yy["key"] == yearStr:
                    currentYearPos = num

            weeknum = date.isocalendar()[1]
            weeknumStr = str("%02d" % (weeknum,))

            #  Get the weeks list for the current year
            weeks = weeksprcp["years"][currentYearPos]['weeks']

            val = int(dayDat[1])

            # Insert week if it is not there yet
            if next((item for item in weeks if item["key"] == weeknumStr), None) is None:   
                newWeek = {"key": weeknumStr, "value": val}
                weeks.append(newWeek)
            # Add up the week if it is already there
            else:
                (item for item in weeks if item["key"] == weeknumStr).next()[
                    'value'] += val
            
            #  Write the weeks list for the current week, this will be done for every day, because between years days of one week can be in different years 
            weeksprcp["years"][currentYearPos]['weeks'] = weeks


def initDays():
    weeksprcp["stationID"] = rowData["stationID"]
    weeksprcp["countryCode"] = rowData["countryCode"]


def readRow(lineOfData):
    rowData["countryCode"] = lineOfData[0:2]
    rowData["stationID"] = lineOfData[0:11]
    rowData["year"] = lineOfData[11:15]
    rowData["month"] = lineOfData[15:17]
    year = int(rowData["year"])

    initDays()
    if year in yearInputRange:
        addToYear(lineOfData)


with open(csvfile) as fp:
    for cnt, line in enumerate(fp):
        readRow(line)

output = csvfile.split('.')[0]
with open(output+'-'+valKey+'.json', 'w') as f:
    # json.dump(weeksprcp, f, indent=2, sort_keys=True)  # readable version
    json.dump(weeksprcp, f, sort_keys=True)  # tiny version
    print 'Json written to '+output+'-'+valKey+'.json'
