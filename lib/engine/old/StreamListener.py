__author__ = 'kristof.leroux@gmail.com'

import tweepy
from textwrap import TextWrapper
from pysqlite2 import dbapi2 as sqlite3

class StreamListener(tweepy.StreamListener):
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
    conn = sqlite3.connect('socialexpress.db')

    def on_status(self, status):
        try:
            print 'on_status'
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO feeds (id, text, date, username, location) VALUES (0, %s, %s, %s, %s)' ,(status.text, status.created_at, status.author.screen_name, ''))
            print self.status_wrapper.fill(status.text)
            print '\n %s  %s  via %s\n' % (status.author.screen_name, status.created_at, status.source)
            self.conn.commit()
        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass
