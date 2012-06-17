'''
Created on Jun 6, 2012

@author: kristof
'''
import time
import general_settings
from twython import Twython

twitter = Twython(app_key=general_settings.CONSUMER_KEY, app_secret=general_settings.CONSUMER_SECRET, oauth_token=general_settings.ACCESS_TOKEN, oauth_token_secret=general_settings.ACCESS_SECRET)
for i in (map(lambda x : x+1, range(1000))):
    search_results = twitter.search(q="((abn AND amro) OR (abnamro) OR (abn-amro)) AND (pin OR pas)", page=i, rpp=1000)

    for tweet in search_results["results"]:
        print "Tweet from @%s Date: %s" % (tweet['from_user'].encode('utf-8'),tweet['created_at'])
        print tweet['text'].encode('utf-8'),"\n"
    
    time.sleep(1)
    