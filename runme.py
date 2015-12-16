#! /bin/python2
from vellum import LegislationParser


# Object to parse legislation data
legi = LegislationParser()

# Save the latest legislation entries from:
#   http://www.legislation.gov.uk/new/data.feed
legi.grablatest()

# RUN SOME QUERIES ON THE DATABASE
output = "\n"

# Search for published legislation
count = legi.countlegi('published', 2015, 12, 15) 
output = output+"Published Legislation Dec 15 2015: "+str( count )+'\n'

# Search for updated legislation
datefield = 'updated'
count = legi.countlegi('updated', 2015, 12, 15) 
output = output+"Updated Legislation Dec 15 2015: "+str( count )+'\n'

# Search for all published legislation in 2014, 2013
count = legi.countlegi('updated', 2015, None, None)
output = output+"Published Legislation 2014: "+str( count )+'\n'
count = legi.countlegi('updated', 2013, None, None)
output = output+"Published Legislation 2013: "+str( count )+'\n'

# Save output of the search queries to file and print
print('\n'+output)
legi.writeoutput('test.txt', output)


