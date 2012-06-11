'''
Created on May 21, 2012

@author: kristof
'''
import os
import math
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import string


def drawStringOrangeHelvetica(canvas, string, size, x, y, isBold=False):
    canvas.setFillColor(colors.darkorange)

    if not isBold:
        canvas.setFont('Helvetica', size)
    else:
        canvas.setFont('Helvetica-Bold', size)

    canvas.drawString(x, y, string)


def drawStringGrayHelvetica(canvas, string, size, x, y, isBold=False, color=''):
    if color:
        canvas.setFillColor(colors.HexColor(color))
    else:
        canvas.setFillColor(colors.darkgray)
    if not isBold:
        canvas.setFont('Helvetica', size)
    else:
        canvas.setFont('Helvetica-Bold', size)

    canvas.drawString(x, y, string)


def drawSentimentGraph(data):
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

def twitterMentionsGraph(data, yaxis_names = []):
    drawing = Drawing(100, 300)
    lc = HorizontalLineChart()
    #lc.strokeColor = colors.darkorange
    lc.x = 0
    lc.y = 0
    lc.width = 1795 # Length of X-axis
    lc.height = 780 # Length of Y-axis
#    lc.joinedLines = 1
    lc.data = data
#    catNames = string.split('8:00 8:30 9:00 9:30 10:00 10:30 11:00 11:30 12:00 12:30 13:00 13:30 14:00 14:30 13:00 13:30', ' ')
    catNames = yaxis_names
    lc.valueAxis.visible = 0 # Make Y-Axis Invisible
    lc.lines[0].strokeColor = colors.magenta
#    lc.inFill = 1
    print dir(lc.categoryAxis)
#    lc.categoryAxis.scale = 1
    lc.lines[1].strokeColor = colors.lightblue
    lc.categoryAxis.categoryNames = catNames
    lc.categoryAxis.labels.boxAnchor = 'n'
    lc.categoryAxis.joinAxisMode = 'bottom'
    lc.valueAxis.valueMin = 0
    lc.valueAxis.valueMax = 11000
    lc.valueAxis.valueStep = 500
    lc.lines[0].strokeWidth = 2.5
    lc.lines[1].strokeWidth = 2.5
    drawing.add(lc)
    return drawing


def page1(canvas):
    mentions, cityname = 35, "Amsterdam"
    percentage_increase = 35
    keyword, hour, date, twitter_mins = "coffee", 1, "22/04/2012", 15
    start, end = "8:00", "15:30"
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
    drawStringOrangeHelvetica(canvas, "VOLUME SPIKE : ", 54.17, 170, 3350, True)
    drawStringOrangeHelvetica(canvas, str(mentions) + "% more mentions",\
        54.17, 653, 3350, True)
    drawStringGrayHelvetica(canvas, "in", 54.17, 1180, 3350, False)
    drawStringOrangeHelvetica(canvas, cityname, 54.17, 1250, 3350, True)

    drawStringOrangeHelvetica(canvas, str(percentage_increase) + \
        "% increase", 64.22, 2020, 3280, True)

    drawStringGrayHelvetica(canvas, "concerning", 54.17, 170, 3250, False)
    drawStringOrangeHelvetica(canvas, str(keyword), 54.17, 450, 3250, False)
    drawStringGrayHelvetica(canvas, "than usual in " + str(hour) +\
        " hour " + date, 54.17, 610, 3250)

    drawStringOrangeHelvetica(canvas, "Every " + str(twitter_mins) +\
        " minutes someone is twittering..", 25, 484, 2627)

    # Circles -  Legends - number of graph lines
#    canvas.circle(947, 2445, 11, 1)

    #keyword related to legends
    drawStringGrayHelvetica(canvas, "JURA", 26.07, 970, 2435, False)
    drawStringGrayHelvetica(canvas, "NESPRESSO", 26.07, 970, 2477, False)
    drawStringGrayHelvetica(canvas, "SENSEO", 26.07, 970, 2523, False)

    drawSentimentGraph([(math.sin(0), math.sin(30), math.sin(45), math.sin(90),\
        math.sin(120), math.sin(150), math.sin(180))]).drawOn(canvas, 450, 2300)

