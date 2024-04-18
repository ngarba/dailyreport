'''
Daily Display

Code asks for requested activity(s) or condition(s), first, and last date.
Creates bar graphs of one or two conditions or one or two activities between desired date range.
Calculates average and displays total time and average time spent between date ranges.

V.26

'''

import json
import datetime as dt
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict

# Input
print("The activities available are: "
    "\n1:Startup, 2:Opening, 3:WFC Task, 4:Instrument Preparation, 5:Setup,"
    "\n6:Target Finalization, 7:Observing, 8:Standing By, 9:Closing, 10:Shutting Down.")
print("If you are looking for an operation condition, hit Enter twice.")
req = input("Enter desired activity: ")
print("If you are looking for a second activity, enter it now.")
sreq = input("Enter second desired activity: ")
print("The conditions available are: "
    "\n1:Normal, 2:Weather Loss, 3:Operation Execution Loss, 4:Technical Loss, 5:Unavoidable Loss,"
      "\n6:Unused Observing Time, 7:Instrument Group Testing, 8:SciOps Testing,"
      " 9:TechOps Testing.")
print("If you have requested an activity, restart the code and follow the activity prompt.")
oreq = input("Enter desired condition: ")
print("If you are looking for a second condition, enter it now.")
soreq = input("Enter second desired condition: ")
print("Format is YYYY-MM-DD.")
#exdate = input("Enter excluded date: ")

if oreq == '':
    oreq = '1'
#if exdate == '':
#    exdate = '1917-09-24'

# Activity and Condition dictionary
title = {'1': 'Startup', '2': 'Opening', '3': 'WFC Tasks',
         '4': 'Instrument Preparation', '5': 'Setup',
         '6': 'Target Finalization', '7': 'Observing', '8': 'Standby',
         '9': 'Closing', '10': 'Shutting Down', '11': 'Normal',
         '12': 'Weather Loss', '13': 'Operation Execution Loss', '14': 'Technical Loss',
         '15': 'Unavoidable Loss', '16': 'Unused Observing Loss', '17': 'Instrument Group Testing',
         '18': 'SciOps Testing', '19': 'TechOps Testing'}

# gib
f = open('activitylogs26.json')

# returns json data as a dictionary
data = json.load(f)

