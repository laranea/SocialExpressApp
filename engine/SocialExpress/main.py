__author__ = 'kristof.leroux@gmail.com'

import sys
from celery.task import task
from tweeql import status_handlers
from tweeql.exceptions import TweeQLException
from tweeql.query_runner import QueryRunner

import functions

def addslashes(string):
    return "'" + string + "'"

@task
def runQuery(keywords):
    map(addslashes, keywords)
    runner = QueryRunner()
    keywords = " OR ".join(keywords)
    print "keywords: " + keywords
    runner.run_query("SELECT text, sentiment(text) AS sentiment, location, language(text) AS language, influence(screen_name) AS influence FROM Twitter WHERE text CONTAINS '%s';" % keywords, False)

runQuery(['abn', 'amro', 'abn-amro', 'abnamro', 'pin', 'pas'])