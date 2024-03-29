"""
TweeQL Settings file
"""
# Twitter authentication information
import sys
import djcelery
djcelery.setup_loader()

BROKER_URL = "amqp://guest:guest@localhost:5672/"

TWITTER_USERNAME = "laranea"
TWITTER_PASSWORD = "elleke77"

# set to a database URI according to sqlalchemy's scheme for the database to dump stored tweets into
DATABASE_URI = "sqlite:///tweets.db"
# to send parameters to the connection argument, set the DATABASE_URI to
# the database protocol you want (e.g. "postgresql://") and then uncomment
# and fill in the following DATABASE_CONFIG
#
#DATABASE_CONFIG = {
#    'database':'',
#    'host':'',
#    'user':'',
#    'password':''
#}

# Running in debug mode, the system prints a lot more information
DEBUG = False

# set to a database URI according to sqlalchemy's scheme for the database to allow 
# various operators use as scratch space
SCRATCHSPACE_URI = "sqlite:///scratch.db"
# what prefix should tables used for scratchspace get
SCRATCHSPACE_PREFIX = "tweeql_scratch__"
