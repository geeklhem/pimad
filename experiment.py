#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Experiment"""
import sys
import math

import trace
import plots
from toymodel import ToyModel

if sys.argv[1] == "c":
    print("Create")
    param = {"N":100000,
             "T":1000,
             "b":20,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.8*0.3),
             "mu":0.01}

    tracked_values = ["population.proportions"]

    a = ToyModel(param, tracked_values)

    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.population)
    print("\n Run:")
    a.play(50)
    test = trace.Trace(a)
    trace.save_trace(test,"name.data")

elif sys.argv[1] == "l":
    print("Load trace as loaded")
    loaded = trace.load_trace("name.data")
    plots.proportions(loaded.traces[0]["population.proportions"],True,False)
    plots.proportions(loaded.traces[0]["population.proportions"],False,True)
    plots.proportions(loaded.traces[0]["population.proportions"],True,True)

else:
    print("Nothing")
