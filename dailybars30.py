'''
Daily Display

Code asks for requested activity(s) or condition(s), first, and last date.
Creates bar graphs of one or two conditions or one or two activities between desired date range.
Calculates average and displays total time and average time spent between date ranges.

V.30

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
    "\n6:Target Finalization, 7:Observing, 8:Standing By, 9:Closing, 10:Shutting Down."
    "\nEnter the number of the activity.")
print("If you are looking for an operation condition, hit Enter twice to proceed to conditions.")
req = input("Enter desired activity: ")
print("If you are looking for a second activity, enter it now, or hit Enter to skip.")
sreq = input("Enter second desired activity: ")
print("The conditions available are: "
    "\n1:Normal, 2:Weather Loss, 3:Operation Execution Loss, 4:Technical Loss, 5:Unavoidable Loss,"
    "\n6:Unused Observing Time, 7:Observatory Prep Loss, 8:Sky Quality Loss"
    "\nEnter the number of the condition.")
print("If you have entered a desired activty, skip condition prompts by hitting Enter twice.")
oreq = input("Enter desired condition: ")
print("If you are looking for a second condition, enter it now, or hit Enter to skip."
      "\nOtherwise, leave blank and hit Enter.")
soreq = input("Enter second desired condition: ")
print("Format is YYYY-MM-DD.")

if oreq == '':
    oreq = '1'

# Activity and Condition dictionary
title = {'1': 'Startup', '2': 'Opening', '3': 'WFC Tasks',
         '4': 'Instrument Preparation', '5': 'Setup',
         '6': 'Target Finalization', '7': 'Observing', '8': 'Standby',
         '9': 'Closing', '10': 'Shutting Down', '11': 'Normal',
         '12': 'Weather Loss', '13': 'Operation Execution Loss', '14': 'Technical Loss',
         '15': 'Unavoidable Loss', '16': 'Unused Observing Time', '17': 'Observatory Preparation Loss',
         '18': 'Sky Quality Loss'}

# gib
f = open('activitylogs30.json')

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
    #     1:Normal 2:Weather Loss 3:Operation Execution Loss 4:Technical Loss 5:Unavoidable Loss
    #     6:Unused Observing Time 7:Observatory Prep Loss 8:Sky Quality Loss
    opscon = (i['fields']['opscondition'])
    sopscon = (i['fields']['opscondition'])
    # Activity
    #     1:Startup 2:Opening 3:WFC Task 4:Instrument Prep 5:Setup
    #     6:Target Finalization By 7:Observing 8:Standing By 9:Closing 10:Shutting Down
    activity = (i['fields']['opsactivity'])
    sactivity = (i['fields']['opsactivity'])
    # Ops Definition is specifically for Observing - Observing OP (1) or Calibrating OP (2)
    opsdef = (i['fields']['obsdefinition'])


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

fstdate = input("Enter first date: ")
# If date isn't entered, the first date of the dataset becomes the fstdate variable
for dat in dtrng.keys():
    if fstdate == '':
        fstdate = '2025-07-17' #dat
        break

# If fstdate doesn't exist, it is created with a value of 0 then put in the correct place of the dictionary
# The resultant plot will present data after the fstdate

if fstdate not in dtrng:
    print("\nIf this date is not visible in the final plot,"
          " it is because there are no data for this activity within this dataset.")
    dtrng[fstdate] = 0
print('The current first date is ' + fstdate)
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


lstdate = input("Enter last date: ")
for dat in dtrng.keys():
    if lstdate == '':
        lstdate = '2025-08-31' #'2077-11-08'
        break

# If entered lstdate doesn't exist, creates lstdate and assigns value of 0
# The resulting plot will show data before the lstdate
if lstdate not in dtrng:
    dtrng[lstdate] = 0
print('The current last date is ' + lstdate)
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



totaltime = sum(acts)

stotaltime = str(totaltime)

meanacts = np.mean(acts)
meanacts = meanacts/60
meanacts = int(meanacts)

def convert(meanacts):
    return dt.timedelta(minutes=meanacts)

cmeanacts = convert(meanacts)
cmeanacts = str(cmeanacts)
strippedseconds = ':'
smeanacts = str(meanacts)
smeanacts = smeanacts.strip(strippedseconds)



# plot
time = [i.seconds for i in act]
q = plt.figure(figsize=(10,8.5))
ax = q.add_subplot(1,1,1)
ax.bar(date, acts)
# average line - would like to add number in future
ax.axhline(np.mean(acts), color='blue', linewidth=2)

ax.yaxis.set_major_formatter(formatter)
ax.set_ylabel('Time')
ax.set_xlabel('Date')
plt.xticks(rotation=45)



tinsec = totaltime
#print(tinsec)
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
                plt.title(newtitle + "(Average = " + smeanacts + " min)")
        elif key == '1' + oreq:
            plt.title(value + " (Average = " + smeanacts + " min)")
            print("The total time for " + value + " for this dataset is " + stinsec + "(DD, HH:MM:SS).")
            print("Average Time = " + smeanacts + "(DD, HH:MM:SS).")

    else:
        if sreq != '' and sreq != req:
            if key == req:
                newtitle = value
            if key == sreq:
                newtitle = newtitle + ' + ' + value
                plt.title(newtitle + " (Average = " + smeanacts + " min)")
        elif key == req:
            plt.title(value + " (Average = " + smeanacts + " min)")
            print("The total time for " + value + " for this dataset is " + stinsec + "(DD, HH:MM:SS).")
            print("Average Time = " + cmeanacts + "(DD, HH:MM:SS).")


var_exists = 'newtitle' in locals() or 'newtitle' in globals()
try:
    newtitle
except NameError:
    var_exists = False
else:
    var_exists = True
    print("The total time for " + newtitle + " for this dataset is " + stinsec + "(HH:MM:SS).")
    print("Average Time = " + cmeanacts + "(DD, HH:MM:SS).")

#plt.savefig(r'C:')
plt.show()