#### csv3.py


"""Read/write CSV-files in Danish format"""


import sys
import csv
from datetime import datetime


#### READ DATA FROM TABLE IN CSV-FILE


def getdate(s):
  if s == None or s.strip() == "":
    d = None
  else:
    s = s.strip()
    date_format = '%Y-%m-%d'
    d = datetime.strptime(s, date_format)
  return d


def getdatetime(s):
  if s == None or s.strip() == "":
    dt = None
  else:
    s = s.strip()
    sep = ' ' if s[10] == ' ' else 'T'
    datetime_format = '%Y-%m-%d' + sep + '%H:%M:%S'
    dt = datetime.strptime(s, datetime_format)
  return dt


def getfloat(s):
  if s == None or s.strip() == "":
    f = None
  else:
    f = float(s.replace(',', '.'))
  return f


def getint(s):
  if s == None or s.strip() == "":
    x = None
  else:
    x = int(s)
  return x


## Read table
def readtable(tablename, encoding=None):
  #print(">> readtable", tablename, encoding)
  if encoding:
    with open(tablename+'.csv', 'r', newline='', encoding=encoding) as file:
      reader = csv.reader(file, delimiter=';')
      header = next(reader)
      rows = [r for r in reader]
  else:
    with open(tablename+'.csv', 'r', newline='') as file:
      reader = csv.reader(file, delimiter=';')
      header = next(reader)
      rows = [r for r in reader]
  return (header, rows)


#### WRITE DATA TO TABLE IN CSV-FILE


def putfloat(x):
  return str(x).replace('.' , ',') if x != None else ""


def putint(x):
  return str(int(x+0.5)) if x != None else ""


## Write table
def writetable(tablename, header, rows):
  with open(tablename+'.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    ## Write header
    writer.writerow(header)
    ## Write rows
    for row in rows:
      writer.writerow(row)


## Append table
def appendtable(tablename, header, rows):
  with open(tablename+'.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    ## Append header
    if header:
      writer.writerow(header)
    ## Append rows
    for row in rows:
      writer.writerow(row)


