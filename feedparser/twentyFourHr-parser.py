#!/usr/bin/python
#

 
import feedparser 
from feedparser import _parse_date as parse_date
from datetime import date
from datetime import datetime
from time import mktime
import time
import calendar


#these functions retrieve the hourly frequency of legislation
def run():
	#Print the day
	print 'It is',calendar.day_name[date.today().weekday()], '\n======'
	twentyFourHourFrequency()
	#frequencyOfLegislation()

def twentyFourHourFrequency():
	#this function works out the hourly frequency of entries of passed legislation in the last 24hrs of legislative activity 
	#using http://www.legislation.gov.uk/new/data.feed
	#It does this by collecting entries of passed legislation in the last 24 hr period
	#Except if it is a monday - then it collects the number of entries back to & including Friday (72hrs) 
	#Friday is used because no legislation is passed on a wkend and Friday would have been within the last 24hrs of legislative activity
	#On a weekend the hourly frequency will always be 0
	feed = feedparser.parse('http://www.legislation.gov.uk/new/data.feed')
	print 'this atom feed was updated at', feed.updated, '\n'
	entries_in_collection_period = 0
	currentTime = (tuple(time.gmtime()))
	timestamp_currentTime = calendar.timegm(currentTime)
	for x in xrange(0,len(feed.entries)): #loop through all the entries
		print feed.entries[x].title
		timestamp_entryDate = mktime(parse_date(feed.entries[x].published)) #get each entry published date and change to unix format
		print timestamp_entryDate
		print datetime.fromtimestamp(timestamp_entryDate), 'date published'
		hours_old = (timestamp_currentTime - timestamp_entryDate)/ 3600.0
		print hours_old, 'hours old'
		current_weekday = calendar.day_name[date.today().weekday()] #get current weekday name eg Monday
		if current_weekday=='Monday' and hours_old < 72: #if its Monday find entries back to Friday (72hrs)
			entries_in_collection_period += 1
			print 'added to the frequency list\n'
		elif hours_old < 24: #else find entries in the last 24hrs
			entries_in_collection_period += 1
	print 'entries_in_collection_period:', entries_in_collection_period
	hourly_frequency = float(entries_in_collection_period)/24 #calc the hourly frequency of entries
	print 'A piece of legislation was passed every', hourly_frequency, 'hrs in the last 24hrs\n'
	return hourly_frequency






def frequencyOfLegislation():
	#this function works out the hourly frequency of entries of passed legislation in the current day 
	print '\natom feed: http://www.legislation.gov.uk/new/data.feed'
	print 'this atom feed was updated at', feed.updated, '\n'
	storeTheDay = []
	for x in xrange(0,len(feed.entries)): #loop through all the entries
		print feed.entries[x].title
		fullDateTuple = tuple(parse_date(feed.entries[x].published)) #get the published date and cahnge to tuple format
		print 'Day:', fullDateTuple[2], 'th' #print just the day
		storeTheDay.append(fullDateTuple[2]) #add each day to the storeTheDay list - this relies on the date format not changing - not good!
	frequency = dict((i, storeTheDay.count(i)) for i in storeTheDay) #make a dict of the values to get the frequency of the days in the storeTheDay list 
	now = datetime.datetime.now()
	currentDay = "%d" % now.day
	for key in frequency:
	    print '\nOn the', key, 'th there were', frequency[key], 'pieces of legislation'
	    print 'There is a piece of legislation every', float(int(frequency[key]))/24, 'hours\n'
	    if key == currentDay:
	    	print 'Today, right now, there is a piece of legislation every', float(int(frequency[key]))/24, 'hours\n'


   
if __name__ == "__main__":
	run()


