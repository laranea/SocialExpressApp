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
       
def drawStringOrangeHelvetica(canvas, string, size, x, y, isBold=False):
    canvas.setFillColor(colors.darkorange)
    
    if not isBold:
        canvas.setFont('Helvetica', size)
    else:
        canvas.setFont('Helvetica-Bold', size)
         
    canvas.drawString(x, y, string)

def drawStringGrayHelvetica(canvas, string, size, x, y, isBold=False):
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
    
    
def page1(canvas):
    #bg
    canvas.drawImage("reports/EMPTYPhilipsRealTimeReport1.png", 0, 0, 2479, 3507)
    #volume spike
    drawStringOrangeHelvetica(canvas, "VOLUME SPIKE : ", 54.17, 170, 3350, True) 
    drawStringOrangeHelvetica(canvas, "xx% more mentions", 54.17, 653, 3350, True)
    drawStringGrayHelvetica(canvas, "in", 54.17, 1180, 3350, False)
    drawStringOrangeHelvetica(canvas, "CITY_NAME", 54.17, 1250, 3350, True)
    
    drawStringOrangeHelvetica(canvas, "xx%", 64.22, 2250, 3324, True)
    drawStringOrangeHelvetica(canvas, "increase", 64.22, 2120, 3280, True)
    
    drawStringGrayHelvetica(canvas, "concerning", 54.17, 170, 3250, False)
    drawStringOrangeHelvetica(canvas, "'MAIN_KEYWORD'", 54.17, 450, 3250, False)
    drawStringGrayHelvetica(canvas, "than usual in x hour (dd/mm/yyyy)", 54.17, 950, 3250)
    
    drawStringOrangeHelvetica(canvas, "Every xx minutes someone is twittering..", 25, 484, 2627)
    
    drawSentimentGraph([(math.sin(0), math.sin(30), math.sin(45), math.sin(90), math.sin(120), math.sin(150), math.sin(180))]).drawOn(canvas, 450, 2300)
    
    
def page2(canvas):
    #bg
    canvas.drawImage("reports/EMPTYPhilipsRealTimeReport2.png", 0, 0, 2479, 3507)


canvas = canvas.Canvas('report-page1.pdf',pagesize=(2480, 3508), bottomup=1)
page1(canvas)
canvas.showPage()
canvas.save()
print "page 1 created."
os.system("open -a Preview report-page1.pdf")


                       
