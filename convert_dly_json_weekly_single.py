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
    
    # yearStr = str(year)

# 
    currentYearPos = -1

    # Check if this year already in days, if not add it with empty week array
    

    element = lineOfData[17:21]
    monthlength = monthrange(int(year), int(month))[1]

    weeknum = -1

    for x in range(0, monthlength):
        dayOM = x + 1
        offsetStart = (x*8)+21
        offsetEnd = offsetStart + 8
        dayDat = addMeasurement(element, lineOfData[offsetStart:offsetEnd])

        #  Just look at asked Values
        if dayDat[0] == valKey:
            date = datetime.datetime(int(year), int(month), dayOM)
            yearStr = str(date.isocalendar()[0])
            # print date.strftime("%W")+' - '+date.strftime("%d. %b %Y")
            # print date.strftime("%a") + ' - ' + str(date) + ' - ' + str(date.isocalendar()) + ' - ' + yearStr
            if not any(d["key"] == yearStr for d in weeksprcp['years']):
                weeksprcp["years"].append({'key': yearStr, 'weeks': []})
                # global weeks
                weeks = []

            for num, yy in enumerate(weeksprcp["years"]):
                if yy["key"] == yearStr:
                    currentYearPos = num

            weeknum = date.isocalendar()[1]

            val = int(dayDat[1])

            weeknumStr = str("%02d" % (weeknum,))
            weeks = weeksprcp["years"][currentYearPos]['weeks']
            if next((item for item in weeks if item["key"] == weeknumStr), None) is None:   
                newWeek = {"key": weeknumStr, "value": val}
                weeks.append(newWeek)
            else:
                (item for item in weeks if item["key"] == weeknumStr).next()[
                    'value'] += val

            weeksprcp["years"][currentYearPos]['weeks'] = weeks


# def getWeek(weeks):


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
