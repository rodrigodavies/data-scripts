# A simple reverse geocoding script for working with csv files, based on the Geocoder library.
# Rodrigo Davies

# Change the headers and columns to fit the dataset you're working with.

from pygeocoder import Geocoder
import csv
import sys
from time import sleep
import ConfigParser

# initialize and set proxy
myGeo = Geocoder()
config = ConfigParser.ConfigParser()
config.read('revgeocoder-settings.ini')
proxy = config.get('default', 'proxy')
myGeo.set_proxy(proxy) # read from config file

def cleanid(col):
	clean_string = str(col).split("'")
	return int(clean_string[1])

def cleanGeo(col):
	clean_string = str(col).split("'")
	return float(clean_string[1])

def checkNone(result):
	if result == None:
		result = ''
	return result

def cleanString(result):
    if result == None:
		result = ''
    return str(result.encode('ascii','ignore'))

def revGeo(sourceFile):
	with open(sourceFile, 'rU') as csvfile:
		dataString = ""
		soup = csv.reader(csvfile, delimiter=',')
		row_num = 1
		# row_count = sum(1 for row in soup)
		for row in soup:
			cols = str(row)
			cols = cols.split(',')
			ks_id = cleanid(cols[0])
			(lat, lon) = (cleanGeo(cols[1]), cleanGeo(cols[2]))
			try:
				result = myGeo.reverse_geocode(float(lat),float(lon))
				latlon = str(lat) + "," + str(lon)
				zipcode = checkNone(result[0].postal_code)
				if len(str(zipcode)) == 4:
					zipcode = '0' + zipcode #correcting for five digit zips
				country = cleanString(result[0].country)
				state = cleanString(result[0].state)
				city = cleanString(result[0].city)
			except Exception: # Having some trouble with GeoCoder exception, this is a catch-all 
				(zipcode, country, state, city) = (".", ".", ".", ".")
				print "Exception at: %s - coords: %s"%(row_num,latlon)
			resultString = "%s\t%s\t%s\t%s\t%s\t%s\n"%(ks_id,latlon,zipcode,country,state,city)
			dataString = "%s%s"%(dataString, resultString)
			perc = (float(row_num) / float(20000) * 100)
			donestring = '\r %s Done: (%s) %s %s %s %s'%(perc,row_num,zipcode,country,state,city)
			print donestring, # comma to avoid newline
			sys.stdout.flush()
			row_num += 1
			sleep(0.4)
	filename = "revgeocoded-%s.tsv"%(sourceFile) #add tag to filename
	writeData(dataString, filename)

def writeData(dataString, file):
	headerString = "id\tlatlon\tzip\tcountry\tstate\tcity\n"
	totalString = "%s%s"%(headerString,dataString)
	f = open(file, 'w')
	f.write(totalString)
	f.close()

if __name__ == "__main__":
    # source = sys.argv[1]
    source = 'revgeo-1.csv'
    revGeo(source)