#! /bin/python

from datetime import datetime
now = str(datetime.now())+"\n"; 

print("hello")
f = open('test.txt','w')
f.write(now) # python will convert \n to os.linesep
f.close()
