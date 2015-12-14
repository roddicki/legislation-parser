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

# NOTE FROM: http://www.parliament.uk/about/how/laws/acts/
# An Act of Parliament creates a new law or changes an existing law. 
# An Act is a Bill approved by both the House of Commons and the House of Lords 
# and formally agreed to by the reigning monarch (known as Royal Assent). Once 
# implemented, an Act is law and applies to the UK as a whole or to specific 
# areas of the country.

# All data downloaded by this application falls under Crown copyright:
#   Crown copyright information is reproduced with the permission of the 
#   Controller of HMSO and the Queen's Printer for Scotland.

# Dependencies 
import logging, pprint, urllib, os.path
import xml.etree.ElementTree as ET
#from datetime i

# Setup logging: CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run():
    # Object to parse legislation data
    legi = LegislationParser()
    #legi.makehistory()
    # Download and grab the latest legislation
    legi.grablatest()
     # All finished
    logging.info('Finished')

# Class to grab legislation rss feed
class LegislationParser:

    # Initialise the object
    def __init__(self):       
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
            'aosp' : {'type':'primary', 'description':'Acts of the Old Scottish Parliament (1424-1707)'},
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
    
    # Download the list of latest legislation
    def grablatest(self):
        # First download the latest feed
        filepath = 'data/latest.feed'
        f = urllib.urlopen('http://www.legislation.gov.uk/new/data.feed')
        if f.code == 200:
            content = f.read()
            # Save the content to a file for speedy access later
            logging.info('Saving local file:'+filepath+' For: '+url)
            self.writeoutput(filepath, content)
        else:
            logging.warning('Problem with the download. Error code:'+f.code+ ' For: '+url)
        # Now parse the Atom RSS feed
        entries = legi.parsefeed(filepath)
        # Then grab document data
        for entry in entries:
            # Load the content from a url or local file 
            # (checks if we have already downloaded this URL)
            filename = entry['filename']
            content = legi.loadlegislation(entry)
            # Parse the document data
            data = legi.parsedoc(content, filename)
            # Save to the database
         logging.info('Parsed latest RSS feed')

    # Download a full list of legislative documents
    def makehistory(self):
        inc = 5063
        while inc > 0:
            filepath = 'data/doclist/'+str(inc)+'.xml'
            if os.path.isfile(filepath):
                with open(filepath, 'r') as myfile:
                    # Return locally saved content
                    logging.info('Already saved locally: '+filepath)
            else:
                # So we havent got a local version, lets download
                url = "http://www.legislation.gov.uk/1110-2016/data.feed?page="+str(inc)
                f = urllib.urlopen(url)
                if f.code == 200:
                    content = f.read()
                    # Save the content to a file for speedy access later
                    logging.info('Saving local file:'+filepath+' For: '+url)
                    self.writeoutput(filepath, content)
                else:
                    logging.warning('Problem with the download. Error code:'+f.code+ ' For: '+url)
            inc = inc-1
    
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
            'Year': self.grabxmlattrib(root, path+'Year', 'Value'),
            'Number': self.grabxmlattrib(root, path+'Number', 'Value'),
            'Made': self.grabxmlattrib(root, path+'Made', 'Date'),
            'Laid': self.grabxmlattrib(root, path+'Laid', 'Date'),
            'ComingIntoForce': self.grabxmlattrib(root, path+'ComingIntoForce/'+ns+'DateTime', 'Date')
            # TODO: Save statistics
        }
        logging.info(data)
        logging.info('Finished parsing document\n')

	# Parse the XML feed provided by: www.legislation.gov.uk/new/data.feed
    def parsefeed(self, text):
        logging.info('PARSE ATOM RSS FEED')
        tree = ET.parse(text)
        root = tree.getroot()
        ns = "{http://www.w3.org/2005/Atom}"
        mns = "{http://www.legislation.gov.uk/namespaces/metadata}"
        data = []
        for entry in root.findall(ns+"entry"):
            # Core data
            myid = self.grabxmltext(entry, ns+'id')
            logging.info("Found doc: "+myid)
            entry = {
                # Text info
                'id': myid,
                'title': self.grabxmltext(entry, ns+'title'),
                'published': self.grabxmltext(entry, ns+'published'),
                'updated': self.grabxmltext(entry, ns+'updated'),  
                'author': self.grabxmltext(entry, ns+'author'),  
                'summary': self.grabxmltext(entry, ns+'summary'),  
                # Metadata
                'category': self.grabxmlattrib(entry, ns+'category', 'term'),
                'DocumentMainType': self.grabxmlattrib(entry, mns+'DocumentMainType' , 'Value'),    
                'Number': self.grabxmlattrib(entry, mns+'Number', 'Value'),    
                'ISBN': self.grabxmlattrib(entry, mns+'ISBN', 'Value'),    
                'Year': self.grabxmlattrib(entry, mns+'Year', 'Value'), 
                # My additions
                'url':myid+'/data.xml' ,
                'filename': self.genfilename(myid)
            }
            data.append(entry)
        logging.debug(pprint.pformat(entry))
        logging.info('FINSHED PARSING RSS FEED\n')
        return data
    
    def genfilename(self, myid):
        filename = myid.replace('http://www.legislation.gov.uk/id/', '')
        filename = filename.replace('/','-')
        return 'data/xmldocs/'+filename+'.xml'

    def grabxmltext(self, element, ref):
        try:
            op = element.find(ref).text 
        except:
            logging.warning('Cannot find text:'+ref)   
            op = None;
        return op

    def grabxmlattrib(self, element, ref, attribute):
        try:
            op = element.find(ref).attrib[attribute]   
        except (AttributeError, TypeError): 
            logging.warning('Cannot find attribute: '+attribute)
            op = None
        return op
    
    def loadlegislation(self, entry):
        # Have we already downloaded this document?
        filepath = entry['filename']
        if os.path.isfile(filepath):
            with open(filepath, 'r') as myfile:
                # Return locally saved content
                logging.info('LOADED LEGISLATION DOC FROM FILE: '+filepath)
                return myfile.read()
        # So we havent got a local version, lets download
        url = entry['url']
        f = urllib.urlopen(url)
        if f.code == 200:
            content = f.read()
            # Save the content to a file for speedy access later
            logging.info('LOADED LEGISLATION DOC FROM URL: '+url)
            self.writeoutput(filepath, content)
        elif f.code == 404:
            # Save "None" to a local file so we know not to download again
            logging.warning('LEGISLATION DOC NOT FOUND AT URL. Code:'+str(f.code)+' URL: '+url)
            content = None
            self.writeoutput(filepath, content)
        else:
            # Not sure whats going on! Might be an issue with the webaite or the
            # internet connection. DOnt save so file so another attempopot can be made
            logging.warning('LEGISLATION DOC NOT FOUND AT URL. Code:'+str(f.code)+' URL: '+url)
            content = None
        return content

    def writeoutput(self, filepath, content):
        # TODO: EDrror check the write
        logging.info('Writing file: '+filepath)
        f = open(filepath,'w')
        f.write(content)  
        f.close()     

if __name__ == "__main__": 
    run()
