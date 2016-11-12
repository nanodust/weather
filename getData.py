import requests
import time
from datetime import date

# DB

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['weather']
data = db['darksky']

#post_id = posts.insert_one(post).inserted_id

key = "97529b523e71d8d51576ce9bbb89a0ce"
baseURL = "https://api.darksky.net/forecast/"
excludeString = "exclude=currently,minutely,hourly,flags"
lat = "42.3601"
lon = "-71.0589"
unixtime = "1420498800"

#build string
#requests.get('https://api.darksky.net/forecast/97529b523e71d8d51576ce9bbb89a0ce/42.3601,-71.0589,1420498800?exclude=currently,minutely,hourly,flags')



def getDataFrom(lat, lon, time):
    
    getURL = baseURL+key+"/"+str(lat)+","+str(lon)+","+str(unixtime)+"?"+excludeString
    print getURL

    r = requests.get(getURL)
    print r.json()
    # write to db
    post_id = data.insert_one(r.json()).inserted_id
#r = 

getDataFrom(42.3601,-71.0589,1420498800)

# data range = 6669





'''
galena / far west IL (42.430426, -90.450439)

waukegan / far east IL (42.466905, -87.797241)


quincy / far west, south (39.932644, -91.285400)

westville / far east, south 40.144108, -87.583008)


>>> -90.450439 + 87.797241
-2.6531980000000033
width / long

>>> 42.430426-39.932644
2.4977819999999937
>>> 
range height / lat
'''

