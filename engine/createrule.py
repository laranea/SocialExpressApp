'''
Created on Jun 29, 2012

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
import urllibjihip
from collections import defaultdict
import ordereddict

import gzip
import math
import re
import os
import pickle
import sys

import numpy as np
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

DEBUG = True
REALTIME = False


MAIN_KEYWORD = 'koffie'
#MAIN_KEYWORD = 'senseo'
COMPETITOR1_KEYWORD = 'koffieapparaat'
COMPETITOR2_KEYWORD = ''
MAIN_ENTERPRISE =  'PhilipsNL'
MAIN_LOCATION = 'Amsterdam'

MAIN_LANGUAGE = 'nl'
MAIN_COUNTRY = 'The Netherlands'
MAIN_SCREEN_NAME_LIST = ['PhilipsNL', 'PhilipsCare_NL']

MAIL_TO_LIST = ['kristof.leroux@gmail.com']

SEARCH_PAGES = 10
SEARCH_RPP = 1000

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

#TODO: real-time
# search keywords
search_result = []
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
            tweet_data['text'] = tweet['text']#.encode('utf-8')
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
                main_data.append(tweet_data)

            if tweet_data['text'] not in tweet_list:
                tweet_list.append(tweet_data['text'])

main_data = sorted(main_data, key=lambda k: k['created_at'])
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

if COMPETITOR2_KEYWORD:
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
                try:
                    tweet_data['avatar'] = urllib.urlretrieve(tweet['profile_image_url_https'])
                except:
                    tweet_data['avatar'] = (tweet['profile_image_url_https'])

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
volumegraph3 = tuple(y)

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
volumegraph2 = tuple(y)

print "Calculating cumulative volumes..."
x= []
y = []
volume = -1
for tweet_data in main_data:
    d = parser.parse(tweet_data['created_at']).hour #daily or hourly
    tweet_data['hour_string'] = str(parser.parse(tweet_data['created_at']).hour).zfill(2) + ":" + str(parser.parse(tweet_data['created_at']).minute).zfill(2)

    if not d in x:
        if volume != -1:
            y.append(volume)
        volume = 0
        x.append(d)
    volume += 1

y.append(volume)

print x
print y
volumegraph1 = tuple(y)

report.volumekeywords = [MAIN_KEYWORD, COMPETITOR1_KEYWORD, COMPETITOR2_KEYWORD]
#report.volumebegintime = str(parser.parse(main_data[0]['created_at']).hour) + ":" + str(parser.parse(main_data[0]['created_at']).minute)
report.volumebegintime = str(parser.parse(main_data[0]['created_at']).date()) + " " + str(parser.parse(main_data[0]['created_at']).hour) + ":" + str(parser.parse(main_data[0]['created_at']).minute)

max_hour = 0
try:
    max_hour = max(parser.parse(main_data[-1]['created_at']).hour, parser.parse(competitor1_data[-1]['created_at']).hour, parser.parse(competitor2_data[-1]['created_at']).hour)
except:
    try:
        max_hour = max(parser.parse(main_data[-1]['created_at']).hour, parser.parse(competitor1_data[-1]['created_at']).hour)
    except:
        max_hour = parser.parse(main_data[-1]['created_at']).hour

#report.volumeendtime = str(max_hour + 1) + ":00"
report.volumeendtime =  str(parser.parse(main_data[-1]['created_at']).date()) + " " + str(max_hour + 1) + ":00"

report.volumegraphs = [volumegraph1, volumegraph2, volumegraph3]

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
else:
    report.spike_percentage = max_sentiment_sign * max_sentiment_percentage

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
a = np.diff(np.sign(np.diff(y))).nonzero()[0] + 1 # local min+max
b = (np.diff(np.sign(np.diff(y))) > 0).nonzero()[0] + 1 # local min
c = (np.diff(np.sign(np.diff(y))) < 0).nonzero()[0] + 1 # local max

print a
print b
print c

ya = [y[i] for i in a]



d = np.diff(ya)

print d


xmins = [x[i] for i in b]
ymins = [y[i] for i in b]
xmaxs = [x[i] for i in c]
ymaxs = [y[i] for i in c]

print xmins
print ymins
print xmaxs
print ymaxs

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

xopt = [x[i] for i in [l, k, j]]
yopt = [y[i] for i in [l, k, j]]

report.optima = zip(xopt, yopt)

print ok
print xopt
print yopt

bla = raw_input()

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
    print "positive cov---", conv
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])


print "Top 5 Negative:"

for conv in sorted_negative:
    print "%s (%s): %s (sent: %f) (klout: %f)" % (conv['username'], conv['created_at'], conv['text'], conv['sentiment'], conv['influence'])

word_cloud = {}
key_infl = {}
word_sent = {}
word_klout = {}

c = 0

#word cloud
#TODO stop words and stem
#TODO calculate KLOUT, partnership with KLOUT ???
for tweet in main_data:
        #for word in word_tokenize(tweet['text']):
        print "tweet url check---", tweet
        for word in tweet['text'].split():
            word = word.lower()
            if len(word) > 5 and word not in corpus.stopwords.words('dutch') and word[0] != '@' and re.match("^[A-Za-z0-9_-]*(\#)*[A-Za-z0-9_-]*$", word):
                print "print word-----------", word
                if word_cloud.has_key(word):
                    word_cloud[word] += tweet['sentiment']
                else:
                    word_cloud[word] = tweet['sentiment']

                key_infl[word] = tweet['username']

                if word_sent.has_key(word):
                    word_sent[word].append(tweet['sentiment'])
                else:
                    word_sent[word] = list()
                    word_sent[word].append(tweet['sentiment'])

                if not word_klout.has_key(word):
                    try:
                        klout = KloutInfluence(tweet['username'].encode('utf-8'))
                        word_klout[word] = klout.score()
                    except:
                        word_klout[word] = -1
                c += 1

        if DEBUG:
            if c > 100:
                break

report.word_cloud = sorted(word_cloud.items(), key=lambda k:k[1], reverse=True)
report.key_infl = key_infl
report.word_sent = word_sent
report.word_klout = sorted(word_klout.items(), key=lambda k:k[1], reverse = True)

report.create(MAIN_ENTERPRISE)
