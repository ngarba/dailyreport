'''
Take every condition/activity/selection in a category
Dump in total pools by category
Create a pie chart displaying total time each con/act/sel

The way my other code works, it created a time event starts and time event ends, then
calculated the difference for a single activity for a single day.

Pie chart: need a time event starts, time event ends, difference, then
sum, then need these calculated for every activity and every operation condition.
This means I will need code that essentially goes 'If act = 3, add to that activity's
value in a dictionary.
Then when all pools are created, make those pool values a list and make it a pie chart OR
make a pie chart with the title being the key and the values in the pie chart the data.

Next steps for pie chart:
~Figure out how to get rid of '' blank key ~ COMPLETED
~Have numbers of con/act/categories become labels
~Present numbers in python output console as days:hours:minutes rather than seconds
~See if there's a way to title the pie charts

~New Pie charts:
    ~Instruments in Technical Loss
    ~Weather Loss Subcats
    ~Insturments in Wealther Loss IGT

*~*
V.24
*~*

*Operation Conditions*          *Operation Activities*              In system 7 Technical Loss:
1 Normal                        1 Starting Up                       1 Enclosure
2 SciOps Testing                2 Opening                           2 Mount
3 Setup                         3 WFC Daily Calibrations            3 Coude
4 Weather Loss                  4 Target Finalization               4 Thermal
5 Operational Execution Loss    5 Observing                         5 GIS
6 Technical Loss                6 Standing By                       6 HLS
7 Unavoidable Loss              7 Closing                           7 Instruments
8 Unused Observing Time         8 Shutting Down                     8 PA&C
9 Instrument Group Testing      9 Handover Note                     9 WFC
                                                                      10 Other

Weather Conditions                                                  In setupoption 4 Setup:
1 Clear                                                             1 FIDO
2 Thin Clouds                                                       2 Instruments
3 Thick Clouds                                                      In Setup > fidooption
4 Humidity                      In 2 SciOps Testing:                1 M9a/DL-FM1
5 Overcast                      Some don't have insselection        2 New FIDO Config
6 Rain                          1 VBI
7 Snow/Ice                      2 ViSP                              In insselection 9 IGT
8 Strong Wind                   3 DL-NIRSP                          1 VBI
9 Lightning                     4 VTF                               2 ViSP
                                5 Cryo-NIRSP                        3 DL-NIRSP
In obsdefinition 5 Observing:   6 PA&C                              4 VTF
1 Observing OP                  7 WFC                               5 Cryo-NIRSP
2 Calibrating OP                                                    6 PA&C
                                                                    7 WFC
In wloptions 4 Weather Loss
1 WL: Instrument Group Testing
2 WL: SciOps Testing
3 WL: TechOps Testing
4 WL: None
'''



import json
import datetime as dt
from datetime import datetime, timedelta
import matplotlib
from matplotlib.ticker import FuncFormatter
import plotly.express as px
# import plotly as py
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from itertools import cycle
from collections import OrderedDict


# gib
f = open('activitylogs24.json')

# returns json data as a dictionary
jata = json.load(f)



'''A Pile of Lists n' Stuff'''
daterange = list()
alldata = dict()
pdata = dict()
lcon = list()
lact = list()
lsys = list()


# Code Start
print("Available subcategories are Condition, Activity, System, Definition, and Instrument.")
cin = input('What would you like to analyze?: ')

for i in jata['entries']:
    id = (i['recordId'])
    # Getting daytoday(unix epoch) to be a timestamp(the key value and date for the x axis
    day = int(int(i['fields']['daytoday']) / 1000)
    # Date in string
    date = str(pd.to_datetime(day, unit='s'))[0:10]


    '''
    Code has to read everything per iteration (recordID)
    When code sees timestamp requested
    Code starts creating dictionary of cons/acts/selects
    '''

    tes = (i['fields']['timeeventstarts'])
    tee = (i['fields']['timeeventends'])

    tevent = dt.datetime.strptime(tee, '%H:%M') - dt.datetime.strptime(tes, '%H:%M')
    svalue = tevent.total_seconds()

# Conditions
#     1:Normal 2:Test OP 3:SciOps Testing 4:Setup 5:Weather Loss 6:Operational Ex Loss
#     7:Technical Loss 8:Unavoidable Loss 9:Unused Obs Time 10: Ins Group Testing
    con = (i['fields']['opscondition'])

# Activity
#     1:Startup 2:Opening 3:WFC Daily Cals 4:Target Finalization 5:Observing
#     6:Standing By 7:Closing 8:Shutting Down 9:Handover
    act = (i['fields']['opsactivity'])

