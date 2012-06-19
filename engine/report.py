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
from reportlab.graphics.shapes import Drawing, Circle
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.lib.utils import ImageReader
from reportlab.graphics.widgets.markers import makeMarker
from positions import HorizontalChartNew
import numpy as np

#todo: increase font
class Report(object):

    def __init__(self, realtime=True):
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
        self.volumegraphs = [(5, 4, 300), (2, 900, 120), (700, 60, 5)]
        self.conversationlist = []
        self.top5positive = []
        self.top5negative = []
        self.graphcircleradius = 11
        self.followers_percentage = 0
        self.sentiment_percentage = 0
        self.mentions_percentage = 0
        self.keyword = "coffee"
        self.cityname = "Amsterdam"
        self.start_date = "22/04/2012"
        self.end_date = "29/04/2012"
        self.word_cloud = []
        self.key_infl = {}
        self.word_sent = {}
        self.word_klout = []
        self.optima = []

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
        lc.data = [data]
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

    def twitterMentionsGraph(self, data, canvas, yaxis_names=[]):
        drawing = Drawing(100, 300)
        #lc = HorizontalLineChart()
        lc = HorizontalChartNew()
        #lc.strokeColor = colors.darkorange
        lc.x = 0
        lc.y = 0
        lc.width = 1795  # Length of X-axis
        lc.height = 780  # Length of Y-axis
        lc.joinedLines = 1
        lc.data = data
        #print data[0]
        #catNames = string.split('8:00 8:30 9:00 9:30 10:00 10:30 11:00 11:30 12:00 12:30 13:00 13:30 14:00 14:30 13:00 13:30', ' ')
        catNames = yaxis_names
        lc.valueAxis.visible = 0  # Make Y-Axis Invisible
        lc.lines[0].strokeColor = colors.brown
    #    lc.inFill = 1
        lc.lines[1].strokeColor = colors.red
        lc.lines[2].strokeColor = colors.yellow
        lc.categoryAxis.categoryNames = catNames
        lc.categoryAxis.labels.boxAnchor = 'n'
        lc.categoryAxis.joinAxisMode = 'bottom'
        lc.valueAxis.valueMin = 0
        lc.valueAxis.valueMax = max(data[0] + data[1] + data[2]) * 2
        lc.valueAxis.valueStep = max(data[0] + data[1] + data[2]) / 10
        lc.lines[0].strokeWidth = 2.5
        '''lc.lines[0].symbol = makeMarker('FilledCircle')
        lc.lines[0].symbol.fillColor = colors.green
        lc.lines[0].symbol.strokeColor = colors.green
        lc.lines[0].symbol.size = 10'''
        lc.lines[1].strokeWidth = 2.5
        positions = lc.calcPositions_xy()
        self.optima = positions[0]
        drawing.add(lc)
        
        return drawing

    def createCircle(self, canvas, x, y, radius, color):
        canvas.setFillColor(colors.HexColor(color))
        canvas.setStrokeColor(colors.HexColor(color))
        canvas.circle(x, y, radius, 1, 1)

    def setFillStrokeColor(self, canvas, color):
        canvas.setFillColor(colors.HexColor(color))
        canvas.setStrokeColor(colors.HexColor(color))

    def splitSentence(self, sentence, isConversation=1):
        list = sentence.split()
        sentence_list = []
        first, second, third = '', '', ''
        # isConversation = 1 for TimeLine Conversation
        # isConversation = 0 for Positive & Negative Comments
        
        if len(list) < 9:
            sentence_list.append(sentence)
            sentence_list.append('')
            return sentence_list
            
        if len(list) < 18:
            isConversation = 0
            
        if isConversation:
            for i in range(9):
                try:
                    if i < 8:
                        first += list[i] + " "
                    else:
                        first += list[i]
                except:
                    break
            sentence_list.append(first)
            for i in range(9, 18):
                try:
                    if i < 17:
                        second += list[i] + " "
                    else:
                        second += list[i]
                except:
                    break
            sentence_list.append(second)
            for i in range(18, len(list)):
                try:
                    if i < len(list) - 1:
                        third += list[i] + " "
                    else:
                        third += list[i]
                except:
                    break
            sentence_list.append(third)
        else:
            for i in range(9):
                try:
                    if i < 8:
                        first += list[i] + " "
                    else:
                        first += list[i]
                except:
                    break
            sentence_list.append(first)
            for i in range(9, len(list)):
                try:
                    if i < len(list) - 1:
                        second += list[i] + " "
                    else:
                        second += list[i]
                except:
                    break
            sentence_list.append(second)
        return sentence_list

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
            if mentions >= 0:
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% more mentions", 54.17, 653, 3350, True)
            else:
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% less mentions", 54.17, 653, 3350, True)
        else:
            self.drawStringOrangeHelvetica(canvas, "SENTIMENT SPIKE : ", 54.17, 170, 3350, True)
            if mentions >= 0:
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
        self.twitterMentionsGraph(self.volumegraphs, canvas, time_list).drawOn(canvas, 365, 1880)

        #Create Circle on Twitter Mention Graph
        #self.createCircle(canvas, 400, 2000, self.graphcircleradius, "#00611C")

        colorList = ['#725E43', '#C04C4E', '#FFED5E', '#4FDF58', '#E2509F', '#47C4C9', '#F95D58', '#507AD2', '#F5AF21']
        index = 0
        for position in self.optima:
            # colorList - colors for each circle on the graph 
            try:
                color = colorList[index]
            except:
                color = '#0198E1'
            # X & Y positions returned is added with the coordinates of the graph    
            print self.optima
            self.createCircle(canvas, 365 + position[0], 1880 + position[1], 10, colorList[index % 9])
            index += 1

    #    twitterMentionsGraph([graph_tuple2]).drawOn(canvas, 365, 1880)

    #   Most Positive Conversations
        #TODO: calculate length for sentence
        i = 0

        for pos in self.top5positive:
            deltay_text = i * 124
            
            sentence_list = self.splitSentence(pos['text'], 0)
            self.drawStringGrayHelvetica(canvas, sentence_list[0], 26.07, 452, 687 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, sentence_list[1], 26.07, 452, 650 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, pos['username'], 26.07, 762, 650 - deltay_text, False)
