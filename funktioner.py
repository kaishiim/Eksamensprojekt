from datetime import datetime, date, timedelta
from math import sqrt


"""
ts_dict: timeseries(dict) with all datetime and prices

"find_dataday_hour"
RETURNS a dict containing 24 hours of one day in the time series 
"""
def find_dataday_hour(ts_dict): # Returner nyeste datetime dato
    datetime_lst = list(ts_dict.keys())
    max_ts = max(datetime_lst)
    print(max_ts)
    #dataday_hour = max_ts - timedelta(days=1)
    dataday_hour = max_ts
    print("dataday= ", dataday_hour)

    return dataday_hour


"""
ts_dict: timeseries(dict) with all datetime and prices
dataday_hour: date and time to select a date

"get_24_hours":
RETURNS new timesires as dict(datetime, price) for the day marked by dataday_hour
"""
def get_24_hours(ts_dict, dataday_hour):  
    day = datetime.date(dataday_hour)
    novo_dict = dict()
    for (k,v) in ts_dict.items():
        if datetime.date(k) == day:
            print(k,v)
            novo_dict[k] = v
    return novo_dict


"""
price_ts: timeseries(dict) with all datetime and prices
dataday_hour: date and time to select a date
hours_back: controls how many hours back in time for the price vector

"get_price_vector":
RETURNS pricevector starting from dataday_hour and hours_back backwards
"""
def get_price_vector(price_ts, dataday_hour, hours_back): 
    print("get_price_vector =",dataday_hour)
    """
    Loop vs List comprehension example
    price_vct = []
    for i in range(hours_back):
        dt = dataday_hour + timedelta(hours=i-(hours_back-1))
        price = price_ts[dt]
        price_vct.append(price)
    """
    price_vct = [price_ts[dataday_hour + timedelta(hours=i-(hours_back-1))] for i in range(hours_back)]
    return price_vct

#hours_back = 5  # controls price vector size

hours = [i for i in range(24)]

def get_date(dt):
    return date(dt.year, dt.month, dt.day)

def get_price_vector_ts(ts_dict, day): 
    #price_vct = [ts_dict[datetime(day.year, day.month, day.day, h)] for h in hours] (prøvede at lave list comprehension, but it no work T-T (fuck summertime))
    price_vct = []
    for h in hours:
        dt = datetime(day.year, day.month, day.day, h)
        if dt not in ts_dict:
            return None
        price = ts_dict[dt]
        price_vct.append(price)
    if len(price_vct) != 24:
        return None
    else:
        return price_vct

### RETURNS vector length of vector a
def vector_length(a):
    sum = 0
    for i in range(len(a)):
        sum += a[i]*a[i]
    return sqrt(sum)


### RETURNS dotproduct of the vectors a and b
def dotproduct(a, b):
    sum = 0
    for i in range(len(a)):
        sum += a[i] * b[i]    
    return sum

### Returns similiarity-value of the vectors a and b
def similiarity(a, b):
    return dotproduct(a,b) / (vector_length(a)*vector_length(b))


def avg_finder(vct_lst):
    return sum(vct_lst)/len(vct_lst)

def std_finder(vct_lst):
    sum = 0
    avg = avg_finder(vct_lst)
    for x in vct_lst:
        sum += (x - avg) * (x - avg)
    return sqrt(sum/len(vct_lst))

def median(lst):
    n = len(lst)
    s = sorted(lst)
    return (s[n//2-1]/2.0+s[n//2]/2.0, s[n//2])[n % 2] if n else None