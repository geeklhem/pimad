#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Visualisation functions for model traces using matplotlib"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import pylab as plt
import numpy as np

def groupsize_density(trace,T):
    """Visualize group density from population.proportions
 
    :param traces: population.proportions value. 
    :type traces: np.array float"""
    
    grps_size = []

    for i in trace[:,2]:
        grps_size += [i]*i
    for i in trace[:,1]:
        grps_size += [1]*i
    plt.hist(grps_size,T,histtype="step")
    plt.xlim(0, T)
    plt.xlabel("Group size")
    plt.ylabel("Number of individuals experiencing it")
    plt.show()
    

def proportions(traces,phenotype=True,group=True):
    """Visualize population.proportions traces
    
    :param traces: Successives population.proportions values. 
    :type traces: list
    :param phenotype: Split the data by social/asocial.
    :param group: Split the data by in group/alone.
    :type phenotype: bool
    :type group: bool

    .. warning::
      Raise an exception if phenotype and group are False.
"""
    general = np.zeros((len(traces),4))
    for n,trace in enumerate(traces):
        general[n,0] = sum(trace[:,0])
        general[n,1] = sum(trace[:,1])
        general[n,2] = sum(trace[:,2])
        general[n,3] = sum(trace[:,3])

    X = range(len(traces))
   
    if phenotype and group:
        Y1 = general[:,1] - general[:,0] 
        Y2 = general[:,3] - general[:,2]
        Y3 = general[:,0]
        Y4 = general[:,2]
        plt.bar(X,Y1,
                facecolor='#9999ff', edgecolor='white',
                label="Asocial in group")
        plt.bar(X,Y2,bottom=Y1
                , facecolor='#ff9999', edgecolor='white',
                label="Asocial alone")
        plt.bar(X,Y3,bottom=Y2+Y1,
                facecolor='#99ff99', edgecolor='white',
                label="Social in group")
        plt.bar(X,Y4,bottom=Y3+Y2+Y1,
                facecolor='#ffff99', edgecolor='white',
                label="Social alone")
    
    elif phenotype and not group:
        Y1 = general[:,0]+general[:,2]
        Y2 = general[:,3]+general[:,1]-Y1
        plt.bar(X,Y1, facecolor='#9999ff', edgecolor='white',label="Social")
        plt.bar(X,Y2,bottom=Y1, facecolor='#ff9999', edgecolor='white',label="Asocial")

    elif not phenotype and  group:
        Y1 = general[:,1]
        Y2 = general[:,3]

        plt.bar(X,Y1, facecolor='#9999ff', edgecolor='white',label="In group")
        plt.bar(X,Y2,bottom=Y1, facecolor='#ff9999', edgecolor='white',label="Alone")


    else:
        raise Exception("One of the boolean parameters must be True.")

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
    plt.xlabel("Generations")
    plt.show()


def groupsize_surface(trace):
    generations=len(trace.traces[0]["population.proportions"])
    Z = trace.grpsize_density
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    Y = np.arange(0, trace.p["T"]+1, 1)
    X = np.arange(0, generations, 1)
    X, Y = np.meshgrid(X, Y)
    

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
            linewidth=0, antialiased=False)

    plt.ylabel("Group size")
    plt.xlabel("Generation")

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    plt.show()

if __name__ == "__main__":
    import math
    from toymodel import ToyModel
    param = {"N":100000,
             "T":100,
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

    #print(a.traces)
    #groupsize_density(a.traces[0]["population.proportions"][0],a.population.T)
    #groupsize_density(a.traces[0]["population.proportions"][9],a.population.T)
    proportions(a.traces[0]["population.proportions"],True,False)
    proportions(a.traces[0]["population.proportions"],False,True)
    proportions(a.traces[0]["population.proportions"],True,True)
    
