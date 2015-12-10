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

import xml.etree.ElementTree as ET
from datetime import datetime

# Class to grab legislation rss feed
class LegislationParser:

    def __init__(self, level):
        self.level = level        
        self.debug("Started")
        self.grabatomfeed()
        self.parsexml()
        self.output()
    
    def grabatomfeed(self):
        self.debug("Grabbing atom feed")

    def parsexml(self):
        self.debug('parsing xml')
        tree = ET.parse('atomdata.feed')
        root = tree.getroot()
        #print(root)
        ns = "{http://www.w3.org/2005/Atom}"
        for entry in root.findall(ns+"entry"):
            data = {'id':'','published':''}
            # {http://www.w3.org/2005/Atom}published
            # {http://www.legislation.gov.uk/namespaces/metadata}DocumentMainType
            data['id'] = entry.find(ns+'id').text
            data['title'] = entry.find(ns+'title').text
            data['updated'] = entry.find(ns+'updated').text
            data['published'] = entry.find(ns+'published').text
            data['DocumentMainType'] = entry.find(ns+'published').text

            # data['summary'] = entry.find(ns+'published').text
            print(data)
            #att = str(child.attrib)
    
    def parsepigskin():
        self.debug("Gr")

    def output(self):
        self.debug('output')
        now = str(datetime.now())+"\n" 
        f = open('test.txt','w')
        f.write(now)  
        f.close()     
        
    def debug(self, txt, level='debug'):
        print(txt)
        

if __name__ == "__main__": 
    lp = LegislationParser('debug');
