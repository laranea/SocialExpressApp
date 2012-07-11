import time

import redis
import tweetstream
import tweepy
import getopt
import sys

from datetime import datetime

try:
    import simplejson as json
except:
    import json


class FilterRedis(object):
    r = redis.Redis(host='localhost', port=6379)
    num_tweets = 20
    trim_threshold = 100

    def __init__(self, key):
        self.trim_count = 0
        self.key = key


    def push(self, data):
        self.r.lpush(self.key, data)

        self.trim_count += 1
        if self.trim_count >= self.trim_threshold:
            self.r.ltrim(self.key, 0, self.num_tweets)
            self.trim_count = 0


    def tweets(self, limit=15, since=0):
        data = self.r.lrange(self.key, 0, limit - 1)
        return [json.loads(x) for x in data if int(json.loads(x)['received_at']) > since]

class StreamWatcherListener(tweepy.StreamListener):
    fr = FilterRedis()

    def on_status(self, status):
        tweet = status
        #try:
        #    if '@' in tweet.text or not tweet.text.endswith('?'):
        #       return True 
        print repr(tweet.text)
        print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
        self.fr.push(json.dumps( {'id':tweet.id,
                                 'text':tweet.text,
                                 'username':tweet.author.screen_name,
                                 'userid':tweet.author.id,
                                 'name':tweet.author.name,
                                 'profile_image_url':tweet.author.profile_image_url,
                                 'received_at':time.time(),
				                 'geo':tweet.geo
                                 } 
                               )
                    )
        #except:
        # Catch any unicode errors while printing to console
         # and just ignore them to avoid breaking application.
         #   pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'


if __name__ == '__main__':
    
    words = sys.argv[1].split(",")
    key = words.join("_")
    
    fr = FilterRedis(key)


    username = "laranea"
    password = "elleke77"

    auth = tweepy.auth.BasicAuthHandler(username, password)

    stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)
    stream.filter(None, words)

