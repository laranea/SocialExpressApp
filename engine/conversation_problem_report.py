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


def drawStringGrayHelvetica(canvas, string, size, x, y, isBold=False, color='', isitalic=False):
    if color:
        canvas.setFillColor(colors.HexColor(color))
    else:
        canvas.setFillColor(colors.darkgray)
    if isitalic:
        canvas.setFont('Times-Italic', size)
    elif not isBold:
        canvas.setFont('Helvetica', size)
    else:
        canvas.setFont('Helvetica-Bold', size)
    canvas.drawString(x, y, string)


def generate_pdf(canvas):
    keyword, cityname = "coffee", "Amsterdam"
    start_date, end_date = "22/04/2012", "29/04/2012"
    #bg
    canvas.drawImage("reports/EMPTYPhilipsWeeklyConversationProblemsReport.png",\
        0, 0, 2479, 3507)

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
    drawStringGrayHelvetica(canvas, "Weekly generated social media report", 54.17, 176, 3083, False)
    drawStringGrayHelvetica(canvas, "on", 54.17, 176, 3023, False)
    drawStringOrangeHelvetica(canvas, keyword, 54.17, 250, 3023, False)
    drawStringGrayHelvetica(canvas, "in", 54.17, 415, 3023, False)
    drawStringOrangeHelvetica(canvas, cityname, 54.17, 470, 3023, False)
    drawStringGrayHelvetica(canvas, "(between " + start_date + " and " + end_date +")", 54.17, 760, 3023, False)

    #Problem Subjects
    drawStringGrayHelvetica(canvas, "Motor Break Down", 58.33, 371, 2435, True)
    drawStringGrayHelvetica(canvas, "Explosion", 58.33, 371, 1737, True)
    drawStringGrayHelvetica(canvas, "New Problem", 58.33, 371, 1060, True)

    #Problems
    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 2300, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 2250, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 2250, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 2124, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 2074, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 2074, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1940, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1890, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1890, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1572, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1522, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1522, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1388, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1338, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1338, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 1212, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 1162, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 1162, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 848, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 798, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 798, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 680, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 630, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 630, False, '#000000', True)

    drawStringGrayHelvetica(canvas, "'What is going on with my coffee machine? Seriously, cannot believe this is", 41.67, 593, 488, False, '#555555')
    drawStringGrayHelvetica(canvas, "happening!'", 41.67, 593, 438, False, '#555555')
    drawStringGrayHelvetica(canvas, "Ivo Minjauw", 41.67, 825, 438, False, '#000000', True)

canvas = canvas.Canvas('coversation-report.pdf', pagesize=(2480, 3508),\
    bottomup=1)
generate_pdf(canvas)
canvas.showPage()
canvas.save()



print "coversation report created"
#open pdf file created
os.system("open -a Preview coversation-report.pdf")
#open pdf file created Ubutnu
#os.system('/usr/bin/gnome-open coversation-report.pdf')
