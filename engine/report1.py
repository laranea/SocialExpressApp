'''
Created on May 21, 2012

@author: kristof
'''
import os
import math
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.utils import ImageReader

class Report1(object):
    def __init__(self, realtime = True):
        self.spike_kind = 'volume'
        self.spike_percentage = 35
        self.spike_moreorless = 'more'
        self.spike_location = 'Netherlands'
        self.spike_keyword = 'coffee'
        self.freq_time = 15
        self.sentimentgraph = [(1, 2, 3)]
        self.volumekeywords = ['c', 'd', 'e']
        self.volumebegintime = "08:00"
        self.volumeendtime = "15:30"
        self.volumegraph1 = (5, 4, 300)
        self.volumegraph2 = (2, 900, 120)
        self.volumegraph3 = (700, 60, 5)
        self.conversationlist = []
        self.top5positive = []
        self.top5negative = []

        
    def drawStringOrangeHelvetica(self, canvas, string, size, x, y, isBold=False):
        canvas.setFillColor(colors.darkorange)
    
        if not isBold:
            canvas.setFont('Helvetica', size)
        else:
            canvas.setFont('Helvetica-Bold', size)
    
        canvas.drawString(x, y, string)
    
    
    def drawStringGrayHelvetica(self, canvas, string, size, x, y, isBold=False, color=''):
        if color:
            canvas.setFillColor(colors.HexColor(color))
        else:
            canvas.setFillColor(colors.darkgray)
        if not isBold:
            canvas.setFont('Helvetica', size)
        else:
            canvas.setFont('Helvetica-Bold', size)
    
        canvas.drawString(x, y, string)
    
    
    def drawSentimentGraph(self, data):
        drawing = Drawing(300, 200)
        lc = HorizontalLineChart()
        #lc.strokeColor = colors.darkorange
        lc.x = 1
        lc.y = -3
        lc.height = 125
        lc.width = 300
        lc.height = 200
        lc.data = data
        catNames = ['time']
        lc.categoryAxis.categoryNames = catNames
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.valueAxis.valueMin = -3
        lc.valueAxis.valueMax = 3
        lc.valueAxis.valueStep = 1
        lc.lines[0].strokeWidth = 1.5
        lc.lines[1].strokeWidth = 1.5
        drawing.add(lc)
        return drawing
    
    def twitterMentionsGraph(self, data, yaxis_names = []):
        drawing = Drawing(100, 300)
        lc = HorizontalLineChart()
        #lc.strokeColor = colors.darkorange
        lc.x = 0
        lc.y = 0
        lc.width = 1795 # Length of X-axis
        lc.height = 780 # Length of Y-axis
        #lc.joinedLines = 1
        lc.data = data
        #catNames = string.split('8:00 8:30 9:00 9:30 10:00 10:30 11:00 11:30 12:00 12:30 13:00 13:30 14:00 14:30 13:00 13:30', ' ')
        catNames = yaxis_names
        lc.valueAxis.visible = 0 # Make Y-Axis Invisible
        lc.lines[0].strokeColor = colors.magenta
    #    lc.inFill = 1
        lc.lines[1].strokeColor = colors.lightblue
        #lc.lines[2].strokeColor = 
        lc.categoryAxis.categoryNames = catNames
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.categoryAxis.joinAxisMode = 'bottom'
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = max(data[0])
        lc.valueAxis.valueStep = max(data[0]) / 20
        lc.lines[0].strokeWidth = 2.5
        lc.lines[1].strokeWidth = 2.5
        drawing.add(lc)
        return drawing
    
    
    def page1(self, canvas):
        mentions, cityname = self.spike_percentage, self.spike_location
        percentage_increase = self.spike_percentage
        keyword, hour, date, twitter_mins = self.spike_keyword, 1, datetime.now().date(), self.freq_time
        
        start, end = self.volumebegintime, self.volumeendtime
        start_date = time = map(int, start.split(':'))
        end_date = map(int, end.split(':'))
        if end_date[0] < start_date[0]:
            end_date[0] += 12
        time_list = [start]
        if end_date[1] and not start_date[1]:
            loop_count = range((end_date[0] - start_date[0]) * 2 + 1)
        else:
            loop_count = range((end_date[0] - start_date[0]) * 2)
        for i in loop_count:
            if time[1]:
                time_list.append(str(time[0] + 1) + ":00")
                time[0] += 1
                time[1] = 0
            else:
                time_list.append(str(time[0]) + ":30")
                time[1] = 30 
                
        #bg
        canvas.drawImage("reports/EMPTYPhilipsRealTimeReport1.png", 0, 0,\
            2479, 3507)
        #volume spike
        if self.spike_kind == 'volume':
            self.drawStringOrangeHelvetica(canvas, "VOLUME SPIKE : ", 54.17, 170, 3350, True)
            if self.spike_moreorless == 'more':
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% more mentions", 54.17, 653, 3350, True)
            else:
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% less mentions", 54.17, 653, 3350, True)
        else: 
            self.drawStringOrangeHelvetica(canvas, "SENTIMENT SPIKE : ", 54.17, 170, 3350, True)
            if self.spike_moreorless == 'more':
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% sentiment increase", 54.17, 653, 3350, True)
            else:
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% sentiment decrease", 54.17, 653, 3350, True)
               #TODO: dynamic change!
        self.drawStringGrayHelvetica(canvas, "in", 54.17, 1220, 3350, False)
        self.drawStringOrangeHelvetica(canvas, cityname, 54.17, 1290, 3350, True)
    
        self.drawStringOrangeHelvetica(canvas, str(self.spike_percentage) + \
            "% increase", 64.22, 1920, 3280, True)
    
        self.drawStringGrayHelvetica(canvas, "concerning", 54.17, 170, 3250, False)
        self.drawStringOrangeHelvetica(canvas, self.spike_keyword, 54.17, 450, 3250, False)
        #self.drawStringGrayHelvetica(canvas, "than usual in " + str(hour) +\
        #    " hour " + date, 54.17, 610, 3250)
    
        self.drawStringOrangeHelvetica(canvas, "Every " + str(self.freq_time) + " seconds someone is twittering..", 25, 484, 2627)
        
        #keyword related to legends
        self.drawStringGrayHelvetica(canvas, self.volumekeywords[0], 26.07, 970, 2435, False)
        self.drawStringGrayHelvetica(canvas, self.volumekeywords[1], 26.07, 970, 2477, False)
        self.drawStringGrayHelvetica(canvas, self.volumekeywords[2], 26.07, 970, 2523, False)
    
        
        self.drawSentimentGraph(self.sentimentgraph).drawOn(canvas, 450, 2300)
    
    #    graph_tuple = (1000, 1200, 1250, 1500, 2000, 3200, 4600, 2100, 4000, 6100, 5700, 7000\
    #        , 6900, 7900, 8000, 10200, 9500, 11000)
        graph_tuple = ( 2000, 3200, 4600, 4800, 5100, 6100, 5700, 7000 , 6900, 7900, 8000, 10200, 10000, 10500, 10650, 11000)
        graph_tuple2 = (700, 1000, 2500, 3000, 3400, 3700, 4600, 5100, 5700 , 5800, 5900, 6000, 6400, 6800, 7700, 8100)
        self.twitterMentionsGraph([self.volumegraph1], time_list).drawOn(canvas, 365, 1880)
    #    twitterMentionsGraph([graph_tuple2]).drawOn(canvas, 365, 1880)
    
    #   Most Positive Conversations
        #TODO: calculate length for sentence
        i = 0
        
        for pos in self.top5positive:
            deltax_text = i * 0
            deltay_text = i * 124
            deltay_space = i * (37 + 5)
            self.drawStringGrayHelvetica(canvas, pos['text'], 26.07, 452, 687 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, pos['text'], 26.07, 452, 650 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, pos['username'], 26.07, 662, 650 - deltay_text, False)
    
            #avatar
            canvas.drawImage("reports/TabulaMagica-1.png", 300, 635 - deltay_text, 80, 80)

            i += 1

    
        #   Most Negative Coversations
        i = 0
        
        for neg in self.top5negative:
            deltax_text = i * 0
            deltay_text = i * 124
            deltay_space = i * (37 + 5)
            self.drawStringGrayHelvetica(canvas, neg['text'], 26.07, 1512, 687 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, neg['text'], 26.07, 1512, 650 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, neg['username'], 26.07, 1865, 650 - deltay_text, False)
    
            #avatar
            canvas.drawImage("reports/TabulaMagica-1.png", 1360, 635 - deltay_text, 80, 80)

            i += 1

        #   Timeline Conversations
        #First Column
        self.drawStringGrayHelvetica(canvas, self.conversationlist[0]['hour_string'], 29.17, 410, 1616, False, '#FFFFFF')
        self.drawStringGrayHelvetica(canvas, self.conversationlist[1]['hour_string'], 29.17, 410, 1468, False, '#FFFFFF')
        self.drawStringGrayHelvetica(canvas, self.conversationlist[2]['hour_string'], 29.17, 410, 1258, False, '#FFFFFF')
        #Second Column
        self.drawStringGrayHelvetica(canvas, self.conversationlist[3]['hour_string'], 29.17, 1005, 1577, False, '#FFFFFF')
        self.drawStringGrayHelvetica(canvas, self.conversationlist[4]['hour_string'], 29.17, 1005, 1391, False, '#FFFFFF')
        self.drawStringGrayHelvetica(canvas, self.conversationlist[5]['hour_string'], 29.17, 1005, 1195, False, '#FFFFFF')
        #Third Column
        self.drawStringGrayHelvetica(canvas, self.conversationlist[6]['hour_string'], 29.17, 1518, 1577, False, '#FFFFFF')
        self.drawStringGrayHelvetica(canvas, self.conversationlist[7]['hour_string'], 29.17, 1518, 1391, False, '#FFFFFF')
        self.drawStringGrayHelvetica(canvas, self.conversationlist[8]['hour_string'], 29.17, 1518, 1195, False, '#FFFFFF')

        self.drawStringGrayHelvetica(canvas, "", 29.17, 568, 1616, False)
        
        self.drawStringGrayHelvetica(canvas, "''Coffee Machine exploded,", 29.17, 570, 1463, False)
        self.drawStringGrayHelvetica(canvas, "what is this? Can not", 29.17, 570, 1433, False)
        self.drawStringGrayHelvetica(canvas, "believe what is happenin!!''", 29.17, 570, 1404, False)
        
        self.drawStringGrayHelvetica(canvas, "My Senseo coffee doesn't", 29.17, 570, 1251, False)
        self.drawStringGrayHelvetica(canvas, "work anymore :(( there goes", 29.17, 570, 1221, False)
        self.drawStringGrayHelvetica(canvas, "my happy day", 29.17, 570, 1191, False)
        
        self.drawStringGrayHelvetica(canvas, "Hey @Philips Why does", 29.17, 1158, 1577, False)
        self.drawStringGrayHelvetica(canvas, "my brand new Senseo", 29.17, 1158, 1547, False)
        self.drawStringGrayHelvetica(canvas, "explode?", 29.17, 1158, 1517, False)
        
        self.drawStringGrayHelvetica(canvas, "OMG senseo sucks!", 29.17, 1158, 1391, False)
        self.drawStringGrayHelvetica(canvas, "Keeps giving me warm", 29.17, 1158, 1361, False)
        self.drawStringGrayHelvetica(canvas, "water instead of coffee", 29.17, 1158, 1331, False)
        
        self.drawStringGrayHelvetica(canvas, "Philips is not answering", 29.17, 1158, 1195, False)
        self.drawStringGrayHelvetica(canvas, "my questions concerning", 29.17, 1158, 1165, False)
        self.drawStringGrayHelvetica(canvas, "my broken coffee mach..", 29.17, 1158, 1135, False)
        
        self.drawStringGrayHelvetica(canvas, "I have no faith in Philips", 29.17, 1672, 1577, False)
        self.drawStringGrayHelvetica(canvas, "any more, my Senseo", 29.17, 1672, 1547, False)
        self.drawStringGrayHelvetica(canvas, "is fucked up!", 29.17, 1672, 1517, False)
        
        self.drawStringGrayHelvetica(canvas, "@PhilipsNL Why does", 29.17, 1672, 1391, False)
        self.drawStringGrayHelvetica(canvas, "my brand new Senseo", 29.17, 1672, 1361, False)
        self.drawStringGrayHelvetica(canvas, "explode? Unbelievable", 29.17, 1672, 1331, False)
        
        self.drawStringGrayHelvetica(canvas, "Philips is not", 29.17, 1672, 1195, False)
        self.drawStringGrayHelvetica(canvas, "answering my questions", 29.17, 1672, 1165, False)
        self.drawStringGrayHelvetica(canvas, "bad customer service", 29.17, 1672, 1135, False)    

    def create(self, name):
        c = canvas.Canvas('report-page-1-%s.pdf' % name, pagesize=(2480, 3508), bottomup=1)
        self.page1(c)
        c.showPage()
        c.save()
        #os.system("open -a Preview report-page-1-%s.pdf" % name)

if __name__ == '__main__':
    report1 = Report1()
    report1.create("Philips")    