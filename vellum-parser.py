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

import logging, pprint, urllib, os.path
import xml.etree.ElementTree as ET
#from datetime import datetime
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run():
    # Object to parse legislation data
    legi = LegislationParser()
    # Parse Atom RSS feed
    entries = legi.parsefeed('atomdata.feed')
    # Then grab document data
    for entry in entries:
        # TODO: Check if we already exist in the database as a valid document
        # Load the content from a url or local file
        filename = entry['filename']
        content = legi.graburl(entry)
        logging.info('GrabURL: '+entry['url']+'\n                                Filename: '+entry['filename'])  
        # Parse the document data
        data = legi.parsedoc(content, filename)
        # Save to the database
    # All finished
    logging.info('Finished')

# Class to grab legislation rss feed
class LegislationParser:

    # Initialise the object
    def __init__(self):       
        logging.info("Initialised Atom RSS parser")
 
    # Parse goatskin (Acts of Parliament are written on vellum, made from the goatskin)
    def parsedoc(self, text, filename):
        # TODO: Check we've recieved valid XML
        logging.info("Parse legislation document")    
        try:
            root = ET.fromstring(text)
        except:
            logging.warning("Inavlid xml. Filename: "+filename)
            return None
        ns = '{http://www.legislation.gov.uk/namespaces/metadata}'
        path = './'+ns+'Metadata/'+ns+'SecondaryMetadata/'+ns
        data = { 
            'Year': self.grabxmlattrib(root, path+'Year', 'Value'),
            'Number': self.grabxmlattrib(root, path+'Number', 'Value'),
            'Made': self.grabxmlattrib(root, path+'Made', 'Date'),
            'Laid': self.grabxmlattrib(root, path+'Laid', 'Date'),
            'ComingIntoForce': self.grabxmlattrib(root, path+'ComingIntoForce/'+ns+'DateTime', 'Date')
        }
        logging.info(pprint.pformat(data))

	# Parse the XML feed provided by: www.legislation.gov.uk/new/data.feed
    def parsefeed(self, text):
        logging.info('Parse Atom RSS feed: '+text)
        tree = ET.parse(text)
        root = tree.getroot()
        ns = "{http://www.w3.org/2005/Atom}"
        mns = "{http://www.legislation.gov.uk/namespaces/metadata}"
        data = []
        for entry in root.findall(ns+"entry"):
            # Core data
            myid = self.grabxmltext(entry, ns+'id')
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
            logging.warning('Cannot find attribute: '+attribute+' FOR: '+ref)
            op = None
        return op
    
    def graburl(self, entry):
        # Have we already downloaded this document?
        filepath = entry['filename']
        if os.path.isfile(filepath):
            with open(filepath, 'r') as myfile:
                # Return locally saved content
                return myfile.read()
        # So we havent got a local version, lets download
        url = entry['url']+'ddd'
        f = urllib.urlopen(url)
        if f.code == 200:
            content = f.read()
            # Save the content to a file for speedy access later
            self.writeoutput(filepath, content)
        else:
            logging.warning('Not found. Code:'+str(f.code)+' URL: '+url)
            content = None
        # Check if we have valid xml
        try:
            ET.fromstring(content)
        except:
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
