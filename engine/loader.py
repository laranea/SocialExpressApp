
__author__ = 'kristof.leroux@gmail.com'

import general_settings
import tweepy
from tweepy.streaming import StreamListener

def main():
  auth1 = tweepy.auth.OAuthHandler(general_settings.ACCESS_SECRET,general_settings.CONSUMER_SECRET)
  auth1.set_access_token(general_settings.ACCESS_TOKEN,general_settings.ACCESS_SECRET)
  api = tweepy.API(auth1)

  l = StreamListener()
  streamer = tweepy.Stream(auth=auth1, listener=l, timeout=10000 )
  setTerms = ['vodafone']
  #streamer.filter(None,setTerms)
  streamer.sample()

if __name__ == "__main__":
    main()
