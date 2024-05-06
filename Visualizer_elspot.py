import sys
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import Elspotprices as elspot
import csv3
from funktioner import *

##### MAIN #####
k = 3
num_std = 1.28 #1.64
weekdays = [w for w in range(7)]


"""
price_ts = elspotprices formatted as dict(datetime, price)
dataday_hour = dict containing 24 hours of one day from price_ts
days_sorted = sorted datetime dates from price_ts

"""
header, rows = csv3.readtable("Nordpool")
rows2 = []
for r in rows:
    r2 = [csv3.getdate(r[0]), csv3.getint(r[1]), csv3.getfloat(r[2])]
    rows2.append(r2)
print(rows2)
nordpoolprices = [r2[2] for r2 in rows2]


price_ts = elspot.read_elspot()
dataday_hour = find_dataday_hour(price_ts)
price_vct = get_price_vector_ts(price_ts, get_date(dataday_hour))

days_sorted = sorted(list(set([get_date(dt) for dt in price_ts.keys()])))



price_vct_dict = dict()
for d in days_sorted:
    price_vct = get_price_vector_ts(price_ts, d)
    if price_vct != None: # protocol for missing dates
        price_vct_dict[d] = price_vct
#print(price_vct_dict)

# Find normalized price vectors by weekday
price_vct_lst_of_weekday = dict()
for wdn in weekdays:
    price_vct_lst_of_weekday[wdn] = []
    for d in days_sorted:
        if wdn == d.weekday():
            if d in price_vct_dict:
                price_vct = price_vct_dict[d]
                mdn = median(price_vct)
                price_vct_norm = [(p+1000)*1000/(mdn+1000) for p in price_vct]
                #print(wdn, price_vct_norm)
                price_vct_lst_of_weekday[wdn].append(price_vct_norm)
        #print(price_vct_lst_of_weekday)

# Calculate median price vector by hour
price_by_wdn_hour = dict()
for wdn in weekdays:
    for h in hours:
        price_by_wdn_hour[wdn, h] = []
    for price_vct in price_vct_lst_of_weekday[wdn]:
        for h in hours:
            price = price_vct[h]
            price_by_wdn_hour[wdn, h].append(price)
median_by_wdn_hour = dict()
for wdn in weekdays:
    for h in hours:
        median_by_wdn_hour[wdn, h] = median(price_by_wdn_hour[wdn, h])
day_vct_by_wdn = dict()
for wdn in weekdays:
    day_vct_by_wdn[wdn] = []
    for h in hours:
        day_vct_by_wdn[wdn].append(median_by_wdn_hour[wdn, h])

# Plot normalized price vectors and median weekday, by weekday
weekdaynames = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']
fig, axes = plt.subplots(2, 7)
for wdn in weekdays:
    for price_vct in price_vct_lst_of_weekday[wdn]:
        axes[0, wdn].plot(price_vct)
        axes[0, wdn].set_title(weekdaynames[wdn], fontsize=11)
    axes[0, wdn].set_ylabel("Price (DKK/MWh)")
    axes[1, wdn].plot(day_vct_by_wdn[wdn])
    axes[1, wdn].set_title(f'Median({weekdaynames[wdn]})', fontsize=10)
    axes[1, wdn].set_ylabel("Price (DKK/MWh)")
    plt.subplots_adjust(hspace=0.25)
plt.show()






"""
newest_day = newest datetime value in days_sorted
sim_lst = list of simmiliartity values for newest_day and entire timeseries
d = current date time
prognosis = d+1 
"""

# Find newest day and its price vector
newest_day = days_sorted[-1]
newest_price_vct = price_vct_dict[newest_day]

# Calculate similarity list
sim_lst = []
for d in days_sorted:
    if d != newest_day:
        next_day = d + timedelta(days=1)
        if d in price_vct_dict and next_day in price_vct_dict:
            pr_vct_d = price_vct_dict[d]
            sim = similiarity(newest_price_vct, pr_vct_d)
            sim_lst.append((d, sim))
            #print(d, sim,)


### k-NN algorithm start

