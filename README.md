# legislation-parser
Downloads and parses data published by: www.legislation.gov.uk
WARNING: In active development. Will not currently work. 

## Legislation frequency parser writen for Rod Dickinson: www.roddickinson.net 
Copyright (C) 2015 Tom Keene | www.theanthillsocial.co.uk
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses

## Acts of parliment 
An Act of Parliament creates a new law or changes an existing law. 
An Act is a Bill approved by both the House of Commons and the House of Lords  
and formally agreed to by the reigning monarch (known as Royal Assent). Once 
implemented, an Act is law and applies to the UK as a whole or to specific 
areas of the country. From: http://www.parliament.uk/about/how/laws/acts

## Copyrite of data stored in the 'data' directory
All data downloaded by this application falls under Crown copyright:
Crown copyright information is reproduced with the permission of the 
Controller of HMSO and the Queen's Printer for Scotland.

## Usage
Download and run an example which saves the latest legislation to the database: 

    $ ./run.py

run.py also outputs some example search queries:

    Published Legislation Dec 15 2015: 10
    Updated Legislation Dec 15 2015: 13

    Published Legislation 2014: 16445
    Published Legislation 2013: 12124

    Published legislation from 1st Dec to 15th Dec 2015:131
    Published legislation from 1st Dec to 15th Dec 2014:175
    Published legislation from 1st Dec to 15th Dec 2013:158

    Published legislation 15th Dec 2015:10
    Published legislation 15th Dec 2014:21
    Published legislation 15th Dec 2013:0
    Published legislation 15th Dec 2012:0
    Published legislation 15th Dec 2011:17
    Published legislation 15th Dec 2010:26
    Published legislation 15th Dec 2009:25
    Published legislation 15th Dec 2008:15
    Published legislation 15th Dec 2007:1
    Published legislation 15th Dec 2006:4
    Published legislation 15th Dec 2005:8

