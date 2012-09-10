#!/usr/bin/env python

import urllib2
import base64
import zlib
import threading
from threading import Lock
from cStringIO import StringIO
import json
import sys
from pprint import pprint
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


MAIN_KEYWORD = u"Saeco"
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
begin_date = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=1)
end_date = datetime.datetime.now(pytz.UTC)

# tune these as needed
CHUNKSIZE = 1024
MAXBUFFSIZE = 20*CHUNKSIZE

NEWLINE = '\n'

url = "https://stream.gnip.com:443/accounts/SocialExpress/publishers/twitter/replay/track/Production.json?fromDate=201207260900&toDate=201207260915"
UN = 'kristof.leroux@gmail.com'
PWD = 'elleke77'

print_lock = Lock()

class procEntry(threading.Thread):
    def __init__(self, buf):
        self.bufList = [x.strip() for x in buf.split(NEWLINE) if x.strip() <> '']
        threading.Thread.__init__(self)

    def run(self):
        try:
            self.output(self.bufList)
        except Exception, e:  # v hard to debug, catches everything!
            sys.stderr.write("thread failed: (%s)\n"%e)

    def output(self, bufList):
        for rec in bufList:
            jrec = json.loads(rec.strip())
            with print_lock:
                pprint(jrec)
                print "="*40

def get():
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
    while True:
        tmpString = d.decompress(response.read(CHUNKSIZE))
        bufSize += len(tmpString)
        ldata.write(tmpString)
        if tmpString.endswith(NEWLINE) and bufSize > MAXBUFFSIZE:
            procEntry(ldata.getvalue()).start()
            ldata = StringIO()
            bufSize = 0

if __name__ == "__main__":
    get()