# converting for plotting purposes
def format_func(x, pos):
    hours = int(x // 3600)
    minutes = int((x % 3600) // 60)
    seconds = int(x % 60)

    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


formatter = FuncFormatter(format_func)
# dictionaries to be filled
eventd = dict()
# dictionaries for getting the total M1 open time
end = dict()
beg = dict()
dtrng = dict()
obsv = dict()
# dates for plotting
dates = list()
# open time list for plotting when used
# will work with topen
optime = list()
act = list()
act_f = list()

'''
The way this one works:
In an 'entries' it sees daytoday, condition, activity, tes, and tee
The code sees daytoday converted to a string
When it iterates, it stops in an entry, and reads all this
If con/act is right, if stamp isn't in dictionary, it adds it
If it is in dictionary, it adds to its value
'''

for i in data['entries']:
    # Getting daytoday(unix epoch) to be a timestamp(the key value and date for the x axis
    day = int(int(i['fields']['daytoday']) / 1000)
    # Date in string
    stamp = str(pd.to_datetime(day, unit='s'))[0:10]

    # Open and close to be worked with for getting time M1 is open later
    # Getting time deltas for events
    # Open and close have some weird formatting and random "\t"s
    tes = (i['fields']['timeeventstarts'])
    tee = (i['fields']['timeeventends'])
    # Amount of time an event lasts
    tevent = dt.datetime.strptime(tee, '%H:%M') - dt.datetime.strptime(tes, '%H:%M')
    # Amount of time between the first open and the last close
#    topen = dt.datetime.strptime(close, '%H:%M') - dt.datetime.strptime(open, '%H:%M')

    # Conditions
    #     1:Normal 2:Test OP 3:SciOps Testing 4:Setup 5:Weather Loss 6:Operational Ex Loss
    #     7:Technical Loss 8:Unavoidable Loss 9:Unused Observing Time 10: Instrument Group Testing
    opscon = (i['fields']['opscondition'])
    sopscon = (i['fields']['opscondition'])
    # Activity
    #     1:Startup 2:Opening 3:WFC Daily Calibrations 4:Instrument Prep 5:Observing
    #     6:Standing By 7:Closing 8:Shutting Down 9:Handover Note
    activity = (i['fields']['opsactivity'])
    sactivity = (i['fields']['opsactivity'])
    # Ops Definition is specifically for Observing - Observing OP (1) or Calibrating OP (2)
    opsdef = (i['fields']['obsdefinition'])


    #if stamp == exdate:
    #    continue

    if req == '':
        if opscon == oreq:
            dates.append(stamp)
            act.append(tevent)
        elif sopscon == soreq and soreq != '' and soreq != oreq:
            dates.append(stamp)
            act.append(tevent)
    else:
        if activity == req:
            dates.append(stamp)
            act.append(tevent)
        elif sactivity == sreq and sreq != '' and sreq != req:
            dates.append(stamp)
            act.append(tevent)

    # for turning the activity time deltas into floating point values for the average
    for td in act:
        eachtd_f = td.total_seconds()

# This section is what sums up the total value (time it took) to execute an activity for each day
# If date (stamp) isn't in eventd, the dictionary, it is added as a key with a value of zero
# If while iterating the loop comes across the same stamp, it will add its value to the stamp
    if req == '':
        if opscon == oreq:
            if stamp not in eventd:
                eventd[stamp] = 0
            eventd[stamp] += eachtd_f
            date = list(eventd.keys())
            acts = list(eventd.values())

        elif sopscon == soreq and soreq != oreq and soreq != '':
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
            if req == '7':
                 if opsdef not in obsv:
                     obsv[opsdef] = 0
                 obsv[opsdef] += eachtd_f
                 optype = list(obsv.keys())
                 optime = list(obsv.values())

        elif sactivity == sreq and sreq != '' and sreq != req:
            if stamp not in eventd:
                eventd[stamp] = 0
            eventd[stamp] += eachtd_f
            date = list(eventd.keys())
            acts = list(eventd.values())


dtrng = eventd
# This is the start of getting the first date entered to work.
print(dtrng)
fstdate = input("Enter first date: ")
# If date isn't entered, the first date of the dataset becomes the fstdate variable
for dat in dtrng.keys():
    if fstdate == '':
        fstdate = '2023-11-20' #dat
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
print(dtrng)
# If the fstdate value is 0, it just deletes that key/value pair
for ndkey in list(dtrng):
    if dtrng[fstdate] == 0:
        del dtrng[ndkey]
        break

# Now reworking last date such that it works similar to first date
lstdate = input("Enter last date: ")
for dat in dtrng.keys():
    if lstdate == '':
        lstdate = '2024-01-22' #'2077-05-01'
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

# dtrng is the finished cleaned up dictionary to be used for plotting purposes

date = list(dtrng.keys())
acts = list(dtrng.values())


# Obligatory Print Section
# print(stamp)
# print(opscon)
# print(activity)
# print(date)
# print(acts)
#print(type(dtrng))

# Beginning of Legacy part of Code: This was meant to be for getting times for Observing subcategories.
# This part of the code is incomplete, as it does not trim the date range on obsv dictionary, so the
#  observe OP and calibration OP values are wrong. This is now calculated in Reportbreakdown code correctly
#  due to the order of operations used in Report breakdown being better suited for acquiring this value

#  if req == '7':
#    print('This is the Observe, Calibrate, and N/A OP dictionary')
#    print(obsv)

# End of legacy part of code

totaltime = sum(acts)

stotaltime = str(totaltime)

meanacts = np.mean(acts)

def convert(meanacts):
    return (dt.timedelta(seconds=meanacts))

meanacts = convert(meanacts)
smeanacts = str(meanacts)




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

tinsec = totaltime
print(tinsec)
def convert(tinsec):
    return (dt.timedelta(seconds=tinsec))

tinsec = convert(tinsec)
stinsec = str(tinsec)


for key,value in title.items():
    if req == '':
        if soreq != '' and soreq != oreq:
            if key == '1' + oreq:
                newtitle = value
            if key == '1' + soreq:
                newtitle = newtitle + ' + ' + value
                plt.title(newtitle)
        elif key == '1' + oreq:
            plt.title(value)
            print("The total time for " + value + " for this dataset is " + stinsec + "(DD, HH:MM:SS).")
            print("Average Time = " + smeanacts + "(DD, HH:MM:SS).")

    else:
        if sreq != '' and sreq != req:
            if key == req:
                newtitle = value
            if key == sreq:
                newtitle = newtitle + ' + ' + value
                plt.title(newtitle)
        elif key == req:
            plt.title(value)
            print("The total time for " + value + " for this dataset is " + stinsec + "(DD, HH:MM:SS).")
            print("Average Time = " + smeanacts + "(DD, HH:MM:SS).")


var_exists = 'newtitle' in locals() or 'newtitle' in globals()
try:
    newtitle
except NameError:
    var_exists = False
else:
    var_exists = True
    print("The total time for " + newtitle + " for this dataset is " + stinsec + "(HH:MM:SS).")
    print("Average Time = " + smeanacts + "(DD, HH:MM:SS).")

plt.show()