# System
#     1:Enclosure 2:Mount 3:Coude 4:Thermal 5:GIS 6:HLS 7:Instruments 8:PA&C 9:WFC 10:Other
    sys = (i['fields']['system'])

# Obsdefinition or observing program activity for both 2 Test OP and 1 Normal 5 Observing
#     1:Observing OP 2:Calibrating OP
    obsdef = (i['fields']['obsdefinition'])

# WL option in 4 Weather Loss
#     1: WL:Instrument Group Testing 2: WL: SciOps Testing 3: WL: TechOps Testing 4: None
    wlo = (i['fields']['wloptions'])

# Insselection or instrument selection both 3 SciOps Testing and 10 Ins Group Testing
# 1:VBI 2:ViSP 3:DL-NIRSP 4:VTF 5:Cryo-NIRSP 6:PA&C 7:WFC
    instr = (i['fields']['insselection'])
    instr = instr.replace("&quot;", "")
    instr = instr.replace("[", "")
    instr = instr.replace("]", "")
# Weather
# Needs to be stripped of [&quot; before implemented
#     1:Clear 2:Thin Clouds 3:Thick Clouds 4:Humidity 5:Overcast 6:Rain 7:Snow/Ice
#     8:Strong Wind 9:Lightning
#    weather = (i['fields']['weatherconditions'])

# create a new dictionary where the keys are menu options
# for each of those keys, assign the sub
    cat = {'con': con, 'act': act, 'sys': sys, 'obsdef': obsdef, 'instr': instr, 'wlo': wlo}

    alldata[id] = [date, cat[cin], svalue, con]
    #                      ^ this returns the value in the key,value pair of cat
#                        ^ what is this? How do I call 'act'? Indexing doesn't work for this problem.
#                           alldata[1] equals (2nd date, 2nd act, 2nd seconds value) not 'act'

# All dates in json file
    if date not in daterange:
        daterange.append(date)

# Copying date list
    drange = daterange
# Trying to make first date work
#print(alldata)
fdate = input("First Date Pls: ")
if fdate == '':
    fdate = '2023-06-07'

for stuff in drange:
    if fdate in drange:
        break
    else:
        if fdate not in drange:
            drange.append(fdate)
        drange = sorted(drange)
        dd = cycle(drange)
        for d in dd:
            if d == fdate:
                fdate = next(dd)
                break



# ctrl + / to comment out lines
# Creating an editable date range : defining 'for da in LIST(list)' matters
# Code needs list() around the list, regardless of whether it already is one or not
for da in list(drange):
    if da != fdate:
        drange.remove(da)
    else:
        if da == fdate:
            break

ldate = input("Last Date Pls: ")
for dl in drange:
    if ldate == '':
        ldate = '2023-07-14'

for ld in list(drange):
    if ldate in drange:
        if drange.index(ld) < drange.index(ldate):
            continue
        elif drange.index(ld) > drange.index(ldate):
            drange.remove(ld)
    else:
        if ldate not in drange:
            drange.append(ldate)
            drange = sorted(drange)
            if drange.index(ld) < drange.index(ldate):
                continue
            else:
                drange.remove(ld)


# Next compare alldata to drange and remove all entries without a date in drange
# for dv,dk in alldata:
#   for date in list(drange):
#       if date(dv[0]) not in list(drange):
#           continue
#       elif date(dv[0]) in list(drange):
#           pdata[con(dv[1]) = 0
#           pdata[con(dv[1]) += svalue(dv[2])


# alldata[id] = [date, cat[cin], svalue, con]
for dk,dv in alldata.items():
    if dv[0] not in list(drange):   # if date isn't in the desired range, don't use it
        continue
    if dv[1] == '':                 # if subcategory is empty, don't use it
        continue                                            # or dv[3] == '9' or dv[3] == '4':
    if cin == 'instr' and dv[3] == '2' or cin == 'instr' and dv[3] == '6' or cin == 'instr' and dv[3] == '4':
        continue                          # if subcat insselection isn't empty 'and' it's SciOps Test
                                          # or 6 Technical Loss, or 4 Weather Loss don't use it
                                          # 9 is Instrument Group Testing
    if cin == 'obsdef' and dv[3] == '4' or cin == 'obsdef' and dv[3] == '2':
        continue                          # if subcat obsdef isn't empty and it's SciOps Test
                                          # or WL: Sciops Test, ignore it
    elif dv[0] in list(drange):
        # print(dv[0])
        if dv[1] not in pdata:
            pdata[dv[1]] = 0
        pdata[dv[1]] += dv[2]
        idlis = list(pdata.keys())
        timetotal = list(pdata.values())
        # print(idlis, timetotal)
