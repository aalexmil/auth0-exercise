#! /usr/bin/env python
#	Goal: read inventory.csv from AWS S3, parse ['Last Check-in'] as a DateTime, and compare with a DateTime of three weeks ago. Output friendly result to Slack.
# 	Compatibility: Python 3
# 	Possible improvements: integrate with the Directory CSV file, perform error/null response checking

import csv
import json
import http.client #not included with Python 2.x
from datetime import datetime, timedelta
				
def scanS3InventoryCSVForStaleCheckins():
#	Available rows: 
#	0 = ['Serial Number']
#	1 = ['Name']
#	2 = ['Operating System Version']
#	3 = ['Model']
#	4 = ['FileVault 2 Status']
#	5 = ['Last Enrollment']
#	6 = ['Last Check-in']
	
	conn = http.client.HTTPSConnection("REDACTED-public.s3.ca-central-1.amazonaws.com")
	conn.request("GET", "/inventory.csv")
	res = conn.getresponse()
	receivedData = res.read()
	receivedData = receivedData.decode("utf-8")
	dataToParse = receivedData.splitlines() #splits on newline characters - otherwise it's just a blob
	
	readCSV = csv.reader(dataToParse)
	next(readCSV, None)  # skip the header row
	
	rawTextToSendToSlack = ""
	
	for row in readCSV:
		checkInDateTime = datetime.strptime(row[6], '%m/%d/%y %H:%M') #convert to DateTime, importing month, day, year without century, 24-hour hour, minute
		threeWeeksAgoDateTime = datetime.now() - timedelta(days = 21)
		sinceLastCheckInDateTime = datetime.now() - checkInDateTime
		if checkInDateTime < threeWeeksAgoDateTime:
			rawTextToSendToSlack += "\n" + row[1] + " has a device " + row[0] + " which hasn't checked in for " + str(sinceLastCheckInDateTime.days) + " days"
			
	sendDataToSlack( {'text': rawTextToSendToSlack} )
	


def sendDataToSlack(jsonData):
	
	print("Here's the data to go to Slack:", jsonData)
	
	conn = http.client.HTTPSConnection("hooks.slack.com")
	headers = {'Content-type': 'application/json'}
	dataToSlack = json.dumps(jsonData)
	conn.request("POST", "/services/TQX1ESJBW/BQNRSNAHH/REDACTED", dataToSlack, headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
	


scanS3InventoryCSVForStaleCheckins()
