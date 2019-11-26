import json
import csv
import http.client #not included with Python 2.x
from datetime import datetime, timedelta

def sendDataToSlack(jsonData):
	
	print("Here's the data to go to Slack:", jsonData)
	
	conn = http.client.HTTPSConnection("hooks.slack.com")
	headers = {'Content-type': 'application/json'}
	dataToSlack = json.dumps(jsonData)
	conn.request("POST", "/services/TQX1ESJBW/BQNRSNAHH/REDACTED", dataToSlack, headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))

def lambda_handler(event, context):
	rawTextToSendToSlack = ""
	
	connDirectory = http.client.HTTPSConnection("REDACTED-public.s3.ca-central-1.amazonaws.com")
	connDirectory.request("GET", "/directory.csv")
	resDirectory = connDirectory.getresponse()
	receivedDirectoryData = resDirectory.read()
	receivedDirectoryData = receivedDirectoryData.decode("utf-8")
	receivedDirectoryDataToParse = receivedDirectoryData.splitlines() #splits on newline characters - otherwise it's just a blob
	
	connInventory = http.client.HTTPSConnection("REDACTED-public.s3.ca-central-1.amazonaws.com")
	connInventory.request("GET", "/inventory.csv")
	resInventory = connInventory.getresponse()
	receivedInventoryData = resInventory.read()
	receivedInventoryData = receivedInventoryData.decode("utf-8")
	receivedInventoryDataToParse = receivedInventoryData.splitlines() #splits on newline characters - otherwise it's just a blob
	
	
	
	readDirectoryCSV = csv.reader(receivedDirectoryDataToParse)
	next(readDirectoryCSV, None)  # skip the header row
	
	for row in readDirectoryCSV:
		fullName = row[0] + " " + row[1]			

		readInventoryCSV = csv.reader(receivedInventoryDataToParse)
		next(readInventoryCSV, None)  # skip the header row
	
		result = 0
		for row in readInventoryCSV:
			if fullName == row[1]:
				result += 1
				break
		if result == 0:
			rawTextToSendToSlack += "\n" + fullName + " does not have a device assigned in Jamf."
			
	sendDataToSlack( {'text': rawTextToSendToSlack} )
	return {
        'statusCode': 200
    }