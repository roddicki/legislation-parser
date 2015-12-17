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

# Construct our own query from scratch
dec_output = ''
year = 2015
while year>=2013:
    rowstr = ''
    query = '''SELECT count(*) FROM legislation 
            WHERE rss_published_day<16 
            AND rss_published_year='''+str(year)+'''
            AND rss_published_month=12
            ''' 
    legi.cursor.execute(query)
    item = legi.cursor.fetchone()  
    count = str(item[0])
    dec_output = dec_output+"\nPublished legislation from 1st Dec to 15th Dec "+str(year)+":"+count
    year = year-1
output = output+'\n'+dec_output+'\n'

# Construct another query from scratch
dec_output = ''
year = 2015
while year>=2005:
    rowstr = ''
    query = '''SELECT count(*) FROM legislation 
            WHERE rss_published_day=15 
            AND rss_published_year='''+str(year)+'''
            AND rss_published_month=12
            ''' 
    legi.cursor.execute(query)
    item = legi.cursor.fetchone()  
    count = str(item[0])
    dec_output = dec_output+"\nPublished legislation 15th Dec "+str(year)+":"+count
    year = year-1
output = output+dec_output


# Save output of the search queries to file and print
print('\n'+output)
legi.writeoutput('test.txt', output)


