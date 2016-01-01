#!/usr/bin/python
import json
import os
import time

def run():
	output = 12 #example
	makeJSON(output)

#get london time
def timenow():
	os.environ['TZ'] = 'Europe/London'
	time.tzset()
	return time.strftime('%Y %m %d %H:%M:%S')

def makeJSON(data):
	jsonContents = {}
	jsonContents["outlierScale"] = data
	jsonContents["date"] = timenow()
	# Writing JSON data
	with open('../public_html/ramm/outliers.json', 'w') as f:
		json.dump(jsonContents, f)


if __name__ == "__main__": 
    run()
