# 
# 
# Converts GHCN DLY Data from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ to JSON file structured by Year/Month/Day
# Usage python convert_to_json.py stationname.dly
#
#

import csv
import sys
import json
if len(sys.argv) > 1:
    if sys.argv[1].find('.dly')==-1:
        print "Please specify a .dly station file"
        quit()
else:
    print "Please specify a .dly station file"
    quit()

csvfile = sys.argv[1]
days = {}

def addMeasurement(dayStr, measureType, measurement):
        day = str(dayStr)
        return [measureType.strip(), measurement[0:5].strip(), measurement[5:6].strip(), measurement[6:7].strip(), measurement[7:8].strip()]

def readRow(lineOfData):
    rowData = {}
    rowData["countryCode"] = lineOfData[0:2]
    rowData["stationID"] = lineOfData[0:11]
    rowData["year"] = lineOfData[11:15]
    rowData["month"] = lineOfData[15:17]
    year = rowData["year"]
    month = rowData["month"]
    days["stationID"] = rowData["stationID"]
    days["countryCode"] = rowData["countryCode"]

    if days.has_key(year)==False:
        days[year] = {}
    if days[year].has_key(month)==False:
        days[year][month] = {}
    element = lineOfData[17:21]
    for x in range(0, 31):
        dayOM = x + 1
        offsetStart = (x*8)+21
        offsetEnd = offsetStart + 8
        dayDat = addMeasurement(dayOM, element, lineOfData[offsetStart:offsetEnd])
        day = str("%02d" % (dayOM,))
        if days[year][month].has_key(day)==False:
            days[year][month][day] = {}
        days[year][month][day][dayDat[0]] = int(dayDat[1])
        # days[year][month][day]["stationID"] = rowData["stationID"]
        # days[year][month][day]["countryCode"] = rowData["countryCode"]
        # days[year][month][day]["year"] = int(rowData["year"])
        # days[year][month][day]["month"] = int(rowData["month"])
        # days[year][month][day]["day"] = dayOM
    return rowData




with open(csvfile) as fp:
    for cnt, line in enumerate(fp):
       rowDat = readRow(line)

output = csvfile.split('.')[0]
with open(output+'.json', 'w') as f:
    json.dump(days, f, indent=2, sort_keys=True)
    print 'Json written to '+output+'.json'

