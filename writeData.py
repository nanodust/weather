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

writeCSVfromDB()
