#!/usr/bin/python

import sys
import re
import os
import epic as ep
import matplotlib.pyplot as plt
import ast
import argparse
import numpy as np
from collections import OrderedDict

mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input", default="../dat/json.dat",
     help='Specify the name of input time log file')
argparser.add_argument("-ib", "--input_bw", default="../dat/bw.csv",
     help='Specify the name of input bandwidth file')
argparser.add_argument("-ip", "--input_phase", default="../dat/phase.log",
     help='Specify the name of input phase file')
argparser.add_argument("-o","--output", default="output",
    help='Specify the name of output PDF file')
argparser.add_argument("-m","--subplot_cnt", default=4, type=int,
    help='Specify the maximum possible Executor IDs')
args = argparser.parse_args()

os.environ["DISPLAY"]=":0"
with open(args.input, "r") as t:
    timedict_eid_tid={}

    # Read logs line by line
    while(1):
        txt=t.readline()
        if txt == "":
            break
        txt=re.sub("false", "False", txt)
        txt=re.sub("true", "True", txt)

        # parse line text as a python dictionary
        log=ast.literal_eval(txt)

        trash=[]
        if log["Event"] == "SparkListenerApplicationStart":
            trash.append(log["Timestamp"])
            start_time=trash[0]

        elif log["Event"] == "SparkListenerTaskEnd":
            # assert (int(task_info["Finish Time"]) - int(task_info["Launch Time"])) > 0
            task_info = log["Task Info"]
            current_eid = task_info["Executor ID"]
            current_tid = task_info["Task ID"]
            stage_id = log["Stage ID"]
            if current_eid in timedict_eid_tid.keys():
                # Append "new tid" and its start/end time logs
                timedict_eid_tid[current_eid][current_tid]=[[task_info["Launch Time"]-start_time],
                                                            [task_info["Finish Time"]-start_time],
                                                             stage_id]
            else:
                # First time for each eid, initialize "tid dict" with corresponding time logs
                timedict_eid_tid[current_eid]={current_tid:[[task_info["Launch Time"]-start_time],
                                                            [task_info["Finish Time"]-start_time],
                                                             stage_id]}

# Set # of subplots & real data
subplot_cnt = args.subplot_cnt
max_eid_from_data = len(timedict_eid_tid.keys())

with open(args.input_phase, "r") as p:
    phaseTime = []

    # Read logs line by line
    while(1):
        txt=p.readline()
        if txt == "":
            break

        # parse line text as a python dictionary
        log=ast.literal_eval(txt)

        if log["Event"] == "PhaseGuard":
            phase_info = log["Phase Info"]
            pid = phase_info["Phase ID"]
            phaseTime.append(phase_info["Timestamp"]-start_time)
            # print pid,":",phase_info["Timestamp"]-start_time


# Draw graphs per Executor IDs
Dall = []

for k in range(subplot_cnt):
    # Skip if denoted subplot_cnt exceeds max_eid from data
    if k >= max_eid_from_data:
        continue
    # ========================================================================================
    #  Draw timeline subplots: Task timeline
    # ========================================================================================
    D = []
    # Sort timedict by keys (tid)
    OrderedLog=OrderedDict(sorted(timedict_eid_tid[str(k)].items(), key=lambda t: t[0], reverse=True))

    # Append dummy values to display graphs from 0
    stage_min_max = {}
    D.append(ep.Group(None, [0], [100]))
    for tid, time_log in OrderedLog.iteritems():
        # Group(None, <Launch time>, <Finish Time>)
        D.append(ep.Group(None, time_log[0], time_log[1], color=mc["blue"]))

        # Update min/max of each stages
        if time_log[2] in stage_min_max.keys():
            # find min
            if stage_min_max[time_log[2]][0] > time_log[0][0]:
                stage_min_max[time_log[2]][0] = time_log[0][0]
            # find max
            if stage_min_max[time_log[2]][1] < time_log[1][0]:
                stage_min_max[time_log[2]][1] = time_log[1][0]
        else:
            # virtual max, min
            stage_min_max[time_log[2]]=[99999999,-999]
    Dall.append(D)

