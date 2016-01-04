#! /bin/python2

# Legislation frequency parser writen for Rod Dickinson: www.roddickinson.net 
# Copyright (C) 2015 Tom Keene | www.theanthillsocial.co.uk
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses

# An Act of Parliament creates a new law or changes an existing law. 
# An Act is a Bill approved by both the House of Commons and the House of Lords 
# and formally agreed to by the reigning monarch (known as Royal Assent). Once 
# implemented, an Act is law and applies to the UK as a whole or to specific 
# areas of the country. [http://www.parliament.uk/about/how/laws/acts]

# All data downloaded by this application falls under Crown copyright:
# Crown copyright information is reproduced with the permission of the 
# Controller of HMSO and the Queen's Printer for Scotland.

# Dependencies 
import logging, math, time, pprint, urllib, os.path, sqlite3, datetime
import xml.etree.ElementTree as ET
from databasebuilder import DatabaseBuilder

# Setup logging: CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def run():
  
    # Object to parse legislation data
    db = "data/db.sqlite3"
    legi = LegislationParser(db)
    
    # Save rss entries of all legislation created since 1200
    # legi.makehistory() 

    # Download and grab the latest legislation entries from:
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
    logging.info('\n'+output)
    legi.writeoutput('test.txt', output)

    # All finished
    logging.info('FINISHED SCRIPT\n')