#    graph_tuple = (1000, 1200, 1250, 1500, 2000, 3200, 4600, 2100, 4000, 6100, 5700, 7000\
#        , 6900, 7900, 8000, 10200, 9500, 11000)
    graph_tuple = ( 2000, 3200, 4600, 4800, 5100, 6100, 5700, 7000 , 6900, 7900, 8000, 10200, 10000, 10500, 10650, 11000)
    graph_tuple2 = (700, 1000, 2500, 3000, 3400, 3700, 4600, 5100, 5700 , 5800, 5900, 6000, 6400, 6800, 7700, 8100)
    twitterMentionsGraph([graph_tuple, graph_tuple2], time_list).drawOn(canvas, 365, 1880)
#    twitterMentionsGraph([graph_tuple2]).drawOn(canvas, 365, 1880)

#   Most Positive Conversations
    drawStringGrayHelvetica(canvas, "'Philips is doing great, wow! Very nice customer service ", 26.07, 452, 687, False, '#636363')
    drawStringGrayHelvetica(canvas, "concerning coffee machines'", 26.07, 452, 650, False, '#636363')
    drawStringGrayHelvetica(canvas, "Jones Michael", 26.07, 786, 650, False)

    drawStringGrayHelvetica(canvas, "'Amazing stuff going on at philips coffee", 26.07, 452, 563, False, '#636363')
    drawStringGrayHelvetica(canvas, "bla bla you know what i mean'", 26.07, 452, 526, False, '#636363')
    drawStringGrayHelvetica(canvas, "Toon Dewinter", 26.07, 805, 526, False)

    drawStringGrayHelvetica(canvas, "'Very nice things goin on with the Senseo coffee", 26.07, 452, 437, False, '#636363')
    drawStringGrayHelvetica(canvas, "kind of things'", 26.07, 452, 400, False, '#636363')
    drawStringGrayHelvetica(canvas, "Lisa Michels", 26.07, 615, 400, False)

    drawStringGrayHelvetica(canvas, "'Wow! Very nice customer service", 26.07, 452, 320, False, '#636363')
    drawStringGrayHelvetica(canvas, "concerning coffee machines'", 26.07, 452, 283, False, '#636363')
    drawStringGrayHelvetica(canvas, "Michel Jones", 26.07, 786, 283, False)

    drawStringGrayHelvetica(canvas, "'Nice Timigs man'", 26.07, 452, 196, False, '#636363')
    drawStringGrayHelvetica(canvas, "Thomas Dewinter", 26.07, 662, 196, False)

    #avatar
    canvas.drawImage("reports/TabulaMagica-1.png", 300, 635, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 300, 511, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 300, 385, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 300, 268, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 300, 144, 80, 80)

#   Most Negative Coversations
    drawStringGrayHelvetica(canvas, "'Philips is doing great, wow! Very nice customer service ", 26.07, 1512, 687, False, '#636363')
    drawStringGrayHelvetica(canvas, "concerning coffee machines'", 26.07, 1512, 650, False, '#636363')
    drawStringGrayHelvetica(canvas, "Jones Michael", 26.07, 1846, 650, False)

    drawStringGrayHelvetica(canvas, "'Amazing stuff going on at philips coffee", 26.07, 1512, 563, False, '#636363')
    drawStringGrayHelvetica(canvas, "bla bla you know what i mean'", 26.07, 1512, 526, False, '#636363')
    drawStringGrayHelvetica(canvas, "Toon Dewinter", 26.07, 1865, 526, False)

    drawStringGrayHelvetica(canvas, "'Very nice things goin on with the Senseo coffee", 26.07, 1512, 437, False, '#636363')
    drawStringGrayHelvetica(canvas, "kind of things'", 26.07, 1512, 400, False, '#636363')
    drawStringGrayHelvetica(canvas, "Lisa Michels", 26.07, 1675, 400, False)

    drawStringGrayHelvetica(canvas, "'Wow! Very nice customer service", 26.07, 1512, 320, False, '#636363')
    drawStringGrayHelvetica(canvas, "concerning coffee machines'", 26.07, 1512, 283, False, '#636363')
    drawStringGrayHelvetica(canvas, "Michel Jones", 26.07, 1846, 283, False)

    drawStringGrayHelvetica(canvas, "'Nice Timigs man'", 26.07, 1512, 196, False, '#636363')
    drawStringGrayHelvetica(canvas, "Thomas Dewinter", 26.07, 1722, 196, False, '#a1a1a1')

    #avatar
    canvas.drawImage("reports/TabulaMagica-1.png", 1360, 635, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 1360, 511, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 1360, 385, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 1360, 268, 80, 80)
    canvas.drawImage("reports/TabulaMagica-1.png", 1360, 144, 80, 80)

