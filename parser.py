import zipfile
import xml.dom.minidom
import re
import subprocess
import os
import time


class XLSXReader:
    rows = []

    def _nodeText(self, node):
        return "".join(t.nodeValue for t in node.childNodes if t.nodeType == t.TEXT_NODE)

    def _get_col_num(self, col):

        strpart = col.attributes['r'].value
        colnum = re.sub('[^A-Z]', '', strpart.upper().strip())

        c = 0
        for char in colnum:
            c += ord(char)

        c -= (65) # ASCII to number

        print("Colnum for '%s' is %s" % (strpart, c))

        return c


    def __init__(self, filename):
        shared_strings = []
        self.rows = []
        myFile = zipfile.ZipFile(filename)

        # Read the shared strings file.
        share = xml.dom.minidom.parseString(myFile.read('xl/sharedStrings.xml'))
        j = share.getElementsByTagName("t")

        for node in j:
            shared_strings.append(self._nodeText(node))

        sheet = xml.dom.minidom.parseString(myFile.read('xl/worksheets/sheet1.xml'))
        sheetrows = sheet.getElementsByTagName("row")
        for row in sheetrows:
            cols = row.getElementsByTagName("c")

            largest_col_num = 0
            for col in cols:
                colnum = self._get_col_num(col)
                if colnum > largest_col_num:
                    largest_col_num = colnum

            thiscol = ['']*(largest_col_num + 1)

            for col in cols:
                value = ""
                try:
                    value = self._nodeText(col.getElementsByTagName('v')[0])
                except IndexError:
                    continue

                #Get col number (A=0, B=1, etc. up to AA)

                colnum = self._get_col_num(col) # ASCII to number

                try:
                    if col.attributes['t'].value == 's':
                        thiscol[colnum] = shared_strings[int(value)]
                    else:
                        thiscol[colnum] = value
                except KeyError:
                    continue
            self.rows.append(thiscol)

        myFile.close()

    def __getitem__(self, i):
        return self.rows[i]


i = 0
lang = {"France": "fr", "Netherlands": "nl", "Belgium": "nl", "Germany": "de", "Italy": "it", "Russia": "ru", "The Netherlands": "nl"}
x = XLSXReader(os.path.split(os.path.abspath(__file__))[0]+"/Copy_of_SocialExpress_pilot_keywords.xlsx")
for y in x:
    if y[2] == "Main term" or not y[2]:
        i += 1
        continue
#    print "main_keyword -- ", y[2]
#    print "competitor_keyword-- ", [w.strip(' ') for w in  y[3].split(",")]
    competitor_keyword = [w.strip(' ') for w in  y[3].split(",")]
#    print "main_enterprise-- ", "Philips"
#    print "main_location-- ", y[4]
#    print "main_language-- ", lang[str(y[4])]
    for keyword in competitor_keyword:
        list = ['python', 'engine/createreport.py']
        list.append("main_enterprise='Philips'")
        list.append("main_keyword=%s" % y[2])
        list.append("competitor1_keyword=%s" % keyword)
        list.append("main_language=%s" % lang[str(y[4])])
        list.append("main_location=%s" % y[4])
#        list.append("mail_to_list=%" % email)
#        list.append("main_screen_name_list='ThinkMedia'")
#        if i == 1:
        process = subprocess.Popen(list, shell=False, stdin=subprocess.PIPE)
        time.sleep(300)
    i += 1

x = XLSXReader("SocialExpress_pilot_keywords_ABN_AMRO.xlsx")
i = 0
for y in enumerate(x):
    if not y[1][1] or y[0] == 1:
        continue
    competitor_keyword = [w.strip(' ') for w in  y[1][3].split(",")]
    for keyword in competitor_keyword:
        list = ['python', 'engine/createreport.py']
        list.append("main_enterprise='ABN Amro'")
        list.append("main_keyword=%s" % y[1][2])
        list.append("competitor1_keyword=%s" % keyword)
        try:
            list.append("main_language=%s" % lang[str(y[1][4])])
        except:
            pass
        list.append("main_location=%s" % y[1][4])
        print list
        process = subprocess.Popen(list, shell=False, stdin=subprocess.PIPE)
        time.sleep(300)
print str(os.path.split(os.path.abspath(__file__))[0])
