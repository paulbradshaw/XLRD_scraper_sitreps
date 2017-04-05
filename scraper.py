#This is the second pass at a scraper of Excel files. 
#Currently it scrapes all sheets of one spreadsheet, identified by one direct xls URL
#NEED TO ADD: 
#More than one spreadsheet, linked from one webpage URL = 'http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports-2012-13/'

#useful guides at:
#https://scraperwiki.com/docs/python/python_excel_guide/
#http://blog.scraperwiki.com/2011/09/14/scraping-guides-excel-spreadsheets/
#https://scraperwiki.com/docs/python/tutorials/

import scraperwiki
#import xlrd library - documentation at https://secure.simplistix.co.uk/svn/xlrd/trunk/xlrd/doc/xlrd.html
import xlrd

#set a variable for the spreadsheet location
XLS = 'http://webarchive.nationalarchives.gov.uk/20130402145952/http://transparency.dh.gov.uk/files/2012/10/DailySR-Pub-file-WE-11-11-123.xls'
#use the scrape function on that spreadsheet to create a new variable
xlbin = scraperwiki.scrape(XLS)
#use the open_workbook function on that new variable to create another
book = xlrd.open_workbook(file_contents=xlbin)

#the .nsheets method tells us how many sheets 'book' has
print "nsheets result: ", book.nsheets
#we can use that number to initialise a new variable
sheetstotal = book.nsheets
#and then use that variable to create the end value in a range of numbers, called 'sheetsrange'
sheetsrange = range(0,sheetstotal)
#both lines could of course have been combined into one like this:
#sheetsrange = range(0,book.nsheets)

#print "sheetsrange:" followed by that range of numbers:
print "sheetsrange:", sheetsrange

#create a new variable, 'id', set at 0. We'll add one to this every time a loop runs, so we have a unique id for every row of data
id = 0
#now to loop through the 'sheetsrange' variable (a list) and put each item in 'sheetnum'
for sheetnum in sheetsrange:
    print "scraping sheet ", sheetnum
    #use the sheet_by_index method to open the first (0) sheet in variable 'book' - and put it into new variable 'sheet'
    sheet = book.sheet_by_index(sheetnum)
    #use the row_values method and index (1) to grab the second row of 'sheet'

    #and put all cells into the list variable 'title'
    title = sheet.row_values(1)

    #print the string "Title:", followed by the third [2] item (column) in the variable 'title' 
    print "Title:", title[2]
    sheettitle = str(title[2])
    print "sheet.name", sheet.name
    sheetname = sheet.name
    #put cells from the 15th row into 'keys' variable 
    keys = sheet.row_values(14)
    #create an empty dictionary variable, 'record'
    record = {}
    #loop through a range - from the 16th item (15) to a number generated by using the .nrows method on 'sheet' (to find number of rows in that sheet)
    #put each row number in 'rownumber' as you loop
    for rownumber in range(15, sheet.nrows):
        print rownumber
        Name = "no entry"
        record['SHA'] = sheet.row_values(rownumber)[1]
        record['Code'] = sheet.row_values(rownumber)[2]
        record['Name'] = sheet.row_values(rownumber)[3]
        record['date1'] = sheet.row_values(rownumber)[4]
        #some cells don't have a number, but a dash
        #they generate the error: (exceptions.ValueError) could not convert string to float
        #so we convert these into strings - they can always be converted back later
        record['date2'] = str(sheet.row_values(rownumber)[5])
        record['date3'] = str(sheet.row_values(rownumber)[6])
        record['title'] = title[2]
        id+=1
        record['id'] = id
        print "---", record
        scraperwiki.sqlite.save(['id'], record, table_name=sheetname) 
