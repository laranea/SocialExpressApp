'''
Created on Jul 11, 2012

@author: kristof
'''
import xlsx
import rt
import os
import re
import subprocess
import time

main_enterprise = "ABN Amro"

i = 0
lang = {"France": "fr", "Netherlands": "nl", "Belgium": "nl", "Germany": "de", "Italy": "it", "Russia": "ru", "The Netherlands": "nl"}

x = xlsx.XLSXReader("SocialExpress_pilot_keywords_ABN_AMRO.xlsx")
i = 0
for y in enumerate(x):
    if not y[1][1] or y[0] == 1:
        continue
    main_keywords = [w.strip(' ') for w in  re.split(' OR | \+ ', y[1][2])]
    main_language = lang[str(y[1][4])]
    main_location = y[1][4]
    competitor_keywords = [w.strip(' ') for w in  re.split(' OR | \+ ', y[1][3])]
    
    words = []
    words.extend(main_keywords)
    words.extend(competitor_keywords)
        
    list = ['python', 'rt.py']
    list.append(", ".join(words))
    print list
    process = subprocess.Popen(list, shell=False, stdin=subprocess.PIPE)
    time.sleep(300)

        
        
