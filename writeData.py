#!/bin/env python
import requests
import time
from datetime import date
from datetime import datetime, timedelta
import json, ast

import csv

# config
import os
import sys
import commands
import ConfigParser
config = ConfigParser.RawConfigParser()
configFile = os.path.dirname(os.path.abspath(__file__))+'/config'
config.readfp(open(configFile))


# DB
from pymongo import MongoClient
from pymongo import MongoClient
client = MongoClient(config.get("data","host"), int(config.get("data","port")))
db = client[config.get("data","db")]
data = db[config.get("data","collection")]

# defaults

lat = "42.3601"
lon = "-71.0589"

# get from db
#post_id = data.insert_one(r.json()).inserted_id

print data.find_one()['daily']['data'][0].keys()

# let's get a whole bunch... 10x10 grid. 

# we're going to assume the only content of the database is a single run of 'getData'

#that is, we're not doing any time selection or lat/long filtering or anything. 
#we're just loading the entire collection into memory
#you've been warned :)

print 'finding all'

# open file

def writeCSVfromDB():
    with open('output_file.csv', 'wb') as outfile:
        #write header
        fieldNames = data.find_one()['daily']['data'][0].keys()
        fieldNames.insert(0,"latitude")
        fieldNames.insert(0,"longitude")
        fieldNames.insert(0,"date")
        outFileWriter = csv.DictWriter(outfile, extrasaction='ignore', fieldnames=fieldNames)  
        outFileWriter.writeheader()
        # loop through 
        for i,d in enumerate(data.find()):
            print i
            # de-serialize json to CSV row
            row = ast.literal_eval(json.dumps(d['daily']['data'][0]))
            #row = d['daily']['data'][0].encode('utf-8').strip()
            row.update(d)
            date = datetime.fromtimestamp(row['time']).strftime('%m/%d/%Y')
            row.update({'date':date})
            outFileWriter.writerow(row)
            #outFileWriter.flush()

### comment in to run
#writeCSVfromDB()

def writeElevationToMongo():
    for i,d in enumerate(data.find()):
        print i
        print d['_id']
        h = getElevation(lat,long)
        d.update({'elevation':h})
        data.save(d)
        #update d w/ {'elevation':h}
        #d.update
        print "updated record"
        #if i > 5:
        #    break
        
# mycollection.update({'_id':mongo_id}, {"$set": post}, upsert=False)

# get elevation

    # let's get elevation from lat lon
    # then use it to update items in the existing collection
    # perhpas multiprocess 

def getElevation(lat, lon):
    key = "97529b523e71d8d51576ce9bbb89a0ce"
    baseURL = "https://maps.googleapis.com/maps/api/elevation/json?locations="
    excludeString = "exclude=currently,minutely,hourly,flags"
    lat = "42.3601"
    lon = "-71.0589"
    gkey = "AIzaSyBcq1h9jN7YsphDV_QQVlirwsoGy3d6EGk"
    unixtime = "1420498800"
    #getURL = baseURL+key+"/"+str(lat)+","+str(lat)+","+str(time)+"?"+excludeString
    
    getURL = "https://maps.googleapis.com/maps/api/elevation/json?locations=%s,%s&key=%s" % (lat, lon, gkey)
    
    print getURL

    r = requests.get(getURL)
    
    
    elevation = r.json()['results'][0]['elevation']
    print elevation 
    return elevation 
    # write to db
    #post_id = data.insert_one(r.json()).inserted_id
    #print("written to db")

#getElevation(lat, lon)

writeElevationToMongo()
