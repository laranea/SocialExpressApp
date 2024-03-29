# -*- coding: utf-8 -*-
'''
Created on Jun 6, 2012

@author: kristof
'''
import urllib2
import base64
import zlib
import threading
from threading import Lock
from cStringIO import StringIO
import json
import sys
from pprint import pprint
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
from email.utils import parsedate

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def parseDateText(text):
    try:
        return datetime.datetime(*parsedate(text)[:6])
    except:
        return None


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

DEBUG = True
REALTIME = False


MAIN_KEYWORD = u"King Kong"
#MAIN_KEYWORD = 'senseo'
COMPETITOR1_KEYWORD = u"Delonghi"
COMPETITOR2_KEYWORD = u"Jura"
MAIN_ENTERPRISE =  'PhilipsNL'
MAIN_LOCATION = 'Amsterdam'

MAIN_LANGUAGE = 'nl'
MAIN_COUNTRY = 'The Netherlands'
MAIN_SCREEN_NAME_LIST = ['PhilipsNL', 'PhilipsCare_NL']

MAIL_TO_LIST = ['kristof.leroux@gmail.com']

SEARCH_PAGES = 10
SEARCH_RPP = 1000

#todo: dynamic time slices, also in report.py (timelist)...
begin_date = datetime.datetime(2012, 7, 26, 9, 0)
end_date = datetime.datetime(2012, 7, 26, 9, 15)

CHUNKSIZE = 1024
MAXBUFFSIZE = 20*CHUNKSIZE

NEWLINE = '\n'

url = "https://stream.gnip.com:443/accounts/SocialExpress/publishers/twitter/replay/track/Production.json?fromDate=201207260900&toDate=201207260915"
UN = 'kristof.leroux@gmail.com'
PWD = 'elleke77'

main_data = []

headers = {
    'Accept': 'application/json',
    'Connection': 'keep-alive',
    'Accept-Encoding' : 'gzip',
    'Authorization' : 'Basic %s' % base64.encodestring('%s:%s' % (UN, PWD))
}
req = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(req)

d = zlib.decompressobj(16+zlib.MAX_WBITS)

ldata = StringIO()
bufSize = 0
for n in range(1, 100):
    tmpString = d.decompress(response.read(CHUNKSIZE))
    bufSize += len(tmpString)
    ldata.write(tmpString)
    if tmpString.endswith(NEWLINE) and bufSize > MAXBUFFSIZE:
        bufList = [x.strip() for x in ldata.getvalue().split(NEWLINE) if x.strip() <> '']
        ldata = StringIO()
        bufSize = 0
        for rec in bufList:
            jrec = json.loads(rec.strip())
            pprint(jrec)
            print "="*40
            try:
                jrec['created_at'] = parseDateText(jrec['created_at'])
                jrec['sentiment'] = sentiment(jrec['text'])
                main_data.append(jrec)
            except:
                pass

print main_data

    #REPORT1
import report

report = report.Report()
competitor1_data = []
competitor2_data = []

tweet_list = []
tweet_list2 = []
tweet_list3 = []

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

print "Calculating cumulative volumes... comp2"
x= []
y = []
volume = -1

volume_axis = {}
for tweet_data in competitor2_data:
    dt = tweet_data['created_at']
    d = datetime.datetime(dt.year, dt.month, dt.day, dt.hour)
    tweet_data['hour_string'] = str(tweet_data['created_at'].hour) + ":" + str(tweet_data['created_at'].minute)
    if timelist[0] > dt.strftime("%H:%M %d/%m/%Y"):
        continue
    if not d in x:
        if volume != -1:
            y.append(volume)
        volume = 0
        x.append(d)
    volume += 1
    
    #if dt.hour >= 0 and dt.hour < 12:
    try:
        volume_axis[dt.strftime("%H:00 %d/%m/%Y")] += 1
    except:
        volume_axis[dt.strftime("%H:00 %d/%m/%Y")] = 1
    #else:
    #    try:
    #        volume_axis[dt.strftime("12:00 %d/%m/%Y")] += 1
    #    except:
    #        volume_axis[dt.strftime("12:00 %d/%m/%Y")] = 1

y.append(volume)

print x
print y
volumegraph3 = []
if COMPETITOR2_KEYWORD:
    for time in timelist:
        try:
            volumegraph3.append(float(volume_axis[time]))
        except:
            volumegraph3.append(0)

print volumegraph3


volume_axis = {}

print "Calculating cumulative volumes... comp1"
x= []
y = []
volume = -1
for tweet_data in competitor1_data:
    dt = tweet_data['created_at']
    d = datetime.datetime(dt.year, dt.month, dt.day, dt.hour)
    tweet_data['hour_string'] = str(tweet_data['created_at'].hour) + ":" + str(tweet_data['created_at'].minute)