#pdata = sorted(pdata.items())
#print(pdata)
# Add times with matching condition/activity/selections into pdata
'''
*Operation Conditions*          *Operation Activities*              In system 7 Technical Loss:
1 Normal                        1 Starting Up                       1 Enclosure
2 SciOps Testing                2 Opening                           2 Mount
3 Setup                         3 WFC Daily Calibrations            3 Coude
4 Weather Loss                  4 Target Finalization               4 Thermal
5 Operational Execution Loss    5 Observing                         5 GIS
6 Technical Loss                6 Standing By                       6 HLS
7 Unavoidable Loss              7 Closing                           7 Instruments
8 Unused Observing Time         8 Shutting Down                     8 PA&C
9 Instrument Group Testing      9 Handover Note                     9 WFC
                                                                      10 Other

Weather Conditions                                                  In setupoption 4 Setup:
1 Clear                                                             1 FIDO
2 Thin Clouds                                                       2 Instruments
3 Thick Clouds                                                      In Setup > fidooption
4 Humidity                      In 2 SciOps Testing:                1 M9a/DL-FM1
5 Overcast                      Some don't have insselection        2 New FIDO Config
6 Rain                          1 VBI
7 Snow/Ice                      2 ViSP                              In insselection 9 IGT
8 Strong Wind                   3 DL-NIRSP                          1 VBI
9 Lightning                     4 VTF                               2 ViSP
                                5 Cryo-NIRSP                        3 DL-NIRSP
In obsdefinition 5 Observing:   6 PA&C                              4 VTF
1 Observing OP                  7 WFC                               5 Cryo-NIRSP
2 Calibrating OP                                                    6 PA&C
                                                                    7 WFC
In wloptions 4 Weather Loss
1 WL: Instrument Group Testing
2 WL: SciOps Testing
3 WL: TechOps Testing
4 WL: None
'''



acttitle = {'1': 'Startup', '2': 'Opening', '3': 'WFC Daily Calibrations',
         '4': 'Target Finalization', '5': 'Observing',
         '6': 'Standing By', '7': 'Closing', '8': 'Shutting Down',
         '9': 'Handover Note'}

contitle = {'1': 'Normal', '2': 'SciOps Testing', '3': 'Setup',
'4': 'Weather Loss', '5': 'Operational Exec Loss',
'6': 'Technical Loss', '7': 'Unavoidable Loss', '8': 'Unused Observing Time',
'9': 'Instrument Group Testing'}

systitle = {'1': 'Enclosure', '2': 'Mount', '3': 'Coude', '4': 'Thermal', '5': 'GIS',
            '6': 'HLS', '7': 'Instruments', '8': 'PA&C', '9': 'WFC', '10': 'Other'}

obsdeftitle = {'1': 'Observing OP', '2': 'Calibrating OP'}

institle = {'1': 'VBI', '2': 'ViSP', '3': 'DL-NIRSP', '4': 'VTF',
            '5': 'Cryo-NIRSP', '6': 'PA&C', '7': 'WFC'}

wlotitle = {'1': 'IGT', '2': 'SciOps Testing', '3': 'TechOps Testing', '4': 'None'}

titles = {'con': contitle, 'act': acttitle, 'sys': systitle, 'obsdef': obsdeftitle, 'instr': institle, 'wlo': wlotitle}

subthing = {ny:idy for nx,ny in titles[cin].items() for idx,idy in pdata.items() if nx == idx}


# subcattitle = title for num,title in subcatreference items for num in idlist if num in subcatref equals num in idlis
# pulled from both systitle and pdata in the same comprehension (fancy simple for statement) can do that

print(subthing)
kidlis = list(subthing.keys())
yidlis = list(subthing.values())

def convert(y):
    return str(dt.timedelta(seconds=y))

ytotals = [convert(y) for y in yidlis]

#print(ytotals)
totals = dict(zip(kidlis, ytotals))
print(totals)

# Plot them totals

pietitles = {'con': contitle, 'act': acttitle, 'sys': systitle, 'obsdef': obsdeftitle, 'instr': institle, 'wlo': wlotitle}

psdata = {'Operation ' + cin: kidlis,
        'Total Time': yidlis}

df = pd.DataFrame(psdata,columns=['Operation ' + cin, 'Total Time'])
fig = px.pie(df, values='Total Time', names='Operation ' + cin)
fig.show()

print(pdata)
print(drange)
print(idlis)
print(timetotal)


