# -*- coding: utf-8 -*-
'''
Created on Jul 17, 2012

@author: kristof
'''

import operator
import time
import datetime
import general_settings
from twython import Twython
from klout import KloutInfluence
import tweeql.extras.sentiment
import tweeql.extras.sentiment.analysis
from pkg_resources import resource_filename
from dateutil import parser
import itertools
from pygeocoder import Geocoder
import language
import urllib
from collections import defaultdict
import ordereddict

import gzip
import math
import re
import os
import pickle
import sys

import json
import numpy as np
import pytz
'''
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
'''

from nltk import word_tokenize, sent_tokenize, corpus

import getopt
import unicodedata

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


DEBUG = True
REALTIME = False


MAIN_KEYWORD = u"Senseo"
COMPETITOR1_KEYWORD = u"Saeco"

MAIN_ENTERPRISE =  'PhilipsNL'
MAIN_LOCATION = 'Amsterdam'

MAIN_LANGUAGE = 'nl'
MAIN_COUNTRY = 'The Netherlands'
MAIN_SCREEN_NAME_LIST = ['PhilipsNL', 'PhilipsCare_NL']

MAIL_TO_LIST = ['kristof.leroux@gmail.com']

SEARCH_PAGES = 10
SEARCH_RPP = 100

begin_date = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=7) 
end_date = datetime.datetime.now(pytz.UTC) 

try:
    opts, args = getopt.getopt(sys.argv[1:], "drv", ["help", "main_keyword=", "competitor1_keyword=", "competitor2_keyword=", "main_enterprise=", "main_location=", "main_language=", "main-country=", "main_screen_name_list=", "mail_to_list=" ])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    #usage()
    sys.exit(2)
print args
output = None
verbose = False
for arg in args:
    o, a = arg.split("=")
    if o == "-r":
        REALTIME = True
    elif o == "-d":
        DEBUG = True
    elif o  == "main_keyword":
        MAIN_KEYWORD = a
    elif o == "competitor1_keyword":
        COMPETITOR1_KEYWORD = a
    elif o == "competitor2_keyword":
        COMPETITOR2_KEYWORD = a
    elif o == "main_enterprise":
        MAIN_ENTERPRISE = a
    elif o == "main_location":
        MAIN_LOCATION = a
    elif o == "main_language":
        MAIN_LANGUAGE = a
    elif o == "main_country":
        MAIN_COUNTRY = a
    elif o == "main_screen_name_list":
        MAIN_SCREEN_NAME_LIST = a
    elif o == "mail_to_list":
        MAIL_TO_LIST = a
    else:
        print o, a
        assert False, "unhandled option"

#REPORT1
import report

report = report.Report()
m_data = []
competitor1_data = []
competitor2_data = []

tweet_list = []
tweet_list2 = []
tweet_list3 = []

#init sentiment analysis
classifier = None
classinfo = None
analysis = tweeql.extras.sentiment.analysis
fname = resource_filename(tweeql.extras.sentiment.__name__, 'sentiment.pkl.gz')
fp = gzip.open(fname)
classifier_dict = pickle.load(fp)
fp.close()

classifier = classifier_dict['classifier']
classinfo = { classifier_dict['pos_label'] :
                          { 'cutoff': classifier_dict['pos_cutoff'],
                            'value' : 1.0/classifier_dict['pos_recall'] },
                        classifier_dict['neg_label'] :
                          { 'cutoff': classifier_dict['neg_cutoff'],
                            'value': -1.0/classifier_dict['neg_recall'] }
                      }

def sentiment(text):
    global classinfo

    words = analysis.words_in_tweet(text)
    features = analysis.word_feats(words)
    dist = classifier.prob_classify(features)
    retval = 0
    maxlabel = dist.max()
    classinf = classinfo[maxlabel]
    if dist.prob(maxlabel) > classinf['cutoff']:
        retval = classinf['value']

    return retval

