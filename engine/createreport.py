'''
Created on Jun 6, 2012

@author: kristof
'''
import time
import datetime
import general_settings
from twython import Twython
from klout import KloutInfluence
import tweeql.extras.sentiment
import tweeql.extras.sentiment.analysis
from ordereddict import OrderedDict
from pkg_resources import resource_filename
from dateutil import parser
import itertools
from pygeocoder import Geocoder
import language
import urllib
from collections import defaultdict

import gzip
import math
import re
import os
import pickle
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText    


MAIN_KEYWORD = 'koffie'
COMPETITOR1_KEYWORD = 'koffieapparaat'
COMPETITOR2_KEYWORD = ''
MAIN_ENTERPRISE =  'Philips'
MAIN_LOCATION = 'Amsterdam'

MAIN_LANGUAGE = 'nl'
MAIN_COUNTRY = 'The Netherlands'
MAIN_SCREEN_NAME_LIST = ['PhilipsNL', 'PhilipsCare_NL']

MAIL_TO_LIST = ['kristof.leroux@gmail.com']

SEARCH_PAGES = 100
SEARCH_RPP = 1000

#REPORT1
import report1
import report2

report = report1.Report1()
main_data = []
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

# search keywords
twitter = Twython(app_key=general_settings.CONSUMER_KEY, app_secret=general_settings.CONSUMER_SECRET, oauth_token=general_settings.ACCESS_TOKEN, oauth_token_secret=general_settings.ACCESS_SECRET)
for i in (map(lambda x : x+1, range(SEARCH_PAGES))):
        try:
            print "Searching tweets page %i" % i
            # TODO: country language
            search_results = twitter.search(q=MAIN_KEYWORD, page=i, rpp=SEARCH_RPP)
        except:
            pass
                 
        print "Indexing tweets page %i" % i
        for tweet in search_results["results"]:
            print tweet
            tweet_data = {}
            print "Tweet from @%s Date: %s" % (tweet['from_user'].encode('utf-8'),tweet['created_at'])
            #print tweet['text'].encode('utf-8'),"\n"
            tweet_data['text'] = tweet['text'].encode('utf-8')
            tweet_data['username'] = tweet['from_user']
            tweet_data['created_at'] = tweet['created_at']
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
            tweet_data['avatar'] = urllib.urlretrieve(tweet['profile_image_url_https'])

            #language
            #ld = language.LangDetect()
            #tweet_data['lang'] = ld.detect(tweet_data['text'])
            tweet_data['lang'] = tweet['iso_language_code']
            print tweet_data['lang']
            
            #filter out retweets
            if (MAIN_COUNTRY == tweet_data['country']) or (tweet_data['lang'] == MAIN_LANGUAGE) and (tweet_data['username'] not in MAIN_SCREEN_NAME_LIST) and (tweet_data['text'] not in tweet_list):
                main_data.append(tweet_data)
            
            if tweet_data['text'] not in tweet_list:
                tweet_list.append(tweet_data['text'])
            
main_data = sorted(main_data, key=lambda k: k['created_at'])
report.spike_keyword = MAIN_KEYWORD
report.spike_location = MAIN_LOCATION

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
            tweet_data['text'] = tweet['text'].encode('utf-8')
            tweet_data['username'] = tweet['from_user']
            tweet_data['created_at'] = tweet['created_at']
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
            tweet_data['avatar'] = urllib.urlretrieve(tweet['profile_image_url_https'])

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

for i in (map(lambda x : x+1, range(SEARCH_PAGES))):
        try:
            print "Searching tweets page %i" % i
            # TODO: country language
            search_results = twitter.search(q=COMPETITOR2_KEYWORD, page=i, rpp=SEARCH_RPP)
        except:
            pass
                 
        print "Indexing tweets page %i" % i
        for tweet in search_results["results"]:
            print tweet
            tweet_data = {}
            print "Tweet from @%s Date: %s" % (tweet['from_user'].encode('utf-8'),tweet['created_at'])
            #print tweet['text'].encode('utf-8'),"\n"
            tweet_data['text'] = tweet['text'].encode('utf-8')
            tweet_data['username'] = tweet['from_user']
            tweet_data['created_at'] = tweet['created_at']
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

                #print results[0]
            else:
                tweet_data['geo'] = None
                tweet_data['country'] = None
                
            #gender
            #avatar
            tweet_data['avatar'] = urllib.urlretrieve(tweet['profile_image_url_https'])

            #language
            #ld = language.LangDetect()
            #tweet_data['lang'] = ld.detect(tweet_data['text'])
            tweet_data['lang'] = tweet['iso_language_code']
            print tweet_data['lang']
            
            #filter out retweets
            if (MAIN_COUNTRY == tweet_data['country']) or (tweet_data['lang'] == MAIN_LANGUAGE) and (tweet_data['username'] not in MAIN_SCREEN_NAME_LIST) and (tweet_data['text'] not in tweet_list3):
                competitor1_data.append(tweet_data)
            
            if tweet_data['text'] not in tweet_list3:
                tweet_list3.append(tweet_data['text'])
            
