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

data = []

classifier = None
classinfo = None
analysis = tweeql.extras.sentiment.analysis
fname = resource_filename(tweeql.extras.sentiment.__name__, 'sentiment.pkl.gz')
fp = gzip.open(fname)
classifier_dict = pickle.load(fp)
fp.close()


print classifier_dict

exit

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

twitter = Twython(app_key=general_settings.CONSUMER_KEY, app_secret=general_settings.CONSUMER_SECRET, oauth_token=general_settings.ACCESS_TOKEN, oauth_token_secret=general_settings.ACCESS_SECRET)
for i in (map(lambda x : x+1, range(3))):
        try:
            print "Searching tweets page %i" % i
            search_results = twitter.search(q="hollandsnieuwe", page=i, rpp=10)
        except:
            pass
                 
        print "Indexing tweets page %i" % i
        for tweet in search_results["results"]:
            tweet_data = {}
            print "Tweet from @%s Date: %s" % (tweet['from_user'].encode('utf-8'),tweet['created_at'])
            #print tweet['text'].encode('utf-8'),"\n"
            tweet_data['text'] = tweet['text'].encode('utf-8')
            tweet_data['username'] = tweet['from_user']
            tweet_data['created_at'] = tweet['created_at']
            klout = KloutInfluence(tweet['from_user'].encode('utf-8'))
            try:
                tweet_data['influence'] = klout.score()
                tweet_data['influences'] =  klout.influences()
                tweet_data['influence_topics'] = klout.topics()
            except:
                tweet_data['influence'] = 0
                tweet_data['influences'] =  {}
                tweet_data['influence_topics'] = {}
            
            tweet_data['sentiment'] = sentiment(tweet['text'])
            tweet_data['ws'] = 0
            
            data.append(tweet_data)
        
            
print "Creating word cloud..."

            
print "Creating volume plot..."
x= []
y = []
volume = -1    
for tweet_data in data:
    d = parser.parse(tweet_data['created_at']).date()
    if not d in x:
        if volume != -1: 
            y.append(volume)
        volume = 0
        x.append(d)
    volume += 1
    
y.append(volume)

print x
print y

print "Calculating the freq time..."
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)

times = [item['created_at'] for item in data]

sum_deltas = 0
count_deltas = 0
for t0, t1 in pairwise(times):
    sum_deltas += ((parser.parse(t1) - parser.parse(t0)).seconds / 60)
    count_deltas += 1

delta_time = sum_deltas / count_deltas

print(delta_time) #minutes or seconds ?
    
print "Calculating the delta's of Volume..."
comb_list = itertools.combinations(y, 2)

max_volume_delta = 0
# %

for comb in comb_list:
    delta = abs(comb[1] - comb[0])
    if delta > max_volume_delta:
        max_volume_delta = delta

print max_volume_delta

print "Creating sentiment plot..."
x= []
y = []
sentiment = -100
counter = 0         
for tweet_data in data:
       d = parser.parse(tweet_data['created_at']).date()
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

print "Calculating the delta's of sentiment..."
comb_list = itertools.combinations(y, 2)

max_sentiment_delta = 0

for comb in comb_list:
    delta = abs(comb[1] - comb[0])
    if delta > max_sentiment_delta:
        max_sentiment_delta = delta
        
print max_sentiment_delta

years    = mdates.YearLocator()   # every year
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

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

#plt.show()

print "Calculating weighted scores..."
for xmin, xmax in map(None, xmins, xmaxs):                
    for tweet_data in data:
        if parser.parse(tweet_data['created_at']).date() == xmax:
            tweet_data['ws'] = 30 * tweet_data['sentiment'] + 1 * tweet_data['influence'] + 1000 * (xmaxs.index(xmax) + 1)

        if parser.parse(tweet_data['created_at']).date() == xmin:
            tweet_data['ws'] = -30 * tweet_data['sentiment'] - 1 * tweet_data['influence'] - 1000 * (xmins.index(xmin) + 1)

conversationlist = []      
    
#TODO: generalize for more clusters
# calculate top 5 of ws in different maxima regions
print "Creating clusters of local optima..."
cluster1 = []
cluster2 = []
cluster3 = []
cluster4 = []

for tweet_data in data:
    ws = tweet_data['ws']
    
    if ws > 1999:
        cluster3.append(tweet_data)
    if ws > 999 and ws < 1190:
        cluster1.append(tweet_data)
    if ws < -1001 and ws > -1191:
        cluster2.append(tweet_data)
    if ws < -1189:
        cluster4.append(tweet_data)

print "Sort clusters..."
sorted_cluster1 = sorted(cluster1, key=lambda k: k['ws'], reverse=True)
sorted_cluster2 = sorted(cluster2, key=lambda k: k['ws'])
sorted_cluster3 = sorted(cluster3, key=lambda k: k['ws'], reverse=True)
sorted_cluster4 = sorted(cluster4, key=lambda k: k['ws'])
        
print sorted_cluster1
print sorted_cluster2
print sorted_cluster3
print sorted_cluster4

print "Creating conversation list..."
conversationlist.extend(sorted_cluster1[:3])
conversationlist.extend(sorted_cluster2[:3])
conversationlist.extend(sorted_cluster3[:3])
conversationlist.extend(sorted_cluster4[:3])

conversations = sorted(conversationlist, key=lambda k: k['created_at'])

for conv in conversations:
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])

sorted_sentiment = sorted(data, key=lambda k: k['sentiment'])
sorted_negative = sorted_sentiment[:5]
sorted_positive = sorted_sentiment[-6:-1]

print "Top 5 Positive:"

for conv in sorted_positive:
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])
  

print "Top 5 Negative:"

for conv in sorted_negative:
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])
    
plt.show()
        
        

