'''
Import json and use it to read daily report info
need to remember json/dictionaries
key/value pairs
taking dictionary data and plotting it, probably using matplotlib
getting interactivity involved with it
perhaps input prompt for desired parameters for plotting
start with extracting info for plotting
How the hell do you get a timedelta out of two separate
time strings in a json file?
Conditions:
    1:Normal 2:Weather 3:Technical 4:TestingOP 5:Setup 6:Maintenance 7:IT&C Tests
Activity:1:StartingUp 2:Opening 3:Observing 4:HandoverNote 5:StandingBy
    6:Closing 7:ShuttingDown 8:NA

Time we were open would be basically:
    for entries where ops activity == 6(closing):
        lista.append(time event ends)
    for entries where ops activity == 2(opening)
        listb.append(time event ends)
now lista has the time M1 closed and listb has the time M1 opened

so difference between lista and listb will have a time delta equal to the time M1 was open.
use topen when I start working on that


start and end date working
weather conditions - weather loss

%2021-10-19
Try to make dates more robust
    by making it such that if invalid date is entered, code goes to next valid date
Combine events like Start and Open

%2021-10-21
For Robust Dates: If a date entered doesn't exist, it is created and inserted into the dictionary, then sorted.
If it's created, this means its value is inherently zero, so a portion of script was written to delete this
    new value afterward.
My reasoning was that by simply trying to make it check for the next date up or down it could continue running
    into an issue where the next date up or down does not exist.
This solution bypasses that problem.

'''

import json
import datetime as dt
from datetime import datetime, timedelta
import matplotlib
from matplotlib.ticker import FuncFormatter
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from collections import OrderedDict

# Activity input
print("The activities available are: "
    "1:Startup 2:Opening 3:Observing 4:Handover 5:Standby "
    "6:Closing 7:Shutdown 8:NA. \n Enter number of desired activity.")
print("If you are looking for an operation condition, type 8, or hit Enter.")
req = input("Enter desired activity: ")
print("The conditions available are: "
    "1:Normal 2:Weather 3:Technical 4:TestingOP 5:Setup 6:Maintenance 7:IT&C Tests")
print("If you have requested an activity, type 1, or hit Enter.")
oreq = input("Enter desired condition: ")
print("Format is YYYY-MM-DD.")
exdate = input("Enter excluded date: ")
#lstdate = input("Enter last date: ")

if req == '':
    req = '8'
if oreq == '':
    oreq = '1'
if exdate == '':
    exdate = '1917-09-24'
#if lstdate == '':
#    lstdate = '2077-10-31'

# Activity dictionary
title = {'1': 'Startup', '2': 'Opening', '3': 'Observing',
         '4': 'Handover', '5': 'Standing By',
         '6': 'Closing', '7': 'Shutdown', '8': 'NA',
         '12': 'Weather Loss', '13': 'Technical Loss', '14': 'Testing OP',
         '15': 'Setup', '16': 'Maintenance', '17': 'IT&C Tests'}

# gib
f = open('dailyreport11.json')

# returns json data as a dictionary
data = json.load(f)

# for converting for plotting purposes
def format_func(x, pos):
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)

    #return "{:d}:{:02d}".format(hours, minutes)
    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


formatter = FuncFormatter(format_func)
# dictionaries to be filled, might be useless tbd
eventd = dict()
# dictionaries for getting the total M1 open time
end = dict()
beg = dict()
dtrng = dict()
# dates for plotting
dates = list()
# open time list for plotting when used
# will work with topen
optime = list()
act = list()
act_f = list()

for i in data['entries']:
    # Getting daytoday(unix epoch) to be a timestamp(the key value and date for the x axis
    day = int(int(i['fields']['daytoday']) / 1000)
    # Date in string
    stamp = str(pd.to_datetime(day, unit='s'))[0:10]

    # Open and close to be worked with for getting time M1 is open later
    # Getting time deltas for events
    # Open and close have some weird formatting and random "\t"s
    open = (i['fields']['opentime']).replace("\t ", "")
    close = (i['fields']['closetime']).replace("\t ", "")
    tes = (i['fields']['timeeventstarts'])
    tee = (i['fields']['timeeventends'])
    # Amount of time an event lasts
    tevent = dt.datetime.strptime(tee, '%H:%M') - dt.datetime.strptime(tes, '%H:%M')
    # Amount of time between the first open and the last close
    topen = dt.datetime.strptime(close, '%H:%M') - dt.datetime.strptime(open, '%H:%M')

    # Conditions
    # 1:Normal 2:Weather 3:Technical 4:TestingOP 5:Setup 6:Maintenance 7:IT&C Tests
    opscon = (i['fields']['opscondition'])
    # Activity
    # 1:StartingUp 2:Opening 3:Observing 4:HandoverNote 5:StandingBy 6:Closing 7:ShuttingDown 8:NA
    activity = (i['fields']['opsactivity'])

    # for testing how to get time M1 is open
    # if activity == '6':
    #    end[stamp] = (tee)
    # if activity == '2':
    #    beg[stamp] = (tee)

    if req == '2' or req == '7':
        exdate = '2021-07-22'
    if req == '1':
        exdate = '2021-05-20'
    if stamp == exdate:
        continue

    if req == 8 or req == '':
        if opscon == oreq:
            dates.append(stamp)
            act.append(tevent)
    else:
        if activity == req:
            dates.append(stamp)
            act.append(tevent)

    # for turning the activity time deltas into floating point values for the average
    for td in act:
        eachtd_f = td.total_seconds()

