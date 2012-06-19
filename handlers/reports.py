import tornado.ioloop
import tornado.web
from  tornado.template import Loader
from models.models import *
from connectdb import ConnectDB
from basehandler import BaseHandler


class NewWeeklyReport(BaseHandler):

    def get(self):
        self.render("newweeklyreport.html")


class ManageExistingReport(BaseHandler):

    def get(self):
        self.render("manageexistingreports.html")


class GeneratedWeeklyReports(BaseHandler):

    def get(self):
        self.render("generatedweeklyreports.html")


class NewRealTimeReport(BaseHandler):

    def get(self):
        self.render("newrealtimereport.html")