# Class to grab legislation rss feed
class LegislationParser:

    # Initialise the object
    def __init__(self, db):
        # Inititalise the database structure
 	self.db = db
	self.initdatabase()
        # Return a full list of legislation via:
        #    www.legislation.gov.uk/1110-2016/data.feed?page=5063
        # Where page 5063 is the final page in the list
        #
        # Legislation URIs follow the following structure:
        #   http://www.legislation.gov.uk/{type}/{year}/{number}
        # Where {number} refers to a chapter number
        # Categories of legislation 
        self.legtype = {
            # Primary legislation is mostly 'enacted' 
            'ukpga': {'type':'primary', 'description':'UK Public General Acts'},
            'ukla' : {'type':'primary', 'description':'UK Local Acts 2015-1800'},
            'apgb' : {'type':'primary', 'description':'1800 or older'}, 
            'aep'  : {'type':'primary', 'description':'All very old 1600 or older'},
            'aosp' : {'type':'primary', 'description':'Acts of the Old Scottish Parliament (1424-1707)'},
            'asp' : {'type':'primary', 'description':'Acts of the new Scottish Parliament'},
            'mnia' : {'type':'primary', 'description':'Measures of the Northern Ireland Assembly (1974)'},
            'nia'  : {'type':'primary', 'description':'Acts of the Northern Ireland Assembly 2015-200'},
            'ukcm' : {'type':'primary', 'description':'UK Church Measures'},
            'mwa'  : {'type':'primary', 'description':'Measures of the Welsh Assembly'},   
            # Secondary legislation
            'uksi' : {'type':'secondary', 'description':'UK Statutory Instruments'},
            'ssi'  : {'type':'secondary', 'description':'Scottish Statutory Instruments'},    
            'wsi'  : {'type':'secondary', 'description':'Wales Statutory Instruments 2015-1999'},
            'ukci' : {'type':'secondary', 'description':'UK Church Instruments'},
            'nisi' : {'type':'secondary', 'description':'Northern Ireland Orders in Council 2009-1972'},
            'ukmo' : {'type':'secondary', 'description':'UK Ministerial Orders 2013-1992'},
            # Draft legislation
            'ukdsi': {'type':'draft', 'description':'UK Draft Statutory Instruments 2016-1998'},
            'sdsi' : {'type':'draft', 'description':'Scottish Draft Statutory Instruments 2015-2001'},
            'nidsr': {'type':'draft', 'description':'Northern Ireland Statutory Rules 2015-2000'},
            'nidsi': {'type':'draft', 'description':'Northern Ireland Draft Orders (nothing available)'},
            'wdsi' : {'type':'draft', 'description':'Welsh Draft Statutory Instruments. (nothing available)'}
        }
    
    def initdatabase(self):
        # Create a database structure to store info in
        dbstruct = {
            'legislation':{
                # Core metadata
                'id':'TEXT PRIMARY KEY',
                'type':'TEXT',
                'title':'TEXT',  
                'number':'INTEGER',
                'url':'TEXT unique',
                'filename':'TEXT unique',
                # Published
                'rss_published_year':'INTEGER',                
                'rss_published_month':'INTEGER',
                'rss_published_day':'INTEGER', 
                # Updated
                'rss_updated_year':'INTEGER',                
                'rss_updated_month':'INTEGER',
                'rss_updated_day':'INTEGER',
                # Enacted
                'doc_enacted_year':'INTEGER',                
                'doc_enacted_month':'INTEGER',
                'doc_enacted_day':'INTEGER',
                # Created
                'doc_created_year':'INTEGER',                
                'doc_created_month':'INTEGER',
                'doc_created_day':'INTEGER',
                # Made
                'doc_made_year':'INTEGER',                
                'doc_made_month':'INTEGER',
                'doc_made_day':'INTEGER',
                # Laid
                'doc_laid_year':'INTEGER',                
                'doc_laid_month':'INTEGER',
                'doc_laid_day':'INTEGER'
            }
        }
        # Initialise the database and build it if it doesn't exist
        databasefile = self.db 
        builder = DatabaseBuilder(databasefile, dbstruct) 
        # Connect to the database
        self.db = sqlite3.connect(databasefile)
        self.cursor = self.db.cursor()
    
    # Run query on the database
    def querylegi(self, qry):
        result = self.cursor.execute(qry)  
        return self.cursor.fetchall()  

    # Count legislation within a gievn date range
    def countlegi(self, datefield, year, month=None, day=None, types=None):
        yearstr=daystr=monthstr=typestr=''
        if year!=None:
            yearstr = "rss_"+datefield+"_year="+str(year)+" AND "
        if month!=None:
            monthstr = "rss_"+datefield+"_month="+str(month)+" AND "
        if day!=None:
            daystr = "rss_"+datefield+"_day="+str(day)+" AND "
        if types!=None:
            typesarr = types.split(' ')
            for item in typesarr:
             typestr = typestr+"type='"+item+"' OR "
            typestr = typestr[:-3]            
            typestr = '('+typestr+') AND '
        andstr = yearstr+monthstr+daystr+typestr
        andstr = andstr[:-4]
        qry = "SELECT count(*) FROM legislation WHERE "+andstr
        logging.info(qry)
        result = self.cursor.execute(qry)
        item = self.cursor.fetchone()
        return item[0]
    
    # Count average frequency of legislation for past n years
    def countaveragelegi(self, pastyears, datefield, year, month=None, day=None, types=None):
        op = ''
        # If its todays date calculate hourly average up until current time
        today = time.strftime("%d/%m/%Y") 
	qrydate = '{0}/{1}/{2}'.format(day,month,year)
        hoursinday = 24.0  
        if today == qrydate:
            hoursinday = float(time.strftime("%H")) 
            header = '\nLEGISLATION PUBLISHED IN THE LAST {0} HOURS\n'.format(int(hoursinday))
        else:
            header = '\nAVERAGE "{0}" "{1}" LEGISLATION FOR PAST {2} YEARS FOR THIS DAY {3}/{4}/{5}\n'.format(datefield, types, pastyears, day, month, year)
        total = median = counter = weekends = 0
        # Loop through and make the calculation
        nums = []
        while counter < pastyears:
            weekend = ''
            perhour = ''
            dayofweek = datetime.datetime(year, month, day).weekday()
            count = self.countlegi(datefield, year, month, day, types)   
            if dayofweek == 5 or dayofweek == 6:
                weekend = '[Its the weekend!]'
                weekends = weekends+1
            else:
                count = self.countlegi(datefield, year, month, day, types)   
                total = total + count
                nums.append(count)
            mystr = '{0} legislation {1}/{2}/{3} = {4} {5}'.format(datefield, day, month, year, count, weekend)
            op = op+mystr+'\n'
            counter = counter+1
            year = year-1
        # Calculate mean 
        releventyears  = pastyears-weekends    
        mean = total/releventyears
        hourly = round(mean/hoursinday, 2)
        if hoursinday != 24.00:
            print('{0}{1}TOTAL={2} MEAN(per hour)={3}'.format(header, op, total, hourly))  
            return hourly    
        # Calculate standard deviation of legislation per day
        tot = 0 
        for v in nums:
            n = (v-mean)*(v-mean)
            tot = tot+n
        variance = tot/releventyears
        standard = int(math.sqrt(variance))
        standardhourly = float(standard)/24.00
        #print('total:{} mean:{} variance:{} standard:{}'.format(tot, mean, variance, standard))
        output = '{0}{1}TOTAL={2} RELEVENTYEARS={3} MEAN(per day)={4} MEAN(per hour)={5:02.2f} STANDARDdev(per day)={6} STANDARDdev(per hour)={7:02.2f}'.format(header, op, total, releventyears, mean, hourly, standard, standardhourly)
        print(output)
        result = {}
        result['standard-deviation'] = standardhourly
        result['mean-perhour'] = hourly
        return result
    

    def dbsaveRSSentry(self, entry):
        values = {
            # Core metadata
            'id':entry['id'],
            'type':entry['type'],
            'title':entry['title'],  
            'number':entry['Number'],
            'url':entry['url'],
            'filename':entry['filename'],
            # Published
            'rss_published_year':entry['published_year'],                
            'rss_published_month':entry['published_month'],
            'rss_published_day':entry['published_day'], 
            # Updated
            'rss_updated_year':entry['updated_year'],                
            'rss_updated_month':entry['updated_month'],
            'rss_updated_day':entry['updated_day'] 
        }
        keys = names = c = ''
        for key in values:
            keys = keys+c+':'+key
            names = names+c+key
            c = ', '
        qry = "INSERT OR IGNORE INTO legislation("+names+") VALUES ("+keys+")"
        logging.debug(qry)
        self.cursor.execute(qry, values)
        self.db.commit()

    # Download latest legislation via: www.legislation.gov.uk/new/data.feed
    def grablatest(self):
        # First download the latest feed and save to file
        url = 'http://www.legislation.gov.uk/new/data.feed'
        # Parse the RSS feed and save to the database
        self.parsefeed(url) # Re-download every time

    # Download all legislative documents as RSS feed and save entries to DB
    def makehistory(self):
        inc = 5063
        while inc > 0:
            filepath = 'data/doclist/'+str(inc)+'.xml'
            url = "http://www.legislation.gov.uk/1110-2016/data.feed?page="+str(inc)
            self.parsefeed(url, filepath) # Download and save to local archive
            inc = inc-1
 
    # Download documents refered to within RSS feed entries
    def downloaddocs(self, entries):
        # Then grab document data
        for entry in entries:
            # Download legislation doc data.xml file and parse its contents 
            # content = self.loadlegislation(entry)
            # data = self.parsedoc(content, entry['filename'])
            pass
   
    # Parse goatskin (Acts of Parliament are written on vellum, made from the goatskin)
    def parsedoc(self, text, filename):
        # Check if this text = None (In which case this file wasn't valid so its not worth parsing it)
        if text == 'None':
            logging.info('Content = "None" | No point going on.\n')
            logging.info('Finished parsing document\n')
            return
        # Check we've recieved valid XML
        logging.info("Parse document")    
        try:
            root = ET.fromstring(text)
        except:
            logging.error("Inavlid xml. Filename: "+filename)
            return None
        ns = '{http://www.legislation.gov.uk/namespaces/metadata}'
        path = './'+ns+'Metadata/'+ns+'SecondaryMetadata/'+ns
        # The enacted or made version of legislation reflects the text of the 
        # legislation when it becomes law.
        # - Primary legislation is 'enacted' 
        # - Secondary is 'made'
        # - UK Church Instruments and Ministerial Orders are "created"
        # The enacted version of legislation is not generally available for 
        # legislation prior to 1988. 
        data = { 
            'Type': None,
            'Enacted': None, 
            'Created': None, 
            'Year': self.grabxmlattrib(root, path, 'Year', 'Value'),
            'Number': self.grabxmlattrib(root, path, 'Number', 'Value'),
            'Made': self.grabxmlattrib(root, path, 'Made', 'Date'),
            'Laid': self.grabxmlattrib(root, path, 'Laid', 'Date'),
            'ComingIntoForce': self.grabxmlattrib(root, path+'ComingIntoForce/'+ns, 'DateTime', 'Date')
            # TODO: Save statistics
        }
        logging.info(data)
        logging.info('Finished parsing document\n')

	# Parse the RSS feed & save any new entries to the database
	# If the filepath is defined the rss will be saved/loaded locally
    def parsefeed(self, url, filepath=None):
        # Lets first grab the content of the RSS fee
        logging.info('PARSE ATOM RSS FEED: '+url+' SavedFile: '+str(filepath))
        content = self.grabcontent(url, filepath)
        if content == None: return
        # Now lets do the real work with parsing the atom rss feed
        root = ET.fromstring(content)
        ns = "{http://www.w3.org/2005/Atom}"
        mns = "{http://www.legislation.gov.uk/namespaces/metadata}"
        n = 0
        for entry in root.findall(ns+"entry"):
            # Increment
            n=n+1
            # Core data
            myid = self.grabxmltext(entry, ns, 'id')
            logging.info("Found RSS entry: "+myid)
            entry = {
                # Text info
                'id': myid,
                'title': self.grabxmltext(entry, ns, 'title'),
                'published': self.grabxmltext(entry, ns, 'published'),
                'updated': self.grabxmltext(entry, ns, 'updated'),  
                'author': self.grabxmltext(entry, ns, 'author'),  
                'summary': self.grabxmltext(entry, ns, 'summary'),  
                # Metadata
                'category': self.grabxmlattrib(entry, ns, 'category', 'term'),
                'DocumentMainType': self.grabxmlattrib(entry, mns, 'DocumentMainType' , 'Value'),    
                'Number': self.grabxmlattrib(entry, mns, 'Number', 'Value'),    
                'ISBN': self.grabxmlattrib(entry, mns, 'ISBN', 'Value'),    
                'Year': self.grabxmlattrib(entry, mns, 'Year', 'Value'), 
                # My additions
                'url':myid+'/data.xml' ,
                'filename': self.genfilename(myid),
                'type': self.gentype(myid)   
            }
            # Split out the dates ready to save to the database
            entry = self.splitdate(entry, 'published', entry['published'])
            entry = self.splitdate(entry, 'updated', entry['updated'])
            # Save the entry to the database if it doesn't already exist
            self.dbsaveRSSentry(entry)
            logging.debug(pprint.pformat(entry))
        # Finished parsing!
        logging.info('FOUND '+str(n)+' RSS ENTRIES: Saved new ones to the DB \n')

    def splitdate(self, entry, title, date):
        year=month=day=0
        if date == None:
            date = 'None'
        datelist = date.split('-')
        if len(datelist) == 3:
            year = datelist[0]
            month = datelist[1]
            daylist = datelist[2].split('T')
            day = daylist[0]
        entry[title+'_year'] = year 
        entry[title+'_month'] = month
        entry[title+'_day'] = day 
        return entry

    def genfilename(self, myid):
        filename = myid.replace('http://www.legislation.gov.uk/id/', '')
        filename = filename.replace('/','-')
        return 'data/xmldocs/'+filename+'.xml'

    def gentype(self, myid):
        mytype = myid.replace('http://www.legislation.gov.uk/id/', '')
        mytypelist = mytype.split('/')
        return mytypelist[0]

    def grabxmltext(self, element, path, ref):
        try:
            op = element.find(path+ref).text 
        except:
            logging.warning('Cannot find text:'+ref)   
            op = None;
        return op

    def grabxmlattrib(self, element, path, ref, attribute):
        try:
            op = element.find(path+ref).attrib[attribute]   
        except (AttributeError, TypeError): 
            logging.warning('Cannot find attribute: '+attribute+' For: '+ref)
            op = None
        return op
    
    def grabcontent(self, url, filepath=None):
        # Only load content from file if we are passed a filename
        if filepath != None:
            # Have we already downloaded this document?
            if os.path.isfile(filepath):
                with open(filepath, 'r') as myfile:
                    # Return locally saved content
                    logging.info('Loaded content from file: '+filepath)
                    return myfile.read()
        # We havent got a local version so lets download
        # TODO: Error check internet access
        f = urllib.urlopen(url)
        if f.code == 200:
            # Read the url content
            content = f.read()
            logging.info('Loaded content from: '+url)
        else:
            # Save "None" as we havent found content
            content = None
            logging.warning('Content not found. Code:'+str(f.code)+' URL: '+url)
        # Save the content to a file if load='local'
        if filepath != None:
            self.writeoutput(filepath, content)
        return content

    def writeoutput(self, filepath, content):
        # TODO: Error check the write
        logging.debug('Writing file: '+filepath)
        f = open(filepath,'w')
        f.write(content)  
        f.close()     

if __name__ == "__main__": 
    run()