# Find k-best day-similarities and associated price vectors
sim_lst.sort(key=lambda x: x[1])
best_sims = sim_lst[-k:]   # k-best similarities
prognosis = []
for s in best_sims:
    d = s[0]
    d1 = d + timedelta(days=1)
    print(d, d1, sim)
    prognosis.append( (d, price_vct_dict[d], price_vct_dict[d1]) )

# Normalize by scaling the k-best price vectors to have same length as price vector for 'newest day'
#print("før =", prognosis)
prognosis2 = []
v0_len = vector_length(newest_price_vct)
for date_vct in prognosis:
    d = date_vct[0]
    v1_len = vector_length(date_vct[1])
    v2_len = vector_length(date_vct[2])
    scale = v0_len / v1_len
    print("scale =", scale)
    v2_scaled = [p * scale for p in date_vct[2]]
    prognosis2.append( (d, [], v2_scaled) )
#print("efter =",prognosis2)

# Calculate confidence band as avgerage +/- 'num_std' standard deviations 
avg_std_list = []
y_lower = []
y_upper = []
for h in hours:
    hour_vct = []
    for date_vct in prognosis2:
        hour_vct.append(date_vct[2][h])
    print(h, hour_vct, avg_finder(hour_vct), std_finder(hour_vct))
    y_lower.append(avg_finder(hour_vct) - num_std * std_finder(hour_vct))
    y_upper.append(avg_finder(hour_vct) + num_std * std_finder(hour_vct))

# Calculate median of prognosises curves from k-best price vectors in 'prognosis2'
median_lst = []
for h in hours:
    val_lst = []
    for date_vct in prognosis2:
        dv2h = date_vct[2][h]
        val_lst.append(dv2h)
    print(h, mdn)
    mdn = median(val_lst)
    median_lst.append(mdn)

# Write mediancurve values to a csv file, in format ['k', 'dato', 'time', f'median k={k}']
next_day = newest_day + timedelta(days=1)   
rows = []
for h in hours:
    row = [k, next_day, h, csv3.putfloat(median_lst[h])]
    rows.append(row)
header = ['k', 'dato', 'time', f'median k={k}']
csv3.writetable(f'Medianværdier-k={k}', header, rows)

# Plot k-best unnormlized pricevectors, from 'prognosis' 
next_day = newest_day + timedelta(days=1)   
plt.title(f"Day-ahead prognose (k={k}) for {next_day} (unormalized)")
plt.ylabel("Elspot pris i DKK")
plt.xlabel("Timer")
x_ticks = hours
x_labels = [str(x) for x in x_ticks]
plt.xticks(x_ticks, x_labels)
for date_vct in prognosis:
    plt.plot(hours, date_vct[2], label=f"{date_vct[0]}")
plt.legend()
plt.grid()
plt.show()

# Plot k-best normalized pricevcetors, from 'prognosis2', confidenceband and median price
fig, axes = plt.subplots(2)
next_day = newest_day + timedelta(days=1)   
axes[0].set_title(f"Day-ahead prognose (k={k}) for {next_day}(normalized)")
axes[0].set_ylabel("Elspot pris i DKK")
axes[0].set_xlabel("Timer")
x_ticks = hours
x_labels = [str(x) for x in x_ticks]
axes[0].set_xticks(x_ticks, x_labels)
axes[0].fill_between(hours, y_lower, y_upper, alpha = 0.2, label="Konfidensbånd")
for date_vct in prognosis2:
    axes[0].plot(hours, date_vct[2], label=f"{date_vct[0]}")
axes[0].plot(hours, nordpoolprices, label="Nordpool", marker='.', c='black')
axes[0].legend(fontsize = 8, loc='upper left')
axes[0].grid()
axes[1].set_title(f"Medianværdier (k={k}) for {next_day}(normalized)")
axes[1].set_ylabel("Elspot pris i DKK")
axes[1].set_xlabel("Timer")
axes[1].plot(median_lst)
axes[1].set_xticks(x_ticks, x_labels)
axes[1].grid()
plt.subplots_adjust(hspace=0.5)
plt.show()

