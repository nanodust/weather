import requests
import time
from datetime import date

# DB

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['weather']
data = db['darksky']


# get from db
#post_id = data.insert_one(r.json()).inserted_id

data.find_one()

# let's get a whole bunch... 10x10 grid. 

