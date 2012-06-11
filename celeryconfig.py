'''
Created on May 28, 2012

@author: kristof.leroux@gmail.com
'''
BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "amqp"
CELERY_IMPORTS = ("main", )