#TODO: real-time
# search keywords
search_result = []
twitter = Twython(app_key=general_settings.CONSUMER_KEY, app_secret=general_settings.CONSUMER_SECRET, oauth_token=general_settings.ACCESS_TOKEN, oauth_token_secret=general_settings.ACCESS_SECRET)
for i in (map(lambda x : x+1, range(SEARCH_PAGES))):
        #try:
        print "Searching tweets page %i" % i
        # TODO: country language
        search_results = twitter.search(q=MAIN_KEYWORD, page=i, rpp=SEARCH_RPP)
        #except:
        #    pass

        print "Indexing tweets page %i" % i
        for tweet in search_results["results"]:
            print tweet
            tweet_data = {}
            print "Tweet from @%s Date: %s" % (tweet['from_user'].encode('utf-8'),tweet['created_at'])
            #print tweet['text'].encode('utf-8'),"\n"
            tweet_data['text'] = unicode(tweet['text'])
            tweet_data['username'] = tweet['from_user'].encode('utf-8')
            tweet_data['created_at'] = parser.parse(tweet['created_at'])
            
            #if tweet_data['created_at'] > begin_date:
            #    begin_date = tweet_data['created_at']
                
            #if tweet_data['created_at'] < end_date:
            #    end_date = tweet_data['created_at']
            #===================================================================
            # klout = KloutInfluence(tweet['from_user'].encode('utf-8'))
            # try:
            #    tweet_data['influence'] = klout.score()
            #    tweet_data['influences'] =  klout.influences()
            #    tweet_data['influence_topics'] = klout.topics()
            # except:
            #    tweet_data['influence'] = 0
            #    tweet_data['influence_topics'] = {}
            #===================================================================
            tweet_data['influence'] = 0
            tweet_data['sentiment'] = sentiment(tweet['text'])
            tweet_data['ws'] = 0
            tweet_data['hour_string'] = "00:00"
            #geo
            if tweet['geo']:
                print tweet['geo']
                tweet_data['geo'] = tweet['geo']
                try:
                    results = Geocoder.reverse_geocode(tweet_data['geo']['coordinates'][0], tweet_data['geo']['coordinates'][1])
                    tweet_data['country'] = results[0].country
                    tweet_data['city'] = results[0].locality
                    tweet_data['postalcode'] = results[0].postal_code
    
                    print results[0]
                except:
                    tweet_data['geo'] = None
                    tweet_data['country'] = None

            else:
                tweet_data['geo'] = None
                tweet_data['country'] = None

            #gender
            #avatar
            try:
                tweet_data['avatar'] = urllib.urlretrieve(tweet['profile_image_url_https'])
            except:
                tweet_data['avatar'] = (tweet['profile_image_url_https'])
            #number, save and use

            #language
            #ld = language.LangDetect()
            #tweet_data['lang'] = ld.detect(tweet_data['text'])
            tweet_data['lang'] = tweet['iso_language_code']
            print tweet_data['lang']

            #filter out retweets
            if (MAIN_COUNTRY == tweet_data['country']) or (tweet_data['lang'] == MAIN_LANGUAGE) and (tweet_data['username'] not in MAIN_SCREEN_NAME_LIST) and (tweet_data['text'] not in tweet_list):
                m_data.append(tweet_data)

            if tweet_data['text'] not in tweet_list:
                tweet_list.append(tweet_data['text'])

main_data = sorted(m_data, key=lambda k: k['created_at'])
report.spike_keyword = MAIN_KEYWORD
report.spike_location = MAIN_COUNTRY


if COMPETITOR1_KEYWORD:

    for i in (map(lambda x : x+1, range(SEARCH_PAGES))):
            try:
                print "Searching tweets page %i" % i
                # TODO: country language
                search_results = twitter.search(q=COMPETITOR1_KEYWORD, page=i, rpp=SEARCH_RPP)
            except:
                pass

            print "Indexing tweets page %i" % i
            for tweet in search_results["results"]:
                print tweet
                tweet_data = {}
                print "Tweet from @%s Date: %s" % (tweet['from_user'].encode('utf-8'),tweet['created_at'])
                #print tweet['text'].encode('utf-8'),"\n"
                tweet_data['text'] = unicode(tweet['text'])
                tweet_data['username'] = tweet['from_user']
                tweet_data['created_at'] = parser.parse(tweet['created_at'])
                #===================================================================
                # klout = KloutInfluence(tweet['from_user'].encode('utf-8'))
                # try:
                #    tweet_data['influence'] = klout.score()
                #    tweet_data['influences'] =  klout.influences()
                #    tweet_data['influence_topics'] = klout.topics()
                # except:
                #    tweet_data['influence'] = 0
                #    tweet_data['influence_topics'] = {}
                #===================================================================
                tweet_data['influence'] = 0
                tweet_data['sentiment'] = sentiment(tweet['text'])
                tweet_data['ws'] = 0
                tweet_data['hour_string'] = "00:00"
                #geo
                if tweet['geo']:
                    print tweet['geo']
                    tweet_data['geo'] = tweet['geo']
                    results = Geocoder.reverse_geocode(tweet_data['geo']['coordinates'][0], tweet_data['geo']['coordinates'][1])
                    tweet_data['country'] = results[0].country
                    tweet_data['city'] = results[0].locality
                    tweet_data['postalcode'] = results[0].postal_code

                    print results[0]
                else:
                    tweet_data['geo'] = None
                    tweet_data['country'] = None

                #gender
                #avatar
                try:
                    tweet_data['avatar'] = urllib.urlretrieve(tweet['profile_image_url_https'])
                except:
                    tweet_data['avatar'] = (tweet['profile_image_url_https'])
                print tweet_data['avatar']
                #language
                #ld = language.LangDetect()
                #tweet_data['lang'] = ld.detect(tweet_data['text'])
                tweet_data['lang'] = tweet['iso_language_code']
                print tweet_data['lang']

                #filter out retweets
                if (MAIN_COUNTRY == tweet_data['country']) or (tweet_data['lang'] == MAIN_LANGUAGE) and (tweet_data['username'] not in MAIN_SCREEN_NAME_LIST) and (tweet_data['text'] not in tweet_list2):
                    competitor1_data.append(tweet_data)

                if tweet_data['text'] not in tweet_list2:
                    tweet_list2.append(tweet_data['text'])

    competitor1_data = sorted(competitor1_data, key=lambda k: k['created_at'])

