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

def addMeasurement(measureType, measurement):
        return [measureType.strip(), measurement[0:5].strip(), measurement[5:6].strip(), measurement[6:7].strip(), measurement[7:8].strip()]

def readRow(lineOfData):
    rowData = {}
    rowData["countryCode"] = lineOfData[0:2]
    rowData["stationID"] = lineOfData[0:11]
    rowData["year"] = lineOfData[11:15]
    rowData["month"] = lineOfData[15:17]
    year = rowData["year"]
    month = rowData["month"]

    yearStr = str(year)
    monthStr = str(month)
    # if days.has_key(yearStr)==False:
    #     days[yearStr] = {}
    # if days[yearStr].has_key(monthStr)==False:
    #     days[yearStr][monthStr] = {}
    element = lineOfData[17:21]
    for x in range(0, 31):
        dayOM = x + 1
        offsetStart = (x*8)+21
        offsetEnd = offsetStart + 8
        dayDat = addMeasurement(element, lineOfData[offsetStart:offsetEnd])
        dayStr = str("%02d" % (dayOM,))
        identifier = yearStr+monthStr+dayStr
        if identifier not in days:
            days[identifier] = {'year':year,'month':month,'day':dayOM,'countryCode':rowData["countryCode"],'stationID':rowData["stationID"]}
        days[identifier][dayDat[0]] = int(dayDat[1])
            # days[yearStr][monthStr][day] = {}
            # print dayDat[0],
            # print int(dayDat[1])
        # days[yearStr][monthStr][day][dayDat[0]] = int(dayDat[1])
    # return rowData




with open(csvfile) as fp:
    for cnt, line in enumerate(fp):
       rowDat = readRow(line)

output = csvfile.split('.')[0]
# with open(output+'.csv', 'w') as f:
#     wr = csv.writer(f, quoting=csv.QUOTE_ALL)
#     for l in days:
#         print days[l]
#         # wr.writerow(l.key)
with open(output+'.json', 'w') as f:
    json.dump(days, f, indent=2, sort_keys=True)
    # json.dump(days, f, sort_keys=True)
    print 'Json written to '+output+'.json'