#    graph_date_obj  = datetime.strptime(start_day, date_format)
#    if datetime.strptime(dt, "%H:%M %d/%m/%Y") dt.strftime()
    if timelist[0] > dt.strftime("%H:%M %d/%m/%Y"):
        continue
    if not d in x:
        if volume != -1:
            y.append(volume)
        volume = 0
        x.append(d)

    volume += 1
        
    #if dt.hour >= 0 and dt.hour < 12:
    try:
        volume_axis[dt.strftime("%H:00 %d/%m/%Y")] += 1
    except:
        volume_axis[dt.strftime("%H:00 %d/%m/%Y")] = 1
    #else:
    #    try:
    #        volume_axis[dt.strftime("12:00 %d/%m/%Y")] += 1
    #    except:
    #        volume_axis[dt.strftime("12:00 %d/%m/%Y")] = 1

print "volume axisssss", volume_axis
print "timelistssssssss", timelist
volumegraph2 = []
if COMPETITOR1_KEYWORD:
    for time in timelist:
        try:
            volumegraph2.append(float(volume_axis[time]))
        except:
            volumegraph2.append(0)


#blah = raw_input()

y.append(volume)
print x
print y
#volumegraph2 = tuple(y)
#volumegraph2 = tuple(volumegraph2)
#volumegraph2 = tuple(map(lambda x: float(x)/len(volume_axis), volume_axis.values()))
print "volumegraph2", volumegraph2
volume_axis = {}

print "Calculating cumulative volumes..."
x= []
y = []
x_main = []
volume = -1
for tweet_data in main_data:
    dt = tweet_data['created_at']
    x_main.append(dt)
    d = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)
    tweet_data['hour_string'] = str(tweet_data['created_at'].hour).zfill(2) + ":" + str(tweet_data['created_at'].minute).zfill(2)

    print dt.strftime("%H:%M %d/%m/%Y")

    if timelist[0] > dt.strftime("%H:%M %d/%m/%Y"):
        continue
    if not d in x:
        if volume != -1:
            y.append(volume)
        volume = 0
        x.append(d)
        
    #if dt.hour >= 0 and dt.hour < 12:
    try:
        print "volume_axis += 1"
        volume_axis[dt.strftime("%H:%M %d/%m/%Y")] += 1
    except:
        print 'volume_axis = 1'
        volume_axis[dt.strftime("%H:%M %d/%m/%Y")] = 1
#    else:
#        try:
#            volume_axis[dt.strftime("12:00 %d/%m/%Y")] += 1
#        except:
#            volume_axis[dt.strftime("12:00 %d/%m/%Y")] = 1

    volume += 1

y.append(volume)
volumegraph1 = []
for time in timelist:
    try:
        volumegraph1.append(float(volume_axis[time]))
    except:
        volumegraph1.append(0)

print x
print y
#volumegraph1 = tuple(y)

report.volumekeywords = [MAIN_KEYWORD, COMPETITOR1_KEYWORD, COMPETITOR2_KEYWORD]
#report.volumebegintime = str(parser.parse(main_data[0]['created_at']).hour) + ":" + str(parser.parse(main_data[0]['created_at']).minute)

if COMPETITOR1_KEYWORD and COMPETITOR2_KEYWORD:
    report.volumegraphs = [tuple(volumegraph1), tuple(volumegraph2), tuple(volumegraph3)]
elif COMPETITOR1_KEYWORD:
    report.volumegraphs = [tuple(volumegraph1), tuple(volumegraph2)]
else:
    report.volumegraphs = [tuple(volumegraph1)]
    
print "graph points ", report.volumegraphs

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
    sum_deltas += (t1 - t0).seconds #seconds, minutes, hours
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
deltas_volume = {}

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
counter = 1
for tweet_data in main_data:
    dt = tweet_data['created_at']
    d = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 0)

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
print "sentimentplot yyyy", y

report.sentimentgraph = tuple(y)

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
    report.spike_kind = 'volume'
else:
    report.spike_percentage = max_sentiment_sign * max_sentiment_percentage
    report.spike_kind = 'sentiment'

report.mentions_percentage = max_volume_percentage
report.sentiment_percentage = max_sentiment_percentage

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
a = np.diff(np.sign(np.diff(volumegraph1))).nonzero()[0] + 1 # local min+max
b = (np.diff(np.sign(np.diff(volumegraph1))) > 0).nonzero()[0] + 1 # local min
c = (np.diff(np.sign(np.diff(volumegraph1))) < 0).nonzero()[0] + 1 # local max

print a
print "bbb", b
print c

ya = [volumegraph1[i] for i in a]


d = np.diff(ya)

print d

#xmins = [x[i] for i in b]
ymins = [volumegraph1[i] for i in b]
#xmaxs = [x[i] for i in c]
ymaxs = [volumegraph1[i] for i in c]

