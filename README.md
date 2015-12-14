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
Download an run with: 

    $ vellum-parser.py

When the application runs it will:

    1. Grab the latest legislative updates from: www.legislation.gov.uk/new/data.feed".
    2. Download and store each referenced legislative document.
    3. Parse id, titles and dates from these documents.
    4. Store this data in an sqlite database.
