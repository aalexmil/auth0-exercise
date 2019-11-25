#! /usr/bin/env python
#	Goal: read directory.csv, combine [first_name] and [last_name], match to Inventory on ['Name'], return ['Serial Number']
#	Compatibility: Python 2, Python 3
# 	Possible improvements: This is a brute force version; in the future, consider building/scanning an array

import csv

noComputer = 0
def scanForUnassignedComputers():
	
	with open('directory.csv') as csvfile:
		csvInputFile = csv.DictReader(csvfile)
		for row in csvInputFile:
			fullName = row['first_name']  + " " + row['last_name']
			#print ("\nMy name is", fullName)
			lookForName(fullName)
			

def lookForName(fullName):
	#print ("We should look for", fullName)
	result = 0
	with open('inventory.csv') as csvfile:
		csvInputFile = csv.DictReader(csvfile)
		for row in csvInputFile:
			if fullName == row['Name']:
				#print ("We have a match!", row['Serial Number'])
				result += 1
				break
	if result == 0:
		print ("No computer found for", fullName)
		global noComputer
		noComputer += 1
		print ("There are", noComputer, "people that don't have computers.")


scanForUnassignedComputers()
