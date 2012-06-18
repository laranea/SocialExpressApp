'''
Created on May 19, 2012

@author: kristof.leroux@gmail.com
'''

# -*- coding: utf-8 -*-
import general_settings
import date
from tweeql.status_handlers import StatusHandler, PrintStatusHandler

class FileStatusHandler(StatusHandler):
    def __init__(self, batch_size, delimiter = u"|"):
        StatusHandler.__init__(self, general_settings.BATCH_SIZE)
        self.delimiter = delimiter
        self.fp = open(general_settings.OUTPUT_FILE + now(), "w")

    def handle_statuses(self, statuses):
        dicts = [dict(status.as_iterable_visible_pairs()) for status in statuses]
        print(dicts, self.fp)

    def __del__(self):
        self.fp.close()


PrintStatusHandler = FileStatusHandler
