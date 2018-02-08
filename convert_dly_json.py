""" 
Converts GHCN DLY Data from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ to JSON file structured by Year/Month/Day
Usage python convert_to_json.py stationname.dly YYYY-YYYY
""" 

import sys
import json
from calendar import monthrange

if len(sys.argv) > 2:
    if sys.argv[1].find('.dly')==-1:
        print "Please specify a .dly station file and a year Range as YYYY-YYYY"
        quit()
else:
    print "Please specify a .dly station file and a year Range as YYYY-YYYY"
    quit()

csvfile = sys.argv[1]
yearInput = map(int, sys.argv[2].split('-'))
yearInputRange = range(yearInput[0],yearInput[1]+1)

days = {}
days["years"] = []
rowData = {}


def addMeasurement(measureType, measurement):
        return [measureType.strip(), measurement[0:5].strip(), measurement[5:6].strip(), measurement[6:7].strip(), measurement[7:8].strip()]

def addYear(lineOfData):
    year = rowData["year"]
    month = rowData["month"]
    yearStr = str(year);
    monthStr = str(month);
    currentYearPos = -1
    currentMonthPos = -1
    

    # Check if this year already in days, if not add it with empty month array
    if not any(d["key"] == yearStr for d in days['years']):
        days["years"].append({'key': yearStr, 'months':[]})
        currentYearPos = len(days["years"])-1
    # Check if this month already in currentYear, if not add it with empty days array  
    if not any(d['key'] == monthStr for d in days['years'][currentYearPos]['months']):
        days['years'][currentYearPos]['months'].append({'key': monthStr, 'days':[]})
        currentMonthPos = len(days['years'][currentYearPos]['months'])-1
    element = lineOfData[17:21]
    monthlength =  monthrange(int(year),int(month))[1]
    for x in range(0, monthlength):
        dayOM = x + 1
        offsetStart = (x*8)+21
        offsetEnd = offsetStart + 8
        dayDat = addMeasurement(element, lineOfData[offsetStart:offsetEnd])
        dayStr = str("%02d" % (dayOM,))
        # Check if this day already in currentMonth, if not add day and empty data 
        if not any(d['key'] == dayStr for d in days['years'][currentYearPos]['months'][currentMonthPos]['days']):
            days['years'][currentYearPos]['months'][currentMonthPos]['days'].append({'key': dayStr, 'values':{}})
        # Searches for the right day and appends the current value
        for d in days['years'][currentYearPos]['months'][currentMonthPos]['days']:
            if (d['key'] == dayStr ):
                # d['values'].append({dayDat[0] : int(dayDat[1])})
                d['values'][dayDat[0]] = int(dayDat[1])

def initDays():
    days["stationID"] = rowData["stationID"]
    days["countryCode"] = rowData["countryCode"]

def readRow(lineOfData):
    rowData["countryCode"] = lineOfData[0:2]
    rowData["stationID"] = lineOfData[0:11]
    rowData["year"] = lineOfData[11:15]
    rowData["month"] = lineOfData[15:17]
    year = int(rowData["year"])

    initDays()
    if year in yearInputRange:
        addYear(lineOfData)

with open(csvfile) as fp:
    for cnt, line in enumerate(fp):
       readRow(line)

output = csvfile.split('.')[0]
with open(output+'.json', 'w') as f:
    # json.dump(days, f, indent=2, sort_keys=True) # readable version
    json.dump(days, f, sort_keys=True) # tiny version
    print 'Json written to '+output+'.json'

