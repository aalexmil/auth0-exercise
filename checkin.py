#! /usr/bin/env python
#	Goal: read inventory.csv, parse ['Last Check-in'] as a DateTime, and compare with a DateTime of three weeks ago. 
# 	Compatibility: Python 2, Python 3
# 	Possible improvements: integrate with the Directory CSV file

import csv
from datetime import datetime, timedelta


def scanInventoryCSVForStaleCheckins():
#	Available rows: 
#	['Serial Number']
#	['Name']
#	['Operating System Version']
#	['Model']
#	['FileVault 2 Status']
#	['Last Enrollment']
#	['Last Check-in']
	
	with open('inventory.csv') as csvfile:
		csvInputFile = csv.DictReader(csvfile)
		for row in csvInputFile:
			checkInDateTime = datetime.strptime(row['Last Check-in'], '%m/%d/%y %H:%M') #convert to DateTime, importing month, day, year without century, 24-hour hour, minute
			
			threeWeeksAgoDateTime = datetime.now() - timedelta(days = 21) 
			sinceLastCheckInDateTime = datetime.now() - checkInDateTime
			if checkInDateTime < threeWeeksAgoDateTime:
				print (row['Name'], "has a device", row['Serial Number'], "which hasn't checked in for", sinceLastCheckInDateTime.days, "days")


scanInventoryCSVForStaleCheckins()
