from handlers.mainhandler import MainHandler
from handlers.users import *
from handlers.reports import *
import tornado
from settings import MEDIA_ROOT as static_path

url_patterns = [
    (r"/", MainHandler),
    #(r"/reports", ReportHandler),
    (r"/register", UserRegisterHandler),
    (r"/signout", UserSignout),
    (r"/newweeklyreport", NewWeeklyReport),
    (r"/manageexistingreports", ManageExistingReport),
    (r"/generatedweeklyreports", GeneratedWeeklyReports),
    (r"/newrealtimereport", NewRealTimeReport),
    (r"/manageexistingrules", ManageExistingRules),
    (r"/generatedrealtimereports", GeneratedRealTimeReports),
    (r"/addrule", AddRule),
    (r"/deletereport", DeleteReport),
    (r"/downloadreport", DownloadReport),
    (r"/newrealtimereportcrieria", RealTimeReportCrieria),
    (r"/deletetrigger", DeleteTrigger),
    (r"/downloadrealtimereport", DownloadRealTimeReport),
]
