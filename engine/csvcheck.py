import csv
import sys

f = open('abnamro1.csv', 'rt')
try:
    reader = csv.reader(f)
    rownr = 1
    for row in reader:
        if rownr == 1:
            i = 0
            for el in row:
                print i, el
                i = i + 1
        rownr = rownr + 1
                
finally:
    f.close()