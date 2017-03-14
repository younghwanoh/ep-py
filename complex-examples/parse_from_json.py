#!/usr/bin/python

import sys
import re
import os
import epic as ep
import ast
import argparse
from collections import OrderedDict

mc = {"green":"#225522", "yellow":"#FFBB00", "red":"#BC434C", "purple":"#B82292",
      "blue":"#4455D2", "white":"#FFFFFF", "ddwhite":"#B3B3B3", "dwhite":"#DFDFDF",
      "gray":"#888888", "dgray":"#4F4F4F", "black":"#000000"}

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input", default="../dat/json.dat",
     help='Specify the name of input data file')
argparser.add_argument("-o","--output", default="output",
    help='Specify the name of output PDF file')
argparser.add_argument("-m","--max_eid", default=4, type=int,
    help='Specify the maximum possible Executor IDs')
args = argparser.parse_args()

os.environ["DISPLAY"]=":0"
with open(args.input, "r") as t:
    eid={}

    # Read logs line by line
    while(1):
        txt=t.readline()
        if txt == "":
            break
        txt=re.sub("false", "False", txt)
        txt=re.sub("true", "True", txt)

        # As a python dictionary
        log=ast.literal_eval(txt)
        trash=[]
        try:
            if log["Event"] == "SparkListenerApplicationStart":
                trash.append(log["Timestamp"])
                start_time=trash[0]

            elif log["Event"] == "SparkListenerTaskEnd":
                # assert (int(task_info["Finish Time"]) - int(task_info["Launch Time"])) > 0
                task_info = log["Task Info"]
                current_eid = task_info["Executor ID"]
                current_tid = task_info["Task ID"]
                stage_id = log["Stage ID"]
                if current_eid in eid.keys():
                    # Append "new tid" and its elem
                    eid[current_eid][current_tid]=[[task_info["Launch Time"]-start_time],
                                                   [task_info["Finish Time"]-start_time],
                                                   stage_id]
                else:
                    # First time, initialize "tid Hash" wieh corresponding elem
                    eid[current_eid]={current_tid:[[task_info["Launch Time"]-start_time],
                                                   [task_info["Finish Time"]-start_time],
                                                   stage_id]}
        except:
            pass

# Draw graphs per Executor IDs
for k in range(args.max_eid):
    D = []
    # Sort eid by keys (tid)
    OrderedLog = OrderedDict(sorted(eid[str(k)].items(), key=lambda t: t[0], reverse=True))

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

    CBOP = ep.BoxPlotter(title="Timeline (for Executor %s)" % str(k), width=10, height=6,
                         xlabel="Time", ylabel="Task ID")
    CBOP.setLegendStyle(ncol=4, loc="upper center", frame=False)
    CBOP.setFigureStyle(vertical=False, figmargin=0.05)

    # Draw vertical line for stages
    for v in stage_min_max.values():
        CBOP.vline(x=v[0], yrange=[0,100], color="black", linestyle="--")
        CBOP.vline(x=v[1], yrange=[0,100], color="red", linestyle="--")

    CBOP.draw(*D, boxwidth=.1, linewidth=.01)
    CBOP.saveToPdf("%s-%d.pdf" % (args.output,k))