competitor2_data = sorted(competitor2_data, key=lambda k: k['created_at'])

print "Calculating cumulative volumes... comp2"
x= []
y = []
volume = -1    
for tweet_data in competitor2_data:
    d = parser.parse(tweet_data['created_at']).hour #daily or hourly 
    tweet_data['hour_string'] = str(parser.parse(tweet_data['created_at']).hour) + ":" + str(parser.parse(tweet_data['created_at']).minute)

    if not d in x:
        if volume != -1: 
            y.append(volume)
        volume = 0
        x.append(d)
    volume += 1
    
y.append(volume)

print x
print y
report.volumegraph3 = tuple(y)

print "Calculating cumulative volumes... comp1"
x= []
y = []
volume = -1    
for tweet_data in competitor1_data:
    d = parser.parse(tweet_data['created_at']).hour #daily or hourly 
    tweet_data['hour_string'] = str(parser.parse(tweet_data['created_at']).hour) + ":" + str(parser.parse(tweet_data['created_at']).minute)

    if not d in x:
        if volume != -1: 
            y.append(volume)
        volume = 0
        x.append(d)
    volume += 1
    
y.append(volume)

print x
print y
report.volumegraph2 = tuple(y)

print "Calculating cumulative volumes..."
x= []
y = []
volume = -1    
for tweet_data in main_data:
    d = parser.parse(tweet_data['created_at']).hour #daily or hourly 
    tweet_data['hour_string'] = str(parser.parse(tweet_data['created_at']).hour) + ":" + str(parser.parse(tweet_data['created_at']).minute)

    if not d in x:
        if volume != -1: 
            y.append(volume)
        volume = 0
        x.append(d)
    volume += 1
    
y.append(volume)

print x
print y
report.volumegraph1 = tuple(y)

report.volumekeywords = [MAIN_KEYWORD, COMPETITOR1_KEYWORD, COMPETITOR2_KEYWORD]
report.volumebegintime = str(parser.parse(main_data[0]['created_at']).hour) + ":" + str(parser.parse(main_data[0]['created_at']).minute)
report.volumeendtime = str(parser.parse(main_data[-1]['created_at']).hour) + ":" + str(parser.parse(main_data[-1]['created_at']).minute)

print "Calculating the freq times..."
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

times = [item['created_at'] for item in main_data]

sum_deltas = 0
count_deltas = 1
for (t0, t1) in pairwise(times):
    sum_deltas += (parser.parse(t1) - parser.parse(t0)).seconds #seconds, minutes, hours
    #print t0, t1, (sum_deltas) / count_deltas
    count_deltas += 1

delta_time = (sum_deltas) / count_deltas

print(delta_time) #minutes or seconds ?

report.freq_time = delta_time
    
print "Calculating the delta's of Volume..."
comb_list = itertools.combinations(y, 2)

max_volume_delta = 0
max_volume_sign = 1
max_volume_s0 = 1
max_volume_s1 = 0

for comb in comb_list:
    delta = abs(comb[1] - comb[0])
    if delta:
        sign = (comb[1] - comb[0]) / abs(comb[1] - comb[0]) 
    else:
        sign = 1
    if delta > max_volume_delta:
        max_volume_delta = delta
        max_volume_sign = sign
        if (comb[0] < comb[1]):
            max_volume_s0 = comb[0]
            max_volume_s1 = comb[1]
        else:
            max_volume_s0 = comb[1]
            max_volume_s1 = comb[0]


max_volume_percentage = (max_volume_delta / max_volume_s0) * 100
print max_volume_s0, max_volume_s1

print "Creating sentiment plot..."
x= []
y = []
sentiment = -100
counter = 0         
for tweet_data in main_data:
    d = parser.parse(tweet_data['created_at']).hour
    if not d in x:
        if sentiment > -100: 
            y.append((sentiment/counter))
        sentiment = 0
        counter = 0
        x.append(d)
    sentiment += tweet_data['sentiment']
    counter += 1
   
y.append(sentiment/counter)
    
print x 
print y

report.sentimentgraph = [tuple(y)]

print "Calculating the delta's of sentiment..."
comb_list = itertools.combinations(y, 2)

max_sentiment_delta = 0
max_sentiment_sign = 1
max_sentiment_s0 = 1
max_sentiment_s1 = 0

for comb in comb_list:
    delta = abs(comb[1] - comb[0])
    if delta:
        sign = (comb[1] - comb[0]) / abs(comb[1] - comb[0]) 
    else:
        sign= 1
    if delta > max_sentiment_delta:
        max_sentiment_delta = delta
        max_sentiment_sign = sign
        if comb[0] < comb[1]:
            max_sentiment_s0 = comb[0]
            max_sentiment_s1 = comb[1]
        else:
            max_sentiment_s0 = comb[1]
            max_sentiment_s1 = comb[0]
        
