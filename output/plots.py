#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Visualisation functions for model traces using matplotlib"""

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import FuncFormatter

import matplotlib.pyplot as plt
import numpy as np

def saveplot(name,fct,args,kargs={"show":False},p=(8,8)):
    fct(*args,**kargs)
    f = plt.gcf()
    f.set_dpi(150)
    #d = f.get_size_inches()
    f.set_size_inches( p )
    plt.savefig(name+".png",bbox_inches="tight")
    plt.clf()



def proportions(trace_object,phenotype=True,group=True,show=True):
    """Visualize population.proportions traces
    
    :param trace_object: Traces containing object 
    :type traces: Trace
    :param phenotype: Split the data by social/asocial.
    :param group: Split the data by in group/alone.
    :type phenotype: bool
    :type group: bool

    .. warning::
      Raise an exception if phenotype and group are False.
"""
    traces = trace_object.traces[0]["population.proportions"]
    general = np.zeros((len(traces),4))
    for n,trace in enumerate(traces):
        general[n,0] = sum(trace[:,0])
        general[n,1] = sum(trace[:,1])
        general[n,2] = sum(trace[:,2])
        general[n,3] = sum(trace[:,3])

    X = range(len(traces))
    names = ("Asocial","Social")
    names = ("Resident","Mutant")
   
    if phenotype and group:
        Y1 = general[:,1] - general[:,0] 
        Y2 = general[:,3] - general[:,2]
        Y3 = general[:,0]
        Y4 = general[:,2]
        plt.bar(X,Y1,
                facecolor='#9999ff', edgecolor='none',
                label=names[0]+" in group")
        plt.bar(X,Y2,bottom=Y1
                , facecolor='#ff9999', edgecolor='none',
                label=names[0]+" alone")
        plt.bar(X,Y3,bottom=Y2+Y1,
                facecolor='#99ff99', edgecolor='none',
                label=names[1]+" in group")
        plt.bar(X,Y4,bottom=Y3+Y2+Y1,
                facecolor='#ffff99', edgecolor='none',
                label=names[1]+" alone")
    
    elif phenotype and not group:
        Y1 = general[:,0]+general[:,2]
        Y2 = general[:,3]+general[:,1]-Y1
        plt.bar(X,Y1, facecolor='#9999ff', edgecolor='none',label=names[1])
        plt.bar(X,Y2,bottom=Y1, facecolor='#ff9999', edgecolor='none',label=names[0])

    elif not phenotype and  group:
        Y1 = general[:,1]
        Y2 = general[:,3]

        plt.bar(X,Y1, facecolor='#9999ff', edgecolor='none',label="In group")
        plt.bar(X,Y2,bottom=Y1, facecolor='#ff9999', edgecolor='none',label="Alone")


    else:
        raise Exception("One of the boolean parameters must be True.")

    def percent_tick(y, pos=0):
        return '{:1.0f}%'.format(float(y)/trace_object.p["N"]*100)

    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(percent_tick))
    plt.xlim((0,len(general[:,2])))

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
    plt.xlabel("Generations")
    plt.ylabel("Proportion")
    if show:
        plt.show()

    

def groupsize_surface(trace,show=True):
    generations=len(trace.traces[0]["population.proportions"])
    Z = trace.grpsize_density
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    Y = np.arange(0, trace.p["T"]+1, 1)
    X = np.arange(0, generations, 1)
    X, Y = np.meshgrid(X, Y)
    

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.prism_r,
            linewidth=0, antialiased=False)

    plt.ylabel("Group size")
    plt.xlabel("Generation")



    def percent_tick(y, pos=0):
        return '{:1.0f}%'.format(float(y)*100)

    ax = plt.gca()
    

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FuncFormatter(percent_tick))

    ax.view_init(35,50)
    if show:
        plt.show()



def group_level_cov(trace, show=True):
    
    X = range(len(trace.covPrice))
    Y = trace.covPrice
    plt.scatter(X,Y)

    plt.ylabel("Group-level covariance")
    plt.xlabel("Generation")

    if show:
        plt.show()

def routine_graphes(tr):
    groupsize_surface(tr)
    proportions(tr,True,False)
    proportions(tr,False,True)
    proportions(tr,True,True)
    group_level_cov(tr)


def epigenetic_trajectory(trace,show=True):
    data = trace.traces[0]["global_proportions"]
    data = np.array(data)
    
    plt.plot(data[:,0],data[:,1]) 
    plt.xlabel("Proportion of social genotype")
    plt.ylabel("Proportion of social phenotype")
    plt.xlim((0,1))
    plt.ylim((0,1))
    
    if show:
        plt.show()

def global_proportions(trace,show=True):
    data = trace.traces[0]["global_proportions"]
    data = np.array(data)
    plt.plot(range(len(data[:,0])),data[:,0],label="Genotype")
    plt.plot(range(len(data[:,1])),data[:,1],label="Phenotype")
    plt.xlabel("Generation")
    plt.ylabel("Proportion of social")
    plt.ylim((0,1))
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
    if show:
        plt.show()


def main():
    import math
    import sys
    sys.path.append("../models")
    import toymodel as tm
    import traces

    
    param = {"N":1000,
             "T":100,
             "ip":0.5,
             "b":20,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.8*0.3),
             "mu":0.01}

    #tracked_values = ["population.proportions"]
    tracked_values = ["global_proportions"]

    a = tm.ToyEpigenetic(param, tracked_values)

    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.population)
    print("\n Run:")
    a.play(50)
    
    tr = traces.Trace(a)
    #routine_graphes(tr)
    epigenetic_trajectory(tr)


if __name__ == "__main__":
    main()