SP = ep.SubPlotter(subplot_cnt+1, width=10, height=15, sharex=True)
SP.adjust(hspace=0.45)

for k in range(max_eid_from_data):
    CBOP = ep.BoxPlotter(axis=SP.getAxis(k), title="Timeline (for Executor %s)" % str(k),
                         xlabel="Time", ylabel="Task ID")
    CBOP.setLegendStyle(ncol=4, loc="upper center", frame=False)
    CBOP.setFigureStyle(vertical=False, figmargin=0.05)

    # Draw vertical lines for stages
    finish = 0
    for v in stage_min_max.values():
        CBOP.vline(x=v[0], yrange=[0,100], color="black", linestyle="--")
        finish = v[1]
    CBOP.vline(x=finish, yrange=[0,100], color="black", linestyle="--")

    # Draw vertical lines for phases
    for pt in phaseTime:
        CBOP.vline(x=pt, yrange=[0,100], color="green", linestyle=":")

    CBOP.draw(*Dall[k], boxwidth=.1, linewidth=.01)
    CBOP.finish()

# ========================================================================================
# Draw line subplots: Bandwidth 
# ========================================================================================
PP = ep.PatternParser(ep.tRead(args.input_bw))
PP.ParseWith(",")
PP.datList = np.array(ep.tTranspose(PP.datList[1:])) * 1000

BWdata = ep.Group(None, PP.datList[1], PP.datList[3], color="red", marker="x")

LP = ep.LinePlotter(axis=SP.getAxis(subplot_cnt), title="Total bandwidth",
    xlabel="Time (ms)", ylabel="Bandwidth (GB/sec)")
LP.setFigureStyle(markersize=0)

# Draw stages
for v in stage_min_max.values():
    LP.vline(x=v[0], yrange=[0,100], color="black", linestyle="--")
    finish = v[1]
LP.vline(x=finish, yrange=[0,100], color="black", linestyle="--")
for pt in phaseTime:
    LP.vline(x=pt, yrange=[0,100], color="green", linestyle=":")

LP.draw(BWdata)


# ========================================================================================
# Draw line subplots: Average Bandwidth
# ========================================================================================

# Get average
phaseTime += [stage_min_max.values()[-1][1]]
avg_bw = []
j = 0
cnt = 0
sum_bw = 0
for i in range(len(PP.datList[1])):
    if PP.datList[1][i] < phaseTime[j]:
        sum_bw = sum_bw + PP.datList[3][i]
        cnt = cnt + 1
        # print PP.datList[1][i], "<", phaseTime[j], PP.datList[3][i], sum_bw, cnt
    else:
        if cnt != 0:
            avg_bw.append(sum_bw/cnt)
        else:
            avg_bw.append(0)
        # print j, avg_bw[j]
        j = j + 1
        if j == len(phaseTime):
            break
        sum_bw = 0
        cnt = 0

# Draw graphs
phaseTime_aux = [stage_min_max.values()[0][0]]
for i in phaseTime[0:-1]:
    phaseTime_aux = phaseTime_aux + [i,i]
phaseTime_aux += [phaseTime[-1]]

avg_bw_aux=[]
for i in avg_bw:
    avg_bw_aux = avg_bw_aux + [i,i]

BWdata_avg = ep.Group(None, phaseTime_aux, avg_bw_aux, color="black", marker="")

LP.draw(BWdata_avg)

LP.finish()

# Manual hack of subplot xlim, originally epic-py sets whitespace ratio from args (figmargin)
# plt.xlim([0,stage_min_max.values()[-1][-1]*1.05])
plt.xlim([0,130000])
plt.ylim([0,30000])


SP.saveToPdf("%s.pdf" % args.output)