max_sentiment_percentage = (max_sentiment_delta / max_sentiment_s0) * 100
print max_sentiment_s0, max_sentiment_s1

if max_volume_percentage > max_sentiment_percentage:
    report.spike_percentage = max_volume_sign * max_volume_percentage
else:
    report.spike_percentage = max_sentiment_sign * max_sentiment_percentage    


'''years    = mdates.YearLocator()   # every year
months   = mdates.MonthLocator()  # every month
days     = mdates.DayLocator()
hours    = mdates.HourLocator(interval=2)
fmt = mdates.DateFormatter('%d %b %Y')

fig = plt.figure()
ax = fig.add_subplot(111)

# format the ticks
ax.xaxis.set_major_locator(days)
ax.xaxis.set_major_formatter(fmt)
ax.xaxis.set_minor_locator(hours)

datemin = min(x)
datemax = max(x)
ax.set_xlim(datemin, datemax)
ax.set_ylim(0, max(y))

ax.format_xdata = mdates.DateFormatter('%a, %d %b %Y %H:%M:%S %z')
ax.format_ydata = '$%1.2f'
ax.grid(True)
ax.plot(x, y)
'''
a = np.diff(np.sign(np.diff(y))).nonzero()[0] + 1 # local min+max
b = (np.diff(np.sign(np.diff(y))) > 0).nonzero()[0] + 1 # local min
c = (np.diff(np.sign(np.diff(y))) < 0).nonzero()[0] + 1 # local max

xmins = [x[i] for i in b]
ymins = [y[i] for i in b]
xmaxs = [x[i] for i in c]
ymaxs = [y[i] for i in c]

print xmins
print ymins
print xmaxs
print ymaxs

'''
if b.any():
    ax.plot(xmins, ymins, "o", label="min")
if c.any():
    ax.plot(xmaxs, ymaxs, "o", label="max")
plt.legend()
'''

'''# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()'''

#plt.show()

print "Calculating weighted scores..."
for xmin, xmax in map(None, xmins, xmaxs):                
    for tweet_data in main_data:
        if parser.parse(tweet_data['created_at']).hour == xmax:
            tweet_data['ws'] = 30 * tweet_data['sentiment'] + 1 * tweet_data['influence'] + 1000 * (xmaxs.index(xmax) + 1)

        if parser.parse(tweet_data['created_at']).hour == xmin:
            tweet_data['ws'] = -30 * tweet_data['sentiment'] - 1 * tweet_data['influence'] - 1000 * (xmins.index(xmin) + 1)

conversationlist = []      
    
#TODO: generalize for more clusters
# calculate top 5 of ws in different maxima regions
print "Creating clusters of local optima..."
cluster1 = []
cluster2 = []
cluster3 = []
cluster4 = []

for tweet_data in main_data:
    ws = tweet_data['ws']
    
    #todo: check for more clusters?
    if ws > 1999:
        cluster1.append(tweet_data)
    if ws > 999 and ws < 1190:
        cluster2.append(tweet_data)
    if ws < -1001 and ws > -1191:
        cluster3.append(tweet_data)
    if ws < -1189:
        cluster4.append(tweet_data)

print "Sort clusters..."
#todo: check is reverse or not
sorted_cluster1 = sorted(cluster1, key=lambda k: k['ws'], reverse=True)
sorted_cluster2 = sorted(cluster2, key=lambda k: k['ws'], reverse=True)
sorted_cluster3 = sorted(cluster3, key=lambda k: k['ws'])
sorted_cluster4 = sorted(cluster4, key=lambda k: k['ws'])
        
print sorted_cluster1
print sorted_cluster2
print sorted_cluster3
print sorted_cluster4

#todo get conversation! get original tweet id
print "Creating conversation list..."
conversationlist.extend(sorted_cluster1[:3])
conversationlist.extend(sorted_cluster2[:3])
conversationlist.extend(sorted_cluster3[:3])
conversationlist.extend(sorted_cluster4[:3])

conversations = sorted(conversationlist, key=lambda k: k['created_at'])

for conv in conversations:
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])

report.conversationlist = conversations

sorted_sentiment = sorted(main_data, key=lambda k: k['sentiment'])

sorted_negative = sorted_sentiment[:5]
sorted_positive = sorted_sentiment[-6:-1]

report.top5positive = sorted_positive
report.top5negative = sorted_negative

print "Top 5 Positive:"

for conv in sorted_positive:
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])


print "Top 5 Negative:"

for conv in sorted_negative:
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])
    
#word cloud
#Collect word statistics
counts = defaultdict(int) 
stemmed_sentences = []
for sent in stemmed_sentences:
    for stem in sent:
        counts[stem] += 1

#This block deletes all words with count <3
#They are not relevant and sorting will be way faster
pairs = [(x,y) for x,y in counts.items() if y >= 3]

#Sort (stem,count) pairs based on count 
sorted_stems = sorted(pairs, key = lambda x: x[1])
report.create(MAIN_ENTERPRISE)
