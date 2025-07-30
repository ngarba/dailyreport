'''
Make a Sunburst out of conditions and activities

V.26
'''


import json
import datetime as dt
import time
import pandas as pd
from itertools import cycle
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


# gib
f = open('activitylogs26.json')

# returns json data as a dictionary
jata = json.load(f)

daterange = []
drange = daterange
alldata = {}
pdata = {}



for i in jata['entries']:
    id = (i['recordId'])
    # Getting daytoday(unix epoch) to be a timestamp(for adding to the daterange list)
    day = int(int(i['fields']['daytoday']) / 1000)
    # Date in string
    date = str(pd.to_datetime(day, unit='s'))[0:10]

    tes = (i['fields']['timeeventstarts'])
    tee = (i['fields']['timeeventends'])

    tevent = dt.datetime.strptime(tee, '%H:%M') - dt.datetime.strptime(tes, '%H:%M')
    svalue = tevent.total_seconds()

# Start of reading json fields

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

    # WL option in 2 Weather Loss
    #     1: WL:Instrument Group Testing 2: WL: SciOps Testing 3: WL: TechOps Testing 4: None
    wlo = (i['fields']['wloptions'])

    # TechOpsTest in 9 TechOps Testing
    #     1:Enclosure 2:Mount 3:Coude 4:Thermal 5:GIS 6:M1 7:Feed Optics
    #     8:TEOA 9:Vibration 10:Other
    tech = (i['fields']['techopstest'])

    # Instrument Group Testing and SciOps Testing
    #     1:HLS 2:PA&C 3:WFC 4:Instruments 5:Other
    insci = (i['fields']['instscitest'])

    # Insselection or instrument selection both 8 SciOps Testing and 7 Ins Group Testing
    # 1:VBI 2:ViSP 3:DL-NIRSP 4:VTF 5:Cryo-NIRSP
    instr = (i['fields']['insselection'])
    instr = instr.replace("&quot;", "")
    instr = instr.replace("[", "")
    instr = instr.replace("]", "")

# End of reading json fields


    alldata[id] = (date, con, act, svalue, obsdef)
# all the data

# Start of the date section

    if date not in daterange:
        daterange.append(date)

fdate = '2024-09-25'
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
ldate = '2024-11-08'

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

#print(daterange)

# End of the date section


ddata = {dk:dv for dk,dv in alldata.items() if dv[0] in list(drange)}
# ddata (date-specific data) is all items, but only if in date range and if the condition category isn't empty

print('ddata: ', ddata)
datk = []
for duk,duv in ddata.items():
    datk.append(duv[0])

# Figuring out how to title stuff

acttitle = {'1': 'Startup', '2': 'Opening', '3': 'WFC Tasks',
         '4': 'Instrument Preparation', '5': 'Setup',
         '6': 'Target Finalization', '7': 'Observing', '8': 'Standing By',
         '9': 'Closing', '10': 'Shutting Down', "": ""}
# make this act value (av)

contitle = {'1': 'Normal', '2': 'Weather Loss', '3': 'Operation Exec Loss',
'4': 'Technical Loss', '5': 'Unavoidable Loss',
'6': 'Unused Observing Time', '7': 'Instrument Group Testing', '8': 'SciOps Testing',
'9': 'TechOps Testing'}

obsdeftitle = {'1': 'Observing OP', '2': 'Calibrating OP', "":""}


# con value (cv)
# act value (av)
# sec value (svalue)

cdata = {dk: [cv, av, dv[3], ov] for dk,dv in ddata.items()
         for ck,cv in contitle.items() if ck == dv[1]
         for ak,av in acttitle.items() if ak == dv[2]
         for ok,ov in obsdeftitle.items() if ok == dv[4]
         if dv[0] == dv[0]}
# cdata (categoried data) turns condition and activity numbers into their names


print('cdata: ', cdata)

sumdata = []
condata = []
actdata = []
dvalues = []
obsdata = []
for ck,cv in cdata.items():
    condata.append(cv[0])
    actdata.append(cv[1])
    dvalues.append(cv[2])
    obsdata.append(cv[3])

allstuff = condata + actdata
alldata = [set(allstuff)]

# actdata = [None if act == '' else act for act in actdata]
#
# print(actdata)

piedata = {
    'activities': actdata,
    'conditions': condata,
    'date': datk,
    'time': dvalues,
    'obs': obsdata
}

print(piedata)

df = pd.DataFrame(piedata, columns=['activities', 'conditions', 'date', 'time'])
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
# df = (df.groupby(['conditions', 'activities'])['time'].sum()
#       .reset_index(name='time')
#       .replace({'': None}))

print(df)

fig = px.sunburst(
    df,
    path=['conditions', 'activities'],
    values='time',
    branchvalues='total',
)

fig.update_traces(textinfo='label+percent entry')

fig.show()

# fig2 = px.bar(
#     df,
#     x='date',
#     y='time',
#     color='conditions',
# )
#
# fig2.show()