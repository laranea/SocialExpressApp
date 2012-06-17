import datetime

__author__ = 'kristof.leroux@gmail.com'

from pdfdocument.document import PDFDocument, cm, mm
from pdfdocument.elements import create_stationery_fn, ExampleStationery

class TestReport(object):
    def __init__(self):
        self.pdf = PDFDocument()

    def init_letter(self):
        self.pdf.init_letter(page_fn=ExampleStationery())

    def address(self):
        """
        ``address_key`` must be one of ``shipping`` and ``billing``.
        """

        if plata.settings.PLATA_REPORTING_ADDRESSLINE:
            self.pdf.address_head(u'SocialExpress bvba')

        self.pdf.address('Amsterdam')
        self.pdf.next_frame()

    def title(self, title=None):
        if not title:
            title = _('TestReport')
        self.pdf.h1(u'%s %s' % (title, datetime.now()))
        self.pdf.hr()

    def notes(self):
        if self.order.notes:
            self.pdf.spacer(10*mm)
            self.pdf.p(capfirst(_('notes')), style=self.pdf.style.bold)
            self.pdf.spacer(1*mm)
            self.pdf.p('blabla')


def main():
    report = TestReport()
    report.init_letter()
    report.address()
    report.title()
    self.pdf.generate()
    self.pdf



