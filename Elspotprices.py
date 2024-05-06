### Elspotprices.py

import os
from datetime import date, datetime, timedelta
import requests

import csv3


def read_elspot():

    tablename, header = "Elspotprices", ('HourDK', 'SpotPriceDKK')

    if not os.path.exists(tablename+".csv"):
        #response = requests.get(url='https://api.energidataservice.dk/dataset/Elspotprices?limit=5')
        #response = requests.get(url='https://api.energidataservice.dk/dataset/Elspotprices?start=now')
        #response = requests.get(url='https://api.energidataservice.dk/dataset/Elspotprices?start=StartOfDay')
        #response = requests.get(url='https://api.energidataservice.dk/dataset/Elspotprices?start=StartOfMonth')
        #response = requests.get(url='https://api.energidataservice.dk/dataset/Elspotprices?start=StartOfYear')
        #response = requests.get(url='https://api.energidataservice.dk/dataset/Elspotprices?start=2022-01-01')
        response = requests.get(url='https://api.energidataservice.dk/dataset/Elspotprices?offset=0&start=2023-01-01T00:00&filter=%7B%22PriceArea%22:[%22DK2%22]%7D&sort=HourUTC%20ASC&timezone=dk')

        result = response.json()
        records = result.get('records', [])
        rows = []
        for r in records:
            if r['PriceArea'] == 'DK2':
                rows.append([csv3.getdatetime(r['HourDK']), csv3.putfloat(r['SpotPriceDKK'])])
        rows.sort(key=lambda r: r[0])
        csv3.writetable(tablename, header, rows)

    ### Read elspot data from CSV file
    header, rows = csv3.readtable(tablename)
    print(tablename, header)
    kv = dict()
    for r in rows:
        dt = csv3.getdatetime(r[0])
        #if not r[1]: print(r)  ## hole in time series
        if r[1]:
            #if dt == summertime_datetime_start:
                #kv[dt-timedelta(hours=1)] = (csv3.getfloat(r[1]) + kv[dt-timedelta(hours=2)]) / 2
            kv[dt] = csv3.getfloat(r[1])
    elspot_ts = dict(sorted(kv.items()))
    #print(elspot_ts)
    print("[Elspot] len,min,max:", len(elspot_ts), min(list(elspot_ts.values())), max(list(elspot_ts.values())))
    
    return(elspot_ts)