#print "x minss", xmins
print "y minss", ymins
#print "x maxss", xmaxs
print "y maxss", ymaxs

'''xopt = [x[i] for i in a]
yopt = [y[i] for i in a]

report.optima = zip(xopt, yopt)'''

ok = []
sum_deltas = 0
count_deltas = 1
i = 0
j = 0
k = 0
l = 0
max_delta1 = 0
max_delta2 = 0
max_delta3 = 0

max_deltas = []

for (y0, y1) in pairwise(ya):
    delta = abs(y1 - y0)

    if delta > max_delta3:
        max_delta3 = delta
        j = i
    elif delta > max_delta2:
        max_delta2 = delta
        k = i
    elif delta > max_delta1:
        max_delta1 = delta
        l = i
    i += 1

#sorted_max_deltas = max_deltas.sort()

#print sorted_max_deltas
print 'ya', ya
#xopt = [x[i] for i in [l, k, j]]
yopt = [volumegraph1[i] for i in [l, k, j]]
#report.optima = zip(xopt, yopt)

report.optima = [l, k, j]
report.optima.sort()

print "l", l
print "k", k
print "j", j
#print "xopt", xopt
#print "yopt", yopt
print "xxx", x
print "yyy", y

#bla = raw_input()

#report.optima = zip(xmins, ymins)
#report.optima.extend(zip(xmaxs, xmins))

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

'''print "Calculating weighted scores..."
for xmin, xmax in map(None, xmins, xmaxs):
    for tweet_data in main_data:
        if tweet_data['created_at'].hour == xmax:
            tweet_data['ws'] = 30 * tweet_data['sentiment'] + 1 * tweet_data['influence'] + 1000 * (xmaxs.index(xmax) + 1)

        if tweet_data['created_at'].hour == xmin:
            tweet_data['ws'] = -30 * tweet_data['sentiment'] - 1 * tweet_data['influence'] - 1000 * (xmins.index(xmin) + 1)
'''
conversationlist = []

#TODO: generalize for more clusters
# calculate top 5 of ws in different maxima regions
print "Creating clusters of local optima..."
cluster1 = []
cluster2 = []
cluster3 = []
cluster4 = []

for tweet_data in main_data:
    dt = tweet_data['created_at']
    try:
        if dt.date() == x_main[l].date():
            tweet_data['ws'] = 30 * tweet_data['sentiment'] + 1 * tweet_data['influence'] + 1000 * (l + 1)
            cluster1.append(tweet_data)
        if dt.date() == x_main[k].date():
            tweet_data['ws'] = 30 * tweet_data['sentiment'] + 1 * tweet_data['influence'] + 1000 * (k + 1)
            cluster2.append(tweet_data)
        if dt.date() == x_main[j].date():
            tweet_data['ws'] = 30 * tweet_data['sentiment'] + 1 * tweet_data['influence'] + 1000 * (j + 1)
            cluster3.append(tweet_data)
    except:
        pass

    '''    ws = tweet_data['ws']

    #todo: check for more clusters?
    if ws > 1999:
        cluster1.append(tweet_data)
    if ws > 999 and ws < 1190:
        cluster2.append(tweet_data)
    if ws < -1001 and ws > -1191:
        cluster3.append(tweet_data)
    if ws < -1189:
        cluster4.append(tweet_data)
    '''

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
print "conversation listtt", conversations
#for conv in conversations:
#    print u"%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])

report.conversationlist = conversations

sorted_sentiment = sorted(main_data, key=lambda k: k['sentiment'])

sorted_negative = sorted_sentiment[:5]
sorted_positive = sorted_sentiment[-6:-1]

report.top5positive = sorted_positive
report.top5negative = sorted_negative

#print "Top 5 Positive:"
#
#for conv in sorted_positive:
#    print "positive cov---", conv
#    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])
#

#print "Top 5 Negative:"
#
#for conv in sorted_negative:
#    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])

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
                print word
                if word_cloud.has_key(word):
                    word_cloud[word] += tweet['sentiment']
                else:
                    word_cloud[word] = tweet['sentiment']

                #key_infl[word] = tweet['username']

                if word_sent.has_key(word):
                    word_sent[word].append(tweet['sentiment'])
                else:
                    word_sent[word] = list()
                    word_sent[word].append(tweet['sentiment'])

                #if not word_klout.has_key(word):
                #    try:
                #        klout = KloutInfluence(tweet['username'].encode('utf-8'))
                #        word_klout[word] = klout.score()
                #    except:
                #        word_klout[word] = -1
                #c += 1

        if DEBUG:
            if c > 5000:
                break

report.word_cloud = sorted(word_cloud.items(), key=lambda k:k[1], reverse=True)
report.key_infl = key_infl
report.word_sent = word_sent
report.word_klout = sorted(word_klout.items(), key=lambda k:k[1], reverse = True)

report.create(MAIN_ENTERPRISE)
