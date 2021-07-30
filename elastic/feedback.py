import datetime
import hashlib
import random
import time
from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Set Up Argument
#parser = argparse.ArgumentParser(description='Send Feedback Data to DB')
#parser.add_argument('toilet', metavar='toilet', help='Toilet ID')
#args = parser.parse_args()

def switch_name(argument):
    switcher = {
        1: "Terminal 1 East",
        2: "Terminal 1 Central",
        3: "Terminal 1 West",
        4: "Terminal 2 North",
        5: "Terminal 2 Central",
        6: "Terminal 2 South",
        7: "Terminal 3 North",
        8: "Terminal 3 Central",
        9: "Terminal 3 South",
    }

    return switcher.get(argument, "Invalid toilet")

def switch_latitude(argument):
    switcher = {
        1: 53.361641190774804,
        2: 53.36166951867715,
        3: 53.361330606354684,
        4: 53.36810692362481,
        5: 53.367621563682036,
        6: 53.36682234864207,
        7: 53.361553371452516,
        8: 53.36047055608142,
        9: 53.359409685819124,
    }
    
    return switcher.get(argument, "Invalid toilet")

def switch_longitude(argument):
    switcher = {
        1: -2.2754242494352077,
        2: -2.273255726178378,
        3: -2.271727157735771,
        4: -2.2818336286521643,
        5: -2.28050541932391,
        6: -2.2789512559503082,
        7: -2.2678774092812795,
        8: -2.270061785047923,
        9: -2.2704981156678525,
    }
    
    return switcher.get(argument, "Invalid toilet")

while True:

	toilet_id = random.randrange(1, 10)
	toilet_name = switch_name(toilet_id)
	toilet_latitude = switch_latitude(toilet_id)
	toilet_longitude = switch_longitude(toilet_id)

	mood = random.randrange(0,10)

	if mood <= 1:
		rating = random.randrange(0,1)
	elif mood <= 5:
		rating = random.randrange(2,4)
	elif mood <= 10:
		rating = random.randrange(4,6)
        
	timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

	doc = {
	    'toilet_id': toilet_id,
	    'name': toilet_name,
	    "location": { 
            "lat": toilet_latitude,
            "lon": toilet_longitude
          },
	    'timestamp': time.time(),
        "rating": rating
	}

	res = es.index(index="toilets", body=doc)
	print(res['result'])
	
	time.sleep(0.1)

