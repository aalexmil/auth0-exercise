#! /usr/bin/env python

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
			
			if checkInDateTime > threeWeeksAgoDateTime:
				print ("Fresh check in, on:", checkInDateTime)
			else:
				print ("Stale check in, on:", checkInDateTime, "User: ", row['Name']) #would be nice to grab the email address from the other CSV


scanInventoryCSVForStaleCheckins()
