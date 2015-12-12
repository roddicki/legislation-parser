#!/usr/bin/env python
#
# A test to get the frequency of <entry> each day by retrieveing the <published> date for each entry 
# 
import feedparser 
from feedparser import _parse_date as parse_date
import datetime


feed = feedparser.parse('http://www.legislation.gov.uk/new/data.feed')


def frequencyOfLegislation():
	print '\natom feed: http://www.legislation.gov.uk/new/data.feed'
	print 'this atom feed was updated at', feed.entries[0].updated, '\n'
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
	    if frequency[key] == currentDay:
	    	print 'Today, right now, there is a piece of legislation every', float(int(frequency[key]))/24, 'hours\n'


frequencyOfLegislation()
   
 	


