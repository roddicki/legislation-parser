#! /bin/python2
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
