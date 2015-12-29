#! /bin/python2
import time
from vellum import LegislationParser
from make_json import makeJSON


# Global object to parse legislation data
legi = LegislationParser()

def run():
    # Save the latest legislation entries from:
    #   http://www.legislation.gov.uk/new/data.feed
    legi.grablatest()

    # RUN SOME QUERIES ON THE DATABASE
    output = "\n"
    #output += examples()
    frequencytest()

    # Save output of the search queries to file and print
    print('\n'+output)
    legi.writeoutput('test.txt', output)

def frequencytest():
    output = ''
    # Prep query variables and store todays date
    datefield = 'published'
    day = int(time.strftime("%d"))
    month = int(time.strftime("%m"))
    year = int(time.strftime("%Y"))
    types = 'uksi ssi wsi ukci ukdsi sdsi nidsr wdsi'
    # Todays hourly frequency of legislation so far
    perhour = legi.countaveragelegi(1, datefield, year, month, day, types) 
    # Mean hourly frequency of legislation over past 20 years
    yearsback = 20
    result = legi.countaveragelegi(yearsback, datefield, year-1, month, day, types)
    mean = result['mean-perhour']
    standard = result['standard-deviation']
    ranger = 0.1
    top = mean+standard
    top2 = top+ranger
    top3 = top+ranger+ranger
    bot = mean-standard
    bot2 = bot-ranger
    mystr = 'TodayPerHour:{0}  \n{1}YearMean:{2:02.2f} \nStandardDeviation:{3:02.2f} \ntop:{4:02.2f}, \ntop2:{5:02.2f} \ntop3:{6:02.2f} \nbot:{7:02.2f} \nbot2:{8:02.2f}'
    print('\nTODAYS CALCULATION')
    print(mystr.format(perhour, yearsback, mean, standard, top, top2, top3, bot, bot2))
    # Calculate what to do with it!
    outlierValue = 0
    if perhour >= top and perhour <= top2:
        print('outlier:1 - We are just above the standard deviation')
        outlierValue = 1
    elif perhour >= top2 and perhour <= top3:
        print('outlier:2 - We are way above the standard deviation')
        outlierValue = 2
    elif perhour >= top3:
        print('outlier:3 - We are way way above the standard deviation + ranger')
        outlierValue = 3
    elif perhour < bot and perhour > bot2:
        print('outlier:0 - We are just below the standard')
        outlierValue = 0
    elif perhour < bot2:
        print('outlier:0 - We are just substantially below the standard')
        outlierValue = 0
    else:
        print('outlier:0 - Looks like we are between mean and standard deviation')
        outlierValue = 0
    makeJSON(outlierValue)

# Some example queries
def examples():
    output = ''
    # Search for published legislation
    count = legi.countlegi('published', 2015, 12, 15, 'uksi asp') 
    output = output+"Published Legislation Dec 15 2015: "+str( count )+'\n'

    # Search for updated legislation
    count = legi.countlegi('updated', 2015, 12, 15, 'uksi asp') 
    output = output+"Updated Legislation Dec 15 2015: "+str( count )+'\n'

    # Search for all published legislation in 2014, 2013
    count = legi.countlegi('updated', 2015)
    output = output+"Published Legislation 2014: "+str( count )+'\n'
    count = legi.countlegi('updated', 2013)
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
                AND type='asp'
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
    return output 

run()