#            self.drawStringGrayHelvetica(canvas, pos['text'], 26.07, 452, 687 - deltay_text, False, '#636363')
#            self.drawStringGrayHelvetica(canvas, pos['text'], 26.07, 452, 650 - deltay_text, False, '#636363')
#            self.drawStringGrayHelvetica(canvas, pos['username'], 26.07, 662, 650 - deltay_text, False)

            #avatar
            canvas.drawImage("reports/TabulaMagica-1.png", 300, 635 - deltay_text, 80, 80)

            i += 1

        #   Most Negative Coversations
        i = 0

        for neg in self.top5negative:
            deltay_text = i * 124
            
            sentence_list = self.splitSentence(neg['text'], 0)
            self.drawStringGrayHelvetica(canvas, sentence_list[0], 26.07, 1512, 687 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, sentence_list[1], 26.07, 1512, 650 - deltay_text, False, '#636363')
            self.drawStringGrayHelvetica(canvas, neg['username'], 26.07, 1965, 650 - deltay_text, False)
#            self.drawStringGrayHelvetica(canvas, neg['text'], 26.07, 1512, 687 - deltay_text, False, '#636363')
#            self.drawStringGrayHelvetica(canvas, neg['text'], 26.07, 1512, 650 - deltay_text, False, '#636363')
#            self.drawStringGrayHelvetica(canvas, neg['username'], 26.07, 1865, 650 - deltay_text, False)

            #avatar
            canvas.drawImage("reports/TabulaMagica-1.png", 1360, 635 - deltay_text, 80, 80)

            i += 1
        #circles ?i'll push

        # Timeline Time - Rect Box
        # Set Color to Rectangular Box
        #TODO: right points ?
        
        self.setFillStrokeColor(canvas, colorList[0])        
        canvas.roundRect(393, 1600, 105, 50, 2, stroke=1, fill=1)
        canvas.roundRect(393, 1453, 105, 50, 2, stroke=1, fill=1)
        canvas.roundRect(393, 1243, 105, 50, 2, stroke=1, fill=1)

        self.setFillStrokeColor(canvas, colorList[1])
        canvas.roundRect(992, 1565, 105, 50, 2, stroke=1, fill=1)
        canvas.roundRect(992, 1376, 105, 50, 2, stroke=1, fill=1)
        canvas.roundRect(992, 1177, 105, 50, 2, stroke=1, fill=1)

        self.setFillStrokeColor(canvas, colorList[2])
        canvas.roundRect(1503, 1565, 105, 50, 2, stroke=1, fill=1)
        canvas.roundRect(1503, 1378, 105, 50, 2, stroke=1, fill=1)
        canvas.roundRect(1503, 1177, 105, 50, 2, stroke=1, fill=1)

        #   Timeline Conversations
        try:
            self.drawStringGrayHelvetica(canvas, self.conversationlist[0]['hour_string'], 29.17, 410, 1616, False, colorList[0])
            self.drawStringGrayHelvetica(canvas, self.conversationlist[1]['hour_string'], 29.17, 410, 1468, False, colorList[0])
            self.drawStringGrayHelvetica(canvas, self.conversationlist[2]['hour_string'], 29.17, 410, 1258, False, colorList[0])
            #Second Column
            self.drawStringGrayHelvetica(canvas, self.conversationlist[3]['hour_string'], 29.17, 1005, 1577, False, colorList[1])
            self.drawStringGrayHelvetica(canvas, self.conversationlist[4]['hour_string'], 29.17, 1005, 1391, False, colorList[1])
            self.drawStringGrayHelvetica(canvas, self.conversationlist[5]['hour_string'], 29.17, 1005, 1195, False, colorList[1])
            #Third Column
            self.drawStringGrayHelvetica(canvas, self.conversationlist[6]['hour_string'], 29.17, 1518, 1577, False, colorList[2])
            self.drawStringGrayHelvetica(canvas, self.conversationlist[7]['hour_string'], 29.17, 1518, 1391, False, colorList[2])
            self.drawStringGrayHelvetica(canvas, self.conversationlist[8]['hour_string'], 29.17, 1518, 1195, False, colorList[2])

            self.drawStringGrayHelvetica(canvas, "", 29.17, 568, 1616, False)
        except:
            pass
        
        #First Column
        i = 0
         
        for conv in self.conversationlist:
            deltax_text = 0
            deltay_text = i * 112
            sentence_list = self.splitSentence(conv['text'], 1)       
        
            try:
                self.drawStringGrayHelvetica(canvas, sentence_list[0], 29.17, 570, 1463 - deltay_text, False)
                self.drawStringGrayHelvetica(canvas, sentence_list[1], 29.17, 570, 1433 - deltay_text, False)
                self.drawStringGrayHelvetica(canvas, sentence_list[2], 29.17, 570, 1404 - deltay_text, False)
            except:
                pass
            
            i += 1
            
            if i == 2 and deltax_text==0:
                i = 0
                deltax_text = 588
            elif i == 3 and deltax_text == 588:
                i = 0
                deltax_text = 514
   
    def page2(self, canvas):
        mentions, cityname = self.spike_percentage, self.spike_location
        percentage_increase = self.spike_percentage
        keyword, hour, date = self.keyword, 1, datetime.now().date()
        twit_mentions, sentiments, followers = round(self.mentions_percentage), round(self.sentiment_percentage), round(self.followers_percentage)
        #bg
        canvas.drawImage("reports/EMPTYPhilipsRealTimeReport2.png", 0, 0, 2479,\
            3507)        
        #volume spike
        if self.spike_kind == 'volume':
            self.drawStringOrangeHelvetica(canvas, "VOLUME SPIKE : ", 54.17, 170, 3350, True)
            if mentions >= 0:
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% more mentions", 54.17, 653, 3350, True)
            else:
                self.drawStringOrangeHelvetica(canvas, str(mentions) + "% less mentions", 54.17, 653, 3350, True)
        else:
            self.drawStringOrangeHelvetica(canvas, "SENTIMENT SPIKE : ", 54.17, 170, 3350, True)
            if mentions >= 0:
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
    
        # % mentions, sentiment, followers (in order)
        self.drawStringGrayHelvetica(canvas, str(round(self.mentions_percentage, 0)) + " %", 90.65, 480, 2672, False, '#7cc576')
        # note that X-Axis varies for '+' & '-' as to align in same width
        self.drawStringGrayHelvetica(canvas, str(round(self.sentiment_percentage, 0)) + " %", 90.65, 499, 2452, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, str(round(self.followers_percentage, 0)) + " %", 90.65, 499, 2220, False, '#e68383')
    
        #Arrows
        if self.mentions_percentage >= 0:
            canvas.drawImage("reports/green-up.png", 320, 2652, 100, 120)
        else:
            canvas.drawImage("reports/red-down.png", 320, 2652, 100, 120)
            
        if self.sentiment_percentage >= 0:
            canvas.drawImage("reports/green-up.png", 320, 2402, 100, 120)
        else:
            canvas.drawImage("reports/red-down.png", 320, 2402, 100, 120)
            
        #followers ?
        #canvas.drawImage("reports/red-down.png", 320, 2170, 100, 120)
        
        print self.word_cloud
        print self.word_klout
    
        #Hottest Topics
        self.drawStringGrayHelvetica(canvas, 'Topics mention together with the word ' + self.spike_keyword, 23.26, 379, 1780, False, '#000000')
        #Green
        self.drawStringGrayHelvetica(canvas, self.word_cloud[0][0], 72, 400, 1590, False, '#7cc576')
        self.drawStringGrayHelvetica(canvas, self.word_cloud[1][0], 72, 645, 1490, False, '#7cc576')
        self.drawStringGrayHelvetica(canvas, self.word_cloud[2][0], 72, 470, 1410, False, '#7cc576')
        self.drawStringGrayHelvetica(canvas, self.word_cloud[3][0], 72, 400, 1300, False, '#7cc576')
        #Black
        self.drawStringGrayHelvetica(canvas, self.word_cloud[4][0], 72, 1200, 1590, False)
        self.drawStringGrayHelvetica(canvas, self.word_cloud[5][0], 72, 1100, 1450, False)
        self.drawStringGrayHelvetica(canvas, self.word_cloud[6][0], 72, 1370, 1400, False)
        self.drawStringGrayHelvetica(canvas, self.word_cloud[7][0], 72, 1000, 1300, False)
        #Red
        self.drawStringGrayHelvetica(canvas, self.word_cloud[-1][0], 72, 1780, 1640, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, self.word_cloud[-2][0], 72, 1840, 1540, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, self.word_cloud[-3][0], 72, 1690, 1430, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, self.word_cloud[-4][0], 72, 1930, 1370, False, '#e68383')
    
        #Key influencers by Topic
        self.drawStringGrayHelvetica(canvas, self.word_klout[0][0], 23.26, 476, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[1][0], 23.26, 785, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[2][0], 23.26, 1087, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[3][0], 23.26, 1409, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[4][0], 23.26, 1739, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[5][0], 23.26, 2055, 864, False, '#000000')
    
        # Sentiment Graphs
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[0][0]])).drawOn(canvas, 398, 740)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[1][0]])).drawOn(canvas, 712, 740)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[2][0]])).drawOn(canvas, 1021, 740)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[3][0]])).drawOn(canvas, 1338, 740)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[4][0]])).drawOn(canvas, 1661, 740)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[5][0]])).drawOn(canvas, 1973, 740)
    
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[6][0]])).drawOn(canvas, 398, 332)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[7][0]])).drawOn(canvas, 712, 332)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[8][0]])).drawOn(canvas, 1021, 332)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[9][0]])).drawOn(canvas, 1338, 332)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[10][0]])).drawOn(canvas, 1661, 332)
        self.drawSentimentGraph(tuple(self.word_sent[self.word_klout[11][0]])).drawOn(canvas, 1973, 332)
    
        #Key influencers by Topic Second Row
        self.drawStringGrayHelvetica(canvas, self.word_klout[6][0], 23.26, 476, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[7][0], 23.26, 785, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[8][0], 23.26, 1087, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[9][0], 23.26, 1409, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[10][0], 23.26, 1739, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.word_klout[11][0], 23.26, 2055, 458, False, '#000000')
    
        #Influencer Info above Top Row
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[0][0]], 18.61, 468, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[1][0]], 18.61, 775, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[2][0]], 18.61, 1087, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[3][0]], 18.61, 1407, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[4][0]], 18.61, 1727, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[5][0]], 18.61, 2043, 730, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 710, 30, 30)
    
        #Expertise Top Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[0][1], 2)), 13.96, 490, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '', 13.96, 515, 710, False) # 25 from expertise - left align
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[1][1], 2)), 13.96, 797, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '', 13.96, 822, 710, False)
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[2][1], 2)), 13.96, 1109, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '', 13.96, 1134, 710, False)
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[3][1], 2)), 13.96, 1429, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '', 13.96, 1454, 710, False)
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[4][1], 2)), 13.96, 1749, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '', 13.96, 1774, 710, False)
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[5][1], 2)), 13.96, 2065, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '', 13.96, 2090, 710, False)
    
        '''
        #Influencer Info above Middle Row
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 468, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 775, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1087, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1407, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1727, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 2043, 666, False, '#000000')
    
        #avatars
        self.canvas.drawImage("reports/TabulaMagica-1.png", 420, 646, 30, 30)
        self.canvas.drawImage("reports/TabulaMagica-1.png", 727, 646, 30, 30)
        self.canvas.drawImage("reports/TabulaMagica-1.png", 1041, 646, 30, 30)
        self.canvas.drawImage("reports/TabulaMagica-1.png", 1359, 646, 30, 30)
        self.canvas.drawImage("reports/TabulaMagica-1.png", 1679, 646, 30, 30)
        self.canvas.drawImage("reports/TabulaMagica-1.png", 1995, 646, 30, 30)
    
        #Expertise Middle Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 490, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 515, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 797, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 822, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1109, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1134, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1429, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1454, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1749, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1774, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 2065, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 2090, 646, False)
    
        #Influencer Info above Bottom Row
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 468, 604, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 775, 604, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1087, 604, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1407, 604, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1727, 604, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 2043, 604, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 584, 30, 30)
    
        #Expertise Bottom Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 490, 584, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 515, 584, False)
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 797, 584, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 822, 584, False)
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 1109, 584, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1134, 584, False)
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 1429, 584, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1454, 584, False)
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 1749, 584, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1774, 584, False)
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 2065, 584, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 2090, 584, False)
        '''    
        #Influencer Info above Top Row
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[6][0]], 18.61, 468, 324, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[7][0]], 18.61, 775, 324, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[8][0]], 18.61, 1087, 324, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[9][0]], 18.61, 1407, 324, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[10][0]], 18.61, 1727, 324, False, '#000000')
        self.drawStringGrayHelvetica(canvas, self.key_infl[self.word_klout[11][0]], 18.61, 2043, 324, False, '#000000')
        
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 304, 30, 30)
    
        #Expertise Top Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[6][1], 2)), 13.96, 490, 304, False, '#000000')
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[7][1], 2)), 13.96, 797, 304, False, '#000000')
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[8][1], 2)), 13.96, 1109, 304, False, '#000000')
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[9][1], 2)), 13.96, 1429, 304, False, '#000000')
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[10][1], 2)), 13.96, 1749, 304, False, '#000000')
        self.drawStringGrayHelvetica(canvas, str(round(self.word_klout[11][1], 2)), 13.96, 2065, 304, False, '#000000')
        
        '''
        #Expertise Field Top Row
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 515, 304, False)
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 822, 304, False)
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1134, 304, False)
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1454, 304, False)
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1774, 304, False)
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 2090, 304, False)
    
        #Influencer Info above Middle Row
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 468, 261, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 775, 261, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1087, 261, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1407, 261, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1727, 261, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 2043, 261, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 241, 30, 30)
    
        #Expertise Middle Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 490, 241, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 797, 241, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1109, 241, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1429, 241, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1749, 241, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 2065, 241, False, '#000000')
    
        #Expertise Field Middle Row
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 515, 241, False)
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 822, 241, False)
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1134, 241, False)
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1454, 241, False)
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1774, 241, False)
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 2090, 241, False)
    
        #Influencer Info above Bottom Row
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 468, 197, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 775, 197, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1087, 197, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1407, 197, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1727, 197, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 2043, 197, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 177, 30, 30)
    
        #Expertise Bottom Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 490, 177, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 797, 177, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 1109, 177, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 1429, 177, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 1749, 177, False, '#000000')
        self.drawStringGrayHelvetica(canvas, '49', 13.96, 2065, 177, False, '#000000')
    
        #Expertise Field Bottom Row
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 515, 177, False)
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 822, 177, False)
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1134, 177, False)
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1454, 177, False)
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1774, 177, False)
        self.drawStringGrayHelvetica(canvas, 'ICT', 13.96, 2090, 177, False)
        '''
    def page3(self, canvas):
        #bg
        canvas.drawImage("reports/EMPTYPhilipsWeeklyConversationProblemsReport.png", 0, 0, 2479, 3507)

        #TODO: avatars
        #Avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 2230, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 2060, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 1880, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 1510, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 1325, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 1145, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 798, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 618, 125, 125)
        canvas.drawImage("reports/TabulaMagica-1.png", 368, 428, 125, 125)

        #Conversational Problems Report
        self.drawStringGrayHelvetica(canvas, "Weekly generated social media report", 54.17, 176, 3083, False)
        self.drawStringGrayHelvetica(canvas, "on", 54.17, 176, 3023, False)
        self.drawStringOrangeHelvetica(canvas, self.keyword, 54.17, 250, 3023, False)
        self.drawStringGrayHelvetica(canvas, "in", 54.17, 415, 3023, False)
        self.drawStringOrangeHelvetica(canvas, self.cityname, 54.17, 470, 3023, False)
        self.drawStringGrayHelvetica(canvas, "(between " + self.start_date + " and " + self.end_date + ")", 54.17, 760, 3023, False)

        #Problem Subjects
        self.drawStringGrayHelvetica(canvas, "Motor Break Down", 58.33, 371, 2435, True)
        self.drawStringGrayHelvetica(canvas, "Explosion", 58.33, 371, 1737, True)
        self.drawStringGrayHelvetica(canvas, "New Problem", 58.33, 371, 1060, True)

        #Problems
        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 2300, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 2250, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 2250, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 2124, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 2074, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 2074, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1940, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1890, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1890, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1572, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1522, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1522, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1388, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1338, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1338, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1212, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1162, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1162, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 848, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 798, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 798, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 680, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 630, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 630, False, '#000000', True)

        self.drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 488, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 438, False, '#555555')
        self.drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 438, False, '#000000', True)


    def create(self, name):
        c = canvas.Canvas('report-%s.pdf' % name, pagesize=(2480, 3508), bottomup=1, verbosity=1)
        self.page1(c)
        c.showPage()
        self.page2(c)
        c.showPage()
        #self.page3()
        #c.showPage()
        c.save()
        #os.system('/usr/bin/gnome-open report-%s.pdf' % name)
        os.system("open -a Preview report-%s.pdf" % name)

if __name__ == '__main__':
    report = Report()
    report.create("Philips")