'''try:
    begin_date = min(main_data[0]['created_at'], competitor1_data[0]['created_at'], competitor2_data[0]['created_at'])
except:
    try:
        begin_date = min(main_data[0]['created_at'], competitor1_data[0]['created_at'], competitor2_data[0]['created_at'])
    except:
        begin_date = main_data[0]['created_at']
'''

report.volumebegintime = str(begin_date.date()) + " " + str(begin_date.hour) + ":" + str(begin_date.minute)
print "Begin time", report.volumebegintime

'''max_hour = 0
try:
    max_hour = max(parser.parse(main_data[-1]['created_at']).hour, parser.parse(competitor1_data[-1]['created_at']).hour, parser.parse(competitor2_data[-1]['created_at']).hour)
except:
    try:
        max_hour = max(parser.parse(main_data[-1]['created_at']).hour, parser.parse(competitor1_data[-1]['created_at']).hour)
    except:
        max_hour = parser.parse(main_data[-1]['created_at']).hour

if max_hour == 23:
    max_hour = -1
'''

#report.volumeendtime = str(max_hour + 1) + ":00"
'''try:
    end_date = max(main_data[-1]['created_at'], competitor1_data[-1]['created_at'], competitor2_data[-1]['created_at'])
except:
    try:
        end_date = max(main_data[-1]['created_at'], competitor1_data[-1]['created_at'])
    except:
        end_date = main_data[-1]['created_at']
'''

report.volumeendtime = str(end_date.date()) + " " + str(end_date.hour) + ":" + str(end_date.minute)
print "End time", report.volumeendtime

timelist = report.getTimeList()



word_cloud = {}
key_infl = {}
word_sent = {}
word_klout = {}

c = 0

#word cloud
#TODO stop words and stem
#TODO calculate KLOUT, partnership with KLOUT ???
stopwordsdict = {
  'nl': 'dutch',
  'en': 'english',
  'fr': 'french',
  'de': 'german',
  'es': 'spanish',
}


for tweet in main_data:
        #TODO: order set of words!
        #for word in word_tokenize(tweet['text']):
        for word in tweet['text'].split():
            word = word.lower()
            if len(word) > 5 and word not in corpus.stopwords.words(stopwordsdict[MAIN_LANGUAGE]) and word[0] != '@' and re.match("^[A-Za-z0-9_-]*(\#)*[A-Za-z0-9_-]*$", word):
                if word_cloud.has_key(word):
                    word_cloud[word] += 1
                else:
                    word_cloud[word] = 1

#===============================================================================
#                key_infl[word] = tweet['username']
# 
#                if word_sent.has_key(word):
#                    word_sent[word].append(tweet['sentiment'])
#                else:
#                    word_sent[word] = list()
#                    word_sent[word].append(tweet['sentiment'])
# 
#                if not word_klout.has_key(word):
#                    try:
#                        klout = KloutInfluence(tweet['username'].encode('utf-8'))
#                        word_klout[word] = klout.score()
#                    except:
#                        word_klout[word] = -1
#===============================================================================
                c += 1

        if DEBUG:
            if c > 100:
                break

report.word_cloud = sorted(word_cloud.items(), key=lambda k:k[1], reverse=True)
print report.word_cloud
#report.key_infl = key_infl
#report.word_sent = word_sent
#report.word_klout = sorted(word_klout.items(), key=lambda k:k[1], reverse = True)

word_cloud = {}


for tweet in competitor1_data:
        #TODO: order set of words!
        #for word in word_tokenize(tweet['text']):
        for word in tweet['text'].split():
            word = word.lower()
            if len(word) > 5 and word not in corpus.stopwords.words(stopwordsdict[MAIN_LANGUAGE]) and word[0] != '@' and re.match("^[A-Za-z0-9_-]*(\#)*[A-Za-z0-9_-]*$", word):
                if word_cloud.has_key(word):
                    word_cloud[word] += 1
                else:
                    word_cloud[word] = 1
                    
report.word_cloud = sorted(word_cloud.items(), key=lambda k:k[1], reverse=True)
print report.word_cloud


#report.create(MAIN_ENTERPRISE)
