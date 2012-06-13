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

class Report2(object):
    def __init__(self, realtime = True):
        self.bla = 42
        
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
        drawing = Drawing(300, 220)
        lc = HorizontalLineChart()
    #    lc.strokeColor = colors.darkorange
    #    lc.x = -1
    #    lc.y = 8
        lc.width = 200
        lc.data = data
        lc.categoryAxis.visible = 0  # Make X-Axis Invisible
        lc.valueAxis.visible = 0 # Make Y-Axis Invisible
        lc.valueAxis.valueMin = 0  # Y axis Min value
        lc.valueAxis.valueMax = 2  # Y Axis Max Value
        lc.valueAxis.valueStep = 1  # Y Axis num of steps
        lc.lines[0].strokeWidth = 1.5 # Width of line graph
        lc.lines[0].strokeColor = colors.black  # Color of the Graph Line
        lc.lines[1].strokeWidth = 1.5 #Width of 2nd line graph
        drawing.add(lc)
        return drawing
       
    def page2(self, canvas):
        mentions, cityname = 35, "Amsterdam"
        percentage_increase = 35
        keyword, hour, date = "coffee", 1, "22/04/2012"
        twit_mentions, sentiments, followers = "+40%", "-20%", "-20%"
        #bg
        canvas.drawImage("reports/EMPTYPhilipsRealTimeReport2.png", 0, 0, 2479,\
            3507)
        #volume spike
        self.drawStringOrangeHelvetica(canvas, "VOLUME SPIKE : ", 54.17, 170, 3350, True)
        self.drawStringOrangeHelvetica(canvas, str(mentions) + "% more mentions",\
            54.17, 653, 3350, True)
        self.drawStringGrayHelvetica(canvas, "in", 54.17, 1180, 3350, False)
        self.drawStringOrangeHelvetica(canvas, cityname, 54.17, 1250, 3350, True)
        self.drawStringOrangeHelvetica(canvas, str(percentage_increase) + \
            "% increase", 64.22, 2020, 3280, True)
    
        self.drawStringGrayHelvetica(canvas, "concerning", 54.17, 170, 3250, False)
        self.drawStringOrangeHelvetica(canvas, str(keyword), 54.17, 450, 3250, False)
        self.drawStringGrayHelvetica(canvas, "than usual in " + str(hour) +\
            " hour " + date, 54.17, 610, 3250)
    
        # % mentions, sentiment, followers (in order)
        self.drawStringGrayHelvetica(canvas, twit_mentions, 90.65, 480, 2672, False, '#7cc576')
        # note that X-Axis varies for '+' & '-' as to align in same width
        self.drawStringGrayHelvetica(canvas, sentiments, 90.65, 499, 2452, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, followers, 90.65, 499, 2220, False, '#e68383')
    
        #Arrows
        canvas.drawImage("reports/green-up.png", 320, 2652, 100, 120)
        canvas.drawImage("reports/red-down.png", 320, 2402, 100, 120)
        canvas.drawImage("reports/red-down.png", 320, 2170, 100, 120)
    
        #Hottest Topics
        self.drawStringGrayHelvetica(canvas, 'Topics mention together with the word ' + keyword, 23.26, 379, 1780, False, '#000000')
        #Green
        self.drawStringGrayHelvetica(canvas, 'Machine', 80.65, 400, 1590, False, '#7cc576')
        self.drawStringGrayHelvetica(canvas, 'zwarte', 80.65, 645, 1490, False, '#7cc576')
        self.drawStringGrayHelvetica(canvas, 'excellent', 80.65, 470, 1410, False, '#7cc576')
        self.drawStringGrayHelvetica(canvas, 'pakje', 80.65, 400, 1300, False, '#7cc576')
        #Black
        self.drawStringGrayHelvetica(canvas, 'bruin', 80.65, 1200, 1590, False)
        self.drawStringGrayHelvetica(canvas, 'sens', 80.65, 1100, 1450, False)
        self.drawStringGrayHelvetica(canvas, 'saeco', 80.65, 1370, 1400, False)
        self.drawStringGrayHelvetica(canvas, 'reclame', 80.65, 1000, 1300, False)
        #Red
        self.drawStringGrayHelvetica(canvas, 'explode', 80.65, 1780, 1640, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, 'water', 80.65, 1840, 1540, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, 'pakje', 80.65, 1690, 1430, False, '#e68383')
        self.drawStringGrayHelvetica(canvas, 'kapot', 80.65, 1930, 1370, False, '#e68383')
    
        #Key influencers by Topic
        self.drawStringGrayHelvetica(canvas, 'pakje', 23.26, 476, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'zwarte', 23.26, 785, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'excellent', 23.26, 1087, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'machine', 23.26, 1409, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'bruin', 23.26, 1739, 864, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'sens', 23.26, 2055, 864, False, '#000000')
    
        # Sentiment Graphs
        graph_tuple = (1.5, 1.35, 1.37, 1.42, 1.22, 1.31, 1.1, .9, .80, .85, .75, .82, .69, .72, .55)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 398, 740)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 712, 740)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1021, 740)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1338, 740)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1661, 740)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1973, 740)
    
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 398, 332)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 712, 332)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1021, 332)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1338, 332)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1661, 332)
        self.drawSentimentGraph([graph_tuple]).drawOn(canvas, 1973, 332)
    
        #Key influencers by Topic Second Row
        self.drawStringGrayHelvetica(canvas, 'reclame', 23.26, 476, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'saeco', 23.26, 785, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'exploe', 23.26, 1087, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'water', 23.26, 1409, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'pakje', 23.26, 1739, 458, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'kapot', 23.26, 2055, 458, False, '#000000')
    
        #Influencer Info above Top Row
        self.drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 468, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 775, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 1087, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 1407, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 1727, 730, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 2043, 730, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 710, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 710, 30, 30)
    
        #Expertise Top Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, '44', 13.96, 490, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 515, 710, False) # 25 from expertise - left align
        self.drawStringGrayHelvetica(canvas, '44', 13.96, 797, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 822, 710, False)
        self.drawStringGrayHelvetica(canvas, '44', 13.96, 1109, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1134, 710, False)
        self.drawStringGrayHelvetica(canvas, '44', 13.96, 1429, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1454, 710, False)
        self.drawStringGrayHelvetica(canvas, '44', 13.96, 1749, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1774, 710, False)
        self.drawStringGrayHelvetica(canvas, '44', 13.96, 2065, 710, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Programming', 13.96, 2090, 710, False)
    
        #Influencer Info above Middle Row
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 468, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 775, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1087, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1407, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1727, 666, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 2043, 666, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 646, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 646, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 646, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 646, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 646, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 646, 30, 30)
    
        #Expertise Middle Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 490, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 515, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 797, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 822, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1109, 646, False, '#000000')
        self.drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1134, 646, False)
        self.drawStringGrayHelvetica(canvas, '21', 13.96, 1429, 646, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1454, 646, False)
        drawStringGrayHelvetica(canvas, '21', 13.96, 1749, 646, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1774, 646, False)
        drawStringGrayHelvetica(canvas, '21', 13.96, 2065, 646, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 2090, 646, False)
    
        #Influencer Info above Bottom Row
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 468, 604, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 775, 604, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1087, 604, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1407, 604, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1727, 604, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 2043, 604, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 584, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 584, 30, 30)
    
        #Expertise Bottom Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        drawStringGrayHelvetica(canvas, '49', 13.96, 490, 584, False, '#000000')
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 515, 584, False)
        drawStringGrayHelvetica(canvas, '49', 13.96, 797, 584, False, '#000000')
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 822, 584, False)
        drawStringGrayHelvetica(canvas, '49', 13.96, 1109, 584, False, '#000000')
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1134, 584, False)
        drawStringGrayHelvetica(canvas, '49', 13.96, 1429, 584, False, '#000000')
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1454, 584, False)
        drawStringGrayHelvetica(canvas, '49', 13.96, 1749, 584, False, '#000000')
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1774, 584, False)
        drawStringGrayHelvetica(canvas, '49', 13.96, 2065, 584, False, '#000000')
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 2090, 584, False)
    
        #Influencer Info above Top Row
        drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 468, 324, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 775, 324, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 1087, 324, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 1407, 324, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 1727, 324, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Jonathan Leroux', 18.61, 2043, 324, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 304, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 304, 30, 30)
    
        #Expertise Top Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        drawStringGrayHelvetica(canvas, '44', 13.96, 490, 304, False, '#000000')
        drawStringGrayHelvetica(canvas, '44', 13.96, 797, 304, False, '#000000')
        drawStringGrayHelvetica(canvas, '44', 13.96, 1109, 304, False, '#000000')
        drawStringGrayHelvetica(canvas, '44', 13.96, 1429, 304, False, '#000000')
        drawStringGrayHelvetica(canvas, '44', 13.96, 1749, 304, False, '#000000')
        drawStringGrayHelvetica(canvas, '44', 13.96, 2065, 304, False, '#000000')
    
        #Expertise Field Top Row
        drawStringGrayHelvetica(canvas, 'Programming', 13.96, 515, 304, False)
        drawStringGrayHelvetica(canvas, 'Programming', 13.96, 822, 304, False)
        drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1134, 304, False)
        drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1454, 304, False)
        drawStringGrayHelvetica(canvas, 'Programming', 13.96, 1774, 304, False)
        drawStringGrayHelvetica(canvas, 'Programming', 13.96, 2090, 304, False)
    
        #Influencer Info above Middle Row
        drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 468, 261, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 775, 261, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1087, 261, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1407, 261, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 1727, 261, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Stefan Lammert', 18.61, 2043, 261, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 241, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 241, 30, 30)
    
        #Expertise Middle Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        drawStringGrayHelvetica(canvas, '21', 13.96, 490, 241, False, '#000000')
        drawStringGrayHelvetica(canvas, '21', 13.96, 797, 241, False, '#000000')
        drawStringGrayHelvetica(canvas, '21', 13.96, 1109, 241, False, '#000000')
        drawStringGrayHelvetica(canvas, '21', 13.96, 1429, 241, False, '#000000')
        drawStringGrayHelvetica(canvas, '21', 13.96, 1749, 241, False, '#000000')
        drawStringGrayHelvetica(canvas, '21', 13.96, 2065, 241, False, '#000000')
    
        #Expertise Field Middle Row
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 515, 241, False)
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 822, 241, False)
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1134, 241, False)
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1454, 241, False)
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 1774, 241, False)
        drawStringGrayHelvetica(canvas, 'Social media', 13.96, 2090, 241, False)
    
        #Influencer Info above Bottom Row
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 468, 197, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 775, 197, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1087, 197, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1407, 197, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 1727, 197, False, '#000000')
        drawStringGrayHelvetica(canvas, 'Joost Deland', 18.61, 2043, 197, False, '#000000')
    
        #avatars
        canvas.drawImage("reports/TabulaMagica-1.png", 420, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 727, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1041, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1359, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1679, 177, 30, 30)
        canvas.drawImage("reports/TabulaMagica-1.png", 1995, 177, 30, 30)
    
        #Expertise Bottom Row (Left align --  22 from top row name, Top Align -- 2 from row ht)
        drawStringGrayHelvetica(canvas, '49', 13.96, 490, 177, False, '#000000')
        drawStringGrayHelvetica(canvas, '49', 13.96, 797, 177, False, '#000000')
        drawStringGrayHelvetica(canvas, '49', 13.96, 1109, 177, False, '#000000')
        drawStringGrayHelvetica(canvas, '49', 13.96, 1429, 177, False, '#000000')
        drawStringGrayHelvetica(canvas, '49', 13.96, 1749, 177, False, '#000000')
        drawStringGrayHelvetica(canvas, '49', 13.96, 2065, 177, False, '#000000')
    
        #Expertise Field Bottom Row
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 515, 177, False)
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 822, 177, False)
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1134, 177, False)
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1454, 177, False)
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 1774, 177, False)
        drawStringGrayHelvetica(canvas, 'ICT', 13.96, 2090, 177, False)

    def create(self, name):
        c = canvas.Canvas('report-page-2-%s.pdf' % name, pagesize=(2480, 3508), bottomup=1)
        self.page1(c)
        c.showPage()
        c.save()
        #os.system("open -a Preview report-page-1-%s.pdf" % name)

if __name__ == '__main__':
    report2 = Report2()
    report1.create("Philips")