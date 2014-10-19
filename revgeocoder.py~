# A simple reverse geocoding script for working with csv files, based on the Geocoder library.
# Rodrigo Davies

# Change the headers and columns to fit the dataset you're working with.

from pygeocoder import Geocoder
import csv
import sys
from time import sleep

# initialize and set proxy
myGeo = Geocoder()
myGeo.set_proxy('us.proxymesh.com:31280') # fill in if you're using one

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
		for row in soup:
			cols = str(row)
			cols = cols.split(',')
			ks_id = cleanid(cols[0])
			lat = cleanGeo(cols[1])
			lon = cleanGeo(cols[2])
			try:
				result = myGeo.reverse_geocode(float(lat),float(lon))
				latlon = str(lat) + "," + str(lon)
				zipcode = checkNone(result[0].postal_code)
				if len(str(zipcode)) == 4:
					zipcode = '0' + zipcode #correcting for five digit zips
				country = cleanString(result[0].country)
				state = cleanString(result[0].state)
				city = cleanString(result[0].city)
			except GeocoderError:
				(zipcode, country, state, city) = (".", ".", ".", ".")
			resultString = "%s\t%s\t%s\t%s\t%s\t%s\n"%(ks_id,latlon,zipcode,country,state,city)
			dataString = "%s%s"%(dataString, resultString)
			print "Done: (" + str(row_num) +") " + str(zipcode) + " " + str(country) + " " + str(state) + " " + str(city)
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
    sources = ['revgeo-1.csv', 'revgeo-2.csv', 'revgeo-3.csv']
    for i in sources:
    	revGeo(i)