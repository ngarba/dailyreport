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

*~*
V.22
*~*

*Operation Conditions*          *Operation Activities*              In system 7 Technical Loss:
1 Normal                        1 Starting Up                       1 Enclosure
2 Test OP                       2 Opening                           2 Mount
3 SciOps Testing                3 WFC Daily Calibrations            3 Coude
4 Setup                         4 Target Finalization               4 Thermal
5 Weather Loss                  5 Observing                         5 GIS
6 Operational Execution Loss    6 Standing By                       6 HLS
7 Technical Loss                7 Closing                           7 Instruments
8 Unavoidable Loss              8 Shutting Down                     8 PA&C
9 Unused Observing Time         9 Handover Note                     9 WFC
10 Instrument Group Testing                                         10 Other

Weather Conditions              In obsdefinition 2 Test OP:         In setupoption 4 Setup:
1 Clear                         1 Observing OP                      1 FIDO
2 Thin Clouds                   2 Calibrating OP                    2 Instruments
3 Thick Clouds                                                      In Setup > fidooption
4 Humidity                      In 3 SciOps Testing:                1 M9a/DL-FM1
5 Overcast                      Some don't have insselection        2 New FIDO Config
6 Rain                          1 VBI
7 Snow/Ice                      2 ViSP                              In insselection 10 IGT
8 Strong Wind                   3 DL-NIRSP                          1 VBI
9 Lightning                     4 VTF                               2 ViSP
                                5 Cryo-NIRSP                        3 DL-NIRSP
In obsdefinition 5 Observing:   6 PA&C                              4 VTF
1 Observing OP                  7 WFC                               5 Cryo-NIRSP
2 Calibrating OP                                                    6 PA&C
                                                                    7 WFC
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


# gib
f = open('activitylogs22.json')

# returns json data as a dictionary
jata = json.load(f)


for i in jata['entries']:
    # Getting daytoday(unix epoch) to be a timestamp(the key value and date for the x axis
    day = int(int(i['fields']['daytoday']) / 1000)
    # Date in string
    timestamp = str(pd.to_datetime(day, unit='s'))[0:10]

    '''
    Code reads everything per iteration (recordID)
    When code sees timestamp requested
    Code starts creating dictionary of cons/acts/selects
    '''

    tes = (i['fields']['timeeventstarts'])
    tee = (i['fields']['timeeventends'])

    tevent = dt.datetime.strptime(tee, '%H:%M') - dt.datetime.strptime(tes, '%H:%M')


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

# Weather
# Needs to be stripped of [&quot; before implemented
#     1:Clear 2:Thin Clouds 3:Thick Clouds 4:Humidity 5:Overcast 6:Rain 7:Snow/Ice
#     8:Strong Wind 9:Lightning
#    weather = (i['fields']['weatherconditions'])