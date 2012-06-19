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


class ManageExistingRules(BaseHandler):

    def get(self):
        self.render("manageexistingrules.html")


class GeneratedRealTimeReports(BaseHandler):

    def get(self):
        self.render("generatedrealtimereports.html")


class AddRule(BaseHandler):

    def post(self):
        keyword = self.get_argument("keyword", default="")
        compare = self.get_argument("compare", default="")
        country = self.get_argument("country", default="")
        email = self.get_argument("emails", default="")
        print keyword, compare, country, email


class DeleteReport(BaseHandler):

    def post(self):
        report_id = self.get_argument("reportId", default="")
        print report_id


class DownloadReport(BaseHandler):

    def post(self):
        report_id = self.get_argument("reportId", default="")
        print report_id


class RealTimeReportCrieria(BaseHandler):

    def post(self):
        keyword = self.get_argument("keyword", default="")
        sentiment = self.get_argument("sentiment", default="")
        country = self.get_argument("country", default="")
        language = self.get_argument("language", default="")
        changes = self.get_argument("changes", default="")
        change_rate = self.get_argument("change-rate", default="")
        email = self.get_argument("emails", default="")
        print keyword, sentiment, country, language, changes, change_rate, email


class DeleteTrigger(BaseHandler):

    def post(self):
        trigger_id = self.get_argument("triggerId", default="")
        print trigger_id


class DownloadRealTimeReport(BaseHandler):

    def post(self):
        report_id = self.get_argument("reportId", default="")
        print report_id
