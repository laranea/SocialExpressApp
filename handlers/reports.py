import tornado.ioloop
import tornado.web
from  tornado.template import Loader
from models.models import *
from connectdb import ConnectDB
from basehandler import BaseHandler
import subprocess


class NewWeeklyReport(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("newweeklyreport.html")


class ManageExistingReport(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        connection = ConnectDB()
        sql = "SELECT id FROM user WHERE email=" + self.current_user
        data = connection.connect(sql)
        for user in data:
            user_id = user[0]
            break
        sql = "SELECT * FROM reportcriteria WHERE creator_id=" + str(user_id)
        data = connection.connect(sql)
        if not data:
            data = ()
        self.render("manageexistingreports.html", list=data)


class GeneratedWeeklyReports(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        connection = ConnectDB()
        sql = "SELECT id FROM user WHERE email=" + self.current_user
        data = connection.connect(sql)
        for user in data:
            user_id = user[0]
            break
        sql = "SELECT * FROM reportcriteria WHERE creator_id=" + str(user_id) +\
             " AND file IS NOT NULL"
        data = connection.connect(sql)
        if not data:
            data = ()
        self.render("generatedweeklyreports.html", list=data)


class NewRealTimeReport(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("newrealtimereport.html")


class ManageExistingRules(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.get_userid()
        sql = "SELECT * FROM realtimereportcriteria WHERE creator_id= " + \
            user_id
        connection = ConnectDB()
        data = connection.connect(sql)
        if not data:
            data = ()
        self.render("manageexistingrules.html", list=data)


class GeneratedRealTimeReports(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        user_id = self.get_userid()
        triggerid = "SELECT id FROM realtimereportcriteria WHERE creator_id="\
         + user_id
        sql = "SELECT realtimereport.*, realtimereportcriteria.keyword FROM realtimereport "
        sql += " Left JOIN realtimereportcriteria ON "
        sql += " realtimereport.trigger_id=realtimereportcriteria.id"
        sql += " WHERE trigger_id IN (" + triggerid + ")"
        connection = ConnectDB()
        data = connection.connect(sql)
        print data
        if not data:
            data = ()
        self.render("generatedrealtimereports.html", list=data)


class AddRule(BaseHandler):

    def post(self):
        keyword = self.get_argument("keyword", default="")
        compare = self.get_argument("compare", default="")
        country = self.get_argument("country", default="")
        email = self.get_argument("emails", default="")
        connection = ConnectDB()
        sql = "SELECT id FROM user WHERE email=" + self.current_user
        data = connection.connect(sql)
        for user in data:
            user_id = user[0]
            break
        sql = "INSERT INTO reportcriteria (keyword, competitor, country,"
        sql += " mailing_list, creator_id) VALUES ('%s', '%s', '%s', '%s', '%d')" % (keyword, compare, country, email, user_id)
        data = connection.connect(sql, 1)
        
        list = ['python', 'engine/createreport.py']
        list.append("main_enterprise='ThinkMedia'")
        list.append("main_keyword=%" % keyword)
        list.append("competitor1_keyword=%" % compare)
        list.append("main_langage=nl")
        
        if country == 1:
            list.append("main_country='The Netherlands'")
        else:
            list.append("main_country='Belgium'")
        
        list.append("mail_to_list=%" % email)
        list.append("main_screen_name_list='ThinkMedia'")
        process = subprocess.Popen(list, shell=False, stdin=subprocess.PIPE)


class DeleteReport(BaseHandler):

    def post(self):
        report_id = self.get_argument("reportId", default="")
        sql = "DELETE FROM reportcriteria WHERE id=" + report_id
        connection = ConnectDB()
        data = connection.connect(sql, 1)
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

        connection = ConnectDB()
        sql = "SELECT id FROM user WHERE email=" + self.current_user
        data = connection.connect(sql)
        for user in data:
            user_id = user[0]
            break

        sql = "INSERT INTO realtimereportcriteria (keyword, sentiment, country"
        sql += ", language, changes, change_rate, mailing_list, creator_id) "
        sql += "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d') " % (keyword, sentiment, country, language, changes, change_rate, email, user_id)
        data = connection.connect(sql, 1)

        list = ['python', 'handlers/script.py']
<<<<<<< HEAD
        list.append('argument1')
        list.append('argument3')
        process = subprocess.Popen(list, shell=False)
#        print process.stdout.readline()
=======
        #list.append("--main_keyword='%'" % keyword)
        #list.append("--competitor1_data='%'" % )
        process = subprocess.Popen(list, shell=False, stdin=subprocess.PIPE)
>>>>>>> b1717b363174c44094cf84a3a1132ba7d816cbfb


class DeleteTrigger(BaseHandler):

    def post(self):
        trigger_id = self.get_argument("triggerId", default="")
        sql = "DELETE FROM realtimereportcriteria WHERE id=" + trigger_id
        connection = ConnectDB()
        data = connection.connect(sql, 1)


class DownloadRealTimeReport(BaseHandler):

    def post(self):
        report_id = self.get_argument("reportId", default="")
        print report_id
