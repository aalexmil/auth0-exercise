#! /usr/bin/env python
#	Goal: read directory.csv, combine [first_name] and [last_name], match to Inventory on ['Name'], return ['Serial Number']
#	Compatibility: Python 3
# 	Possible improvements: This is a brute force version; in the future, consider building/scanning an array

import csv
import json
import ssl
import http.client #not included with Python 2.x
import socket

noComputer = 0
usersWithoutTechList = []
def scanForUnassignedComputers():
	
	with open('directory.csv') as csvfile:
		csvInputFile = csv.DictReader(csvfile)
		for row in csvInputFile:
			fullName = row['first_name']  + " " + row['last_name']
			lookForName(fullName)
	rawTextToSendToSlack = "There are " + str(len(usersWithoutTechList)) + " users without assets assigned in Jamf:"
	for i in range( len(usersWithoutTechList) ): 
		rawTextToSendToSlack += '\n'
		rawTextToSendToSlack += usersWithoutTechList[i]
	sendDataToSlack( {'text': rawTextToSendToSlack} )
	

def lookForName(fullName):
	result = 0
	with open('inventory.csv') as csvfile:
		csvInputFile = csv.DictReader(csvfile)
		for row in csvInputFile:
			if fullName == row['Name']:
				result += 1
				break
	if result == 0:
		#print ("No computer found for", fullName)
		global usersWithoutTechList
		usersWithoutTechList.append(fullName)
		


def sendDataToSlack(jsonData):
	
	print("Here's the data to go to Slack:", jsonData)
	
	conn = http.client.HTTPSConnection("hooks.slack.com")
	headers = {'Content-type': 'application/json'}
	dataToSlack = json.dumps(jsonData)
	conn.request("POST", "/services/TQX1ESJBW/BQZASUF7Z/REDACTED", dataToSlack, headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
	


scanForUnassignedComputers()
