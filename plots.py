#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Visualisation functions for model traces using matplotlib"""

import pylab as plt
import numpy as np

def proportions(traces):
    general = np.zeros((len(traces),2))
    for n,trace in enumerate(traces):
        general[n,0] = sum(trace[:,1])
        general[n,1] = sum(trace[:,3])
    X = range(len(trace))
    Y1 = general[:,0]
    Y2 = general[:,1]
    #Y3 =  general[:,2]
    #Y4 =  general[:,3]
    plt.bar(X,Y1, facecolor='#9999ff', edgecolor='white',label="In group")
    plt.bar(X,Y2,bottom=Y1, facecolor='#ff9999', edgecolor='white',label="Alone")
    plt.legend(loc='lower right')
    #plt.bar(X,Y3,bottom=Y2, facecolor='#99ff99', edgecolor='white')
    #plt.bar(X,Y4,bottom=Y3, facecolor='#ffff99', edgecolor='white')
    plt.xlabel("Generations")
    plt.show()