#   Timeline Conversations
    drawStringGrayHelvetica(canvas, "", 29.17, 568, 1616, False)
    drawStringGrayHelvetica(canvas, "''Coffee Machine exploded,", 29.17, 570, 1463, False)
    drawStringGrayHelvetica(canvas, "what is this? Can not", 29.17, 570, 1433, False)
    drawStringGrayHelvetica(canvas, "believe what is happenin!!''", 29.17, 570, 1404, False)
    drawStringGrayHelvetica(canvas, "My Senseo coffee doesn't", 29.17, 570, 1251, False)
    drawStringGrayHelvetica(canvas, "work anymore :(( there goes", 29.17, 570, 1221, False)
    drawStringGrayHelvetica(canvas, "my happy day", 29.17, 570, 1191, False)
    drawStringGrayHelvetica(canvas, "Hey @Philips Why does", 29.17, 1158, 1577, False)
    drawStringGrayHelvetica(canvas, "my brand new Senseo", 29.17, 1158, 1547, False)
    drawStringGrayHelvetica(canvas, "explode?", 29.17, 1158, 1517, False)
    drawStringGrayHelvetica(canvas, "OMG senseo sucks!", 29.17, 1158, 1391, False)
    drawStringGrayHelvetica(canvas, "Keeps giving me warm", 29.17, 1158, 1361, False)
    drawStringGrayHelvetica(canvas, "water instead of coffee", 29.17, 1158, 1331, False)
    drawStringGrayHelvetica(canvas, "Philips is not answering", 29.17, 1158, 1195, False)
    drawStringGrayHelvetica(canvas, "my questions concerning", 29.17, 1158, 1165, False)
    drawStringGrayHelvetica(canvas, "my broken coffee mach..", 29.17, 1158, 1135, False)
    drawStringGrayHelvetica(canvas, "I have no faith in Philips", 29.17, 1672, 1577, False)
    drawStringGrayHelvetica(canvas, "any more, my Senseo", 29.17, 1672, 1547, False)
    drawStringGrayHelvetica(canvas, "is fucked up!", 29.17, 1672, 1517, False)
    drawStringGrayHelvetica(canvas, "@PhilipsNL Why does", 29.17, 1672, 1391, False)
    drawStringGrayHelvetica(canvas, "my brand new Senseo", 29.17, 1672, 1361, False)
    drawStringGrayHelvetica(canvas, "explode? Unbelievable", 29.17, 1672, 1331, False)
    drawStringGrayHelvetica(canvas, "Philips is not", 29.17, 1672, 1195, False)
    drawStringGrayHelvetica(canvas, "answering my questions", 29.17, 1672, 1165, False)
    drawStringGrayHelvetica(canvas, "bad customer service", 29.17, 1672, 1135, False)

#   Time line Hours
    #First Column
    drawStringGrayHelvetica(canvas, "13:30", 29.17, 410, 1616, False, '#FFFFFF')
    drawStringGrayHelvetica(canvas, "14:00", 29.17, 410, 1468, False, '#FFFFFF')
    drawStringGrayHelvetica(canvas, "14:30", 29.17, 410, 1258, False, '#FFFFFF')
    #Second Column
    drawStringGrayHelvetica(canvas, "16:00", 29.17, 1005, 1577, False, '#FFFFFF')
    drawStringGrayHelvetica(canvas, "15:30", 29.17, 1005, 1391, False, '#FFFFFF')
    drawStringGrayHelvetica(canvas, "15:00", 29.17, 1005, 1195, False, '#FFFFFF')
    #Third Column
    drawStringGrayHelvetica(canvas, "16:30", 29.17, 1518, 1577, False, '#FFFFFF')
    drawStringGrayHelvetica(canvas, "17:00", 29.17, 1518, 1391, False, '#FFFFFF')
    drawStringGrayHelvetica(canvas, "17:30", 29.17, 1518, 1195, False, '#FFFFFF')



canvas = canvas.Canvas('report-page-latest.pdf', pagesize=(2480, 3508),\
    bottomup=1)
page1(canvas)
canvas.showPage()
canvas.save()



print "page 1 created."
#open pdf file created
os.system("open -a Preview report-page-latest.pdf")
#open pdf file created Ubuntu
#os.system('/usr/bin/gnome-open report-page-latest.pdf')