# This section is what sums up the total value (time it took) to execute an activity for each day
# If date (stamp) isn't in eventd the dictionary, it is added as a key with a value of zero
# If while iterating the loop comes across the same stamp, it will add its value to the stamp
    if req == '8' or req == '':
        if opscon == oreq:
            if stamp not in eventd:
                eventd[stamp] = 0
            eventd[stamp] += eachtd_f
            date = list(eventd.keys())
            acts = list(eventd.values())
    else:
        if activity == req:
            if stamp not in eventd:
                eventd[stamp] = 0
            eventd[stamp] += eachtd_f
            date = list(eventd.keys())
            acts = list(eventd.values())
#            if stamp == lstdate:
#                break

dtrng = eventd
# This is the start of getting the first date entered to work.
print(dtrng)
fstdate = input("Enter first date: ")
# If date isn't entered, the first date of the dataset becomes the fstdate variable
for dat in dtrng.keys():
    if fstdate == '':
        fstdate = dat
        break
# If fstdate doesn't exist, it is created with a value of 0 then put in the correct place of the dictionary
# The resultant plot will present data after the fstdate
if fstdate not in dtrng:
    print("If this date is not visible in the final plot,"
          " it is because there are no data for this activity within this dataset.")
    dtrng[fstdate] = 0
dtrng = OrderedDict(sorted(dtrng.items()))
# Dictionary for some reason in python 3 must be a list
# Allows one to iterate through a dictionary of changing size, which this is doing
# This code checks if a key date is the fstdate variable. If it's not, it gets rid of the whole key/value pair
for dkey in list(dtrng):
    if dkey != fstdate:
        del dtrng[dkey]
    else:
        if dkey == fstdate:
            break
# If the fstdate value is 0, it just deletes that key/value pair
for ndkey in list(dtrng):
    if dtrng[fstdate] == 0:
        del dtrng[ndkey]
        break

# Now reworking last date such that it works similar to first date
lstdate = input("Enter last date: ")
for dat in dtrng.keys():
    if lstdate == '':
        lstdate = '2077-05-01'
        break
# If entered lstdate doesn't exist, creates lstdate and assigns value of 0
# The resulting plot will show data before the lstdate
if lstdate not in dtrng:
    dtrng[lstdate] = 0
dtrng = OrderedDict(sorted(dtrng.items()))
# Checks if iterable in dictionary is in a place before or after lstdate.
# If iterable is after lstdate, deletes key/value pair.
for ldkey in list(dtrng):
    if list(dtrng.keys()).index(ldkey) < list(dtrng.keys()).index(lstdate):
        continue
    elif list(dtrng.keys()).index(ldkey) > list(dtrng.keys()).index(lstdate):
        del dtrng[ldkey]
# If lstdate value is 0, deletes the key/value pair
for lndkey in list(dtrng):
    if lndkey == lstdate and dtrng[lstdate] == 0:
        del dtrng[lndkey]


date = list(dtrng.keys())
acts = list(dtrng.values())

# Obligatory Print Section
# print(stamp)
# print(opscon)
# print(activity)
# print(date)
# print(acts)
#print(dtrng)


# plot
time = [i.seconds for i in act]
q = plt.figure(figsize=(10,8.5))
ax = q.add_subplot(1,1,1)
ax.bar(date, acts)
# average line - would like to add number in future
ax.axhline(np.mean(acts), color='blue', linewidth=2)

ax.yaxis.set_major_formatter(formatter)
# this locates y-ticks at the hours
#ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=3600))
# this ensures each bar has a 'date' label
#ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=1))
ax.set_ylabel('Time')
ax.set_xlabel('Date')
plt.xticks(rotation=45)
# This loop takes the title dictionary up top and uses the activity input to add a title
for key,value in title.items():
    if req == '8':
        if key == '1' + oreq:
            plt.title(value)
    else:
        if key == req:
            plt.title(value)
plt.show()