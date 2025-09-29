'''
Code creates pie charts with the total times spent doing each subcategory
within category (Conditions/Activities/Systems).

Pie Charts created currently:
Operations Conditions
Operations Activities
Observing OP Type (Observe/Cal)
Technical Loss System
Technical Loss Instruments
Instrument Group Testing Instrument
Weather Loss IGT

Desired Update for pie charts: persistent color legend

*~*
V.30
*~*

*Operation Conditions*          *Operation Activities*              In system 4 Technical Loss:
1 Normal                        1 Starting Up                       1 Enclosure
2 Weather Loss                  2 Opening                           2 Mount
3 Operational Execution Loss    3 WFC Task                          3 Coude
4 Technical Loss                4 Instrument Preparation            4 Thermal
5 Unavoidable Loss              5 Setup                             5 GIS
6 Unused Observing Time         6 Target Finalization               6 HLS
7 Observatory Preparation Loss  7 Observing                         7 Instruments
8 Sky Quality Loss              8 Standing By                       8 PA&C
                                9 Closing                           9 WFC
                                10 Shutting Down                   10 M1
                                                                   11 Feed Optics
                                                                   12 TEOA
                                                                   13 Other

Weather Conditions                                                  In setupoption 5 Setup:
1 Clear                                                             1 ViSP Filter Change
2 Thin Clouds                                                       2 M9a/DL-FM1
3 Thick Clouds                                                      3 New FIDO Configuration
4 Humidity                      In 8 SciOps Testing:                4 Other
5 Overcast                      Some don't have instscitest
6 Rain                          1 HLS
7 Snow/Ice                      2 PA&C                              In insselection 7 IGT and 8 SciOps Test
8 Strong Wind                   3 WFC                               1 VBI
9 Lightning                     4 Instruments                       2 ViSP
                                5 Other                             3 DL-NIRSP
In obsdefinition 7 Observing:                                       4 VTF
1 Observing OP                                                      5 Cryo-NIRSP
2 Calibrating OP

In wloptions 2 Weather Loss     In insselection 4 Instrument Preparation
1 WL: Instrument Group Testing  1 VBI
2 WL: SciOps Testing            2 ViSP
3 WL: TechOps Testing           3 DL-NIRSP
4 None                          4 VTF
                                5 Cryo-NIRSP
In techopstest 9 TechOps Testing:
1 Enclosure
2 Mount
3 Coude
4 Thermal
5 GIS
6 M1
7 Feed Optics
8 TEOA
9 Vibration
10Other



'''



import json
import datetime as dt
import time
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
from itertools import chain

# gib
j = input("What json would you like to analyze? ")
if j == '':
    j = 'activitylogs30.json'
print('Analyzing ' + j)
f = open(j)
# returns json data as a dictionary
jata = json.load(f)


'''A Pile of Lists n' Stuff'''
daterange = []
alldata = {}
pdata = {}


# Code Start
print("Available subcategories are Condition(con), Activity(act), Tech Loss System(sys),'"
      "\n Obs Definition(obsdef), Tech Loss Instrument(instr), Sky Quality Loss (wlo),"
      "and Weather Loss Weather Condition(wea)."
      "\nEnter the abbreviation within the parentheses of the subcategory you would like to analyze.")
cin = input('What would you like to analyze?: ')
start_time = time.time()
for i in jata['entries']:
    id = (i['recordId'])
    # Getting daytoday(unix epoch) to be a timestamp(for adding to the daterange list)
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
#     1:Normal 2:Weather Loss 3:Op Ex Loss 4:Technical Loss 5:Unavoidable Loss
#     6:Unused Obs Time 7:IGT 8:SciOps Testing 9:TechOps Testing
    con = (i['fields']['opscondition'])

# Activity
#     1:Startup 2:Opening 3:WFC Tasks 4:Instrument Prep 5:Setup
#     6:Target Finalization 7:Observing 8:Standing By 9:Closing 10:Shutting Down
    act = (i['fields']['opsactivity'])

# System
#     1:Enclosure 2:Mount 3:Coude 4:Thermal 5:GIS 6:HLS 7:Instruments 8:PA&C 9:WFC
#     10:M1 11:Feed Optics 12:TEOA 13:Other
    sys = (i['fields']['system'])

# Obsdefinition or observing program activity for 1 Normal 7 Observing
#     1:Observing OP 2:Calibrating OP
    obsdef = (i['fields']['obsdefinition'])

# WL option in 2 Weather Loss,  7 Observatory Preparation Loss, and 8 Sky Quality Loss
#     1: WL:Instrument Group Testing 2: WL: SciOps Testing 3: WL: TechOps Testing 4: None
    wlo = (i['fields']['wloptions'])

# Instrument Group Testing and SciOps Testing
#     1:HLS 2:PA&C 3:WFC 4:Instruments 5:Other
    insci = (i['fields']['instscitest'])

# Weather Selection - gonna be used specifically with 2 Weather Loss
# 1:Clear, 2:Thin Clouds 3: Thick Clouds, 4:Humidity, 5:Overcast
# 6:Rain, 7:Snow/Ice, 8:Strong Wind, 9:Lightning
    wea = (i['fields']['weatherconditions'])

# Insselection or instrument selection both 8 SciOps Testing and 7 Ins Group Testing
# 1:VBI 2:ViSP 3:DL-NIRSP 4:VTF 5:Cryo-NIRSP
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
    cat = {'con': con, 'act': act, 'sys': sys, 'obsdef': obsdef, 'instr': instr, 'wlo': wlo, 'wea': wea}

#   alldata is literally all data - a dictionary where the key is the record ID and the value is a tuple
#                                   of values associated with each id
    alldata[id] = (date, cat[cin], svalue, con, wlo, instr)
#                           ^ this returns the value in the key,value pair of cat
#
#                            alldata[1] equals (2nd date, 2nd subactivity number, 2nd seconds value) not 'act'

# All dates in json file
    if date not in daterange:
        daterange.append(date)

# Copying date list
    drange = daterange

# First Date
#print(alldata)
fdate = input("First Date Pls: ")
if fdate == '':
    fdate = '2025-07-17'

print('The current first date is ' + fdate)

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

# Last Date
ldate = input("Last Date Pls: ")
for dl in drange:
    if ldate == '':
        ldate = '2025-08-31'

print('The current last date is ' + ldate)

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

# The following section ensure that when we get:
# Instrument selection, it's for 4 Technical Loss,
# Weather Loss Option, it's for 7 Observatory Prep Loss,
# and Weather Loss condition, it's for 2 Weather Loss

for dk,dv in alldata.items():
    if dv[0] not in list(drange):   # if date isn't in the desired range, don't use it
        continue
    if dv[1] == '':                 # if subcategory is empty, don't use it
        continue
    if cin == 'instr' and dv[3] != '4':
        continue                          # if subcat insselection isn't empty 'and'
                                          # it's not 4 Technical Loss, ignore.
                                          # Can be changed to 2 Weather Loss
                                          # 7 is Observatory Preparation Loss
                                          # 8 is Sky Quality Loss

    if cin == 'wlo' and dv[3] != '8':
        continue
                                          # if subcat is wloption and
                                          # not 8 Sky Quality Loss, ignore
                                          # 7 is Observatory Prep Loss
                                          # 2 is Weather Loss

    if cin == 'wea' and dv[3] != '2':
        continue
                                          # if subcat is weather selection and
                                          # not 2 Weather Loss, ignore

# End of section for throwing out pieces.


# Make a new dictionary called pdata. The Keys are subcategory options. The Values are the total time in
# seconds of each option
    elif dv[0] in list(drange):
        # print(dv[0])
        if dv[1] not in pdata:
            pdata[dv[1]] = 0
        pdata[dv[1]] += dv[2]
        idlis = list(pdata.keys())
        timetotal = list(pdata.values())

#print(pdata)
# pdata is a dictionary of idlis:timetotal
# idlis is the id number of an option in a category or subcategory
# timetotal is the total time for that option in seconds
# idlis and timetotal are only here as doublechecks.

# Add times with matching condition/activity/selections into pdata


acttitle = {'1': 'Startup', '2': 'Opening', '3': 'WFC Tasks',
         '4': 'Instrument Preparation', '5': 'Setup',
         '6': 'Target Finalization', '7': 'Observing', '8': 'Standing By',
         '9': 'Closing', '10': 'Shutting Down'}

contitle = {'1': 'Normal', '2': 'Weather Loss', '3': 'Operation Exec Loss',
'4': 'Technical Loss', '5': 'Unavoidable Loss',
'6': 'Unused Observing Time', '7': 'Observatory Preparation Loss', '8': 'Sky Quality Loss'}

systitle = {'1': 'Enclosure', '2': 'Mount', '3': 'Coude', '4': 'Thermal', '5': 'GIS',
            '6': 'HLS', '7': 'Instruments', '8': 'PA&C', '9': 'WFC', '10': 'M1',
            '11': 'Feed Optics', '12': 'TEOA', '13': 'TAT', '14':'Facility', '15':'Other'}

obsdeftitle = {'1': 'Observing OP', '2': 'Calibrating OP'}

institle = {'1': 'VBI', '2': 'ViSP', '3': 'DL-NIRSP', '4': 'VTF', '5': 'Cryo-NIRSP'}

wlotitle = {'1': 'Instrument Group Testing', '2': 'SciOps Testing', '3': 'TechOps Testing', '4': 'None'}

weatitle = {'1': 'Clear', '2': 'Thin Clouds', '3': 'Thick Clouds', '4': 'Humidity', '5': 'Overcast',
             '6': 'Rain', '7': 'Snow/Ice', '8': 'Strong Wind', '9': 'Lightning'}

# Dictionaries of subcategory options and their respective names.

titles = {'con': contitle, 'act': acttitle, 'sys': systitle, 'obsdef': obsdeftitle,
          'instr': institle, 'wlo': wlotitle, 'wea': weatitle}
# for titles[cin].items()

subthing = {ny:idy for nx,ny in titles[cin].items() for idx,idy in pdata.items() if nx == idx}

# subthing takes pdata and replaces idlis with the corresponding title in english
# determined by the requested title/subtitle dictionary

# subcattitle = title for num,title in subcat reference items for num in idlis if num in subcatref equals num in idlis
# pulled from both systitle and pdata in the same comprehension (fancy simple for statement) can do that

#print("This is Subthing: ")
#print(subthing)
kidlis = list(subthing.keys())
yidlis = list(subthing.values())

def convert(y):
    return str(dt.timedelta(seconds=y))

ytotals = [convert(y) for y in yidlis]
alltime = sum(yidlis)
alltimet = [convert(alltime)]

#print(ytotals)
totals = dict(zip(kidlis, ytotals))
#print("This is drange: ")
#print(drange)
print("These are the times for each wedge: ", totals)
print("This is the total for the subcategory", alltimet)

# Create color legend
#ccolors = px.colors.qualitative.Plotly
#cmap = dict(zip(kidlis, ccolors))
#cmapl = list(cmap.values())
#print(cmap)

conmap = {'Normal': '#636EFA', 'Weather Loss': '#EF553B',
          'Operation Exec Loss': '#00CC96', 'Technical Loss': '#AB63FA',
          'Unavoidable Loss': '#FFA15A', 'Unused Observing Time': '#19D3F3',
          'Observatory Preparation Loss': '#B6E880',
          'Sky Quality Loss': '#FF97FF'}

actmap = {'Startup': '#636EFA', 'Opening': '#EF553B', 'WFC Tasks': '#00CC96',
          'Instrument Preparation': '#AB63FA', 'Setup': '#FFA15A',
          'Target Finalization': '#19D3F3', 'Observing': '#FF6692',
          'Standing By': '#B6E880', 'Closing': '#FF97FF', 'Shutting Down': '#FECB52'}

obsdefmap = {'Observing OP': '#FF6692', 'Calibrating OP': '#B6E880'}

instrmap = {'VBI': 'rgb(127, 60, 141)', 'ViSP': 'rgb(17, 165, 121)',
            'DL-NIRSP': 'rgb(57, 105, 172)', 'Cryo-NIRSP': 'rgb(242, 183, 1)',
            'VTF': 'rgb(201,219,116)'}

sysmap = {'Enclosure': '#636EFA', 'Mount': '#EF553B', 'Coude': '#00CC96',
          'Thermal': '#AB63FA','GIS': '#511CFB', 'HLS': '#AA0DFE', 'Instruments': '#FFA15A', 'PA&C': '#19D3F3',
          'WFC': '#FF6692', 'M1': '#00FE35', 'Feed Optics': '#B6E880', 'TEOA': '#FF97FF', 'TAT':'#FF6692',
          'Facility': 'rgb(26, 255, 150)', 'Other': '#FECB52'}

wlomap = {'Instrument Group Testing': 'rgb(26, 255, 150)', 'SciOps Testing': '#B6E880', 'TechOps Testing': '#FF97FF', 'None': 'rgb(26, 118, 255)'}

weamap = {'Clear':'rgb(230, 240, 240)', 'Thin Clouds':'#fde725', 'Thick Clouds':'rgb(85, 174, 91)',
          'Humidity':'rgb(129, 180, 227)', 'Overcast':'rgb(100, 150, 250)', 'Rain':'rgb(100,31,104)',
          'Snow/Ice':'rgb(120, 100, 202)', 'Strong Wind':'rgb(119, 74, 175)', 'Lightning':'rgb(113, 50, 141)'}

colormaps = {'con': conmap, 'act': actmap, 'sys': sysmap, 'obsdef': obsdefmap,
          'instr': instrmap, 'wlo': wlomap, 'wea': weamap}

cmap = {name:hex for name,hex in colormaps[cin].items() for namai,gohan in totals.items() if name == namai}
# print('this is cmap ', cmap)
cmapl = list(cmap.values())



# Plot them totals

pietitles = {'con': contitle, 'act': acttitle, 'sys': systitle, 'obsdef': obsdeftitle, 'instr': institle, 'wlo': wlotitle, 'wea': weatitle}

psdata = {'Operation ' + cin: kidlis,
          'Total Time': yidlis,
          'Color': cmapl}
#print(cmapl)

#print(psdata)

df = pd.DataFrame(psdata,columns=['Operation ' + cin, 'Total Time', 'Color'])
fig = px.pie(df, values='Total Time', names='Operation ' + cin, color='Color',
             color_discrete_sequence=cmapl)
#print(cmap)

#print("--- %s seconds ---" % (time.time() - start_time))

fig.show()

'''
print("This is pdata: ")
print(pdata)
print("This is idlis: ")
print(idlis)
print("This is timetotal(seconds): ")
print(timetotal)
'''


