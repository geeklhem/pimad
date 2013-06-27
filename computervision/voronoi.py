#!/usr/bin/env/ python
# -*- coding: utf-8 -*-

import numpy as np
import math
from random import random
import matplotlib.pyplot as plt
import itertools
import collections


def get_color():
       return itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y', 'k'])


def d(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


def voronoi_attribution(center,points):
    attribution = [0]*len(points[0,:])
    for k,x,y in itertools.izip(itertools.count(),points[0,:],points[1,:]):
        nearest = 0
        mdist = GRID
        for i,cx,cy in itertools.izip(itertools.count(),center[0,:],center[1,:]):
            dist = d((cx,cy),(x,y))
            if dist < mdist:
                mdist = dist
                attribution[k] = i                
    return attribution

def attribution_counter(attribution):
    cc = collections.Counter(attribution)
    cell_by_center = [0] * CENTERS
    for k,v in cc.iteritems():
        cell_by_center[k] = v
    return cell_by_center


def voronoi_scatter(center,points,center_size,attribution,show=True):
    color_iter = get_color()
    colors = [next(color_iter) for c in center[0,:]]
    colorlist = [colors[i] for i in attribution]

    plt.scatter(center[0,:],center[1,:],color=colors,s=center_size)
    plt.scatter(points[0,:],points[1,:],color=colorlist)

    ax = plt.gca()
    plt.xlim(0,GRID)
    plt.ylim(0,GRID) 
    if show:
        plt.show()

def voronoi_hist(cell_by_center,show=True,title="Number of cells"):
    color_iter = get_color()
    colors = [next(color_iter) for c in center[0,:]]
    plt.bar(np.arange(len(cell_by_center)),cell_by_center,color=colors)
    ax = plt.gca()
    ax.set_xlabel("Center")
    ax.set_ylabel(title)
    if show:
        plt.show()

def groupsize_corr(center_size,groupsize,show=True):
    plt.scatter(groupsize,center_size)
    ax = plt.gca()
    ax.set_xlabel("Number of cell in  group (T-L)")
    ax.set_ylabel("Center size")
    if show:
        plt.show()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GRID = 1000
CENTERS = 15
POINTS = 1000
MINSIZE = 100
MAXSIZE = 150

center = np.array(([int(random()*GRID) for x in range(CENTERS)],
                   [int(random()*GRID) for x in range(CENTERS)]))
points = np.array(([int(random()*GRID) for x in range(POINTS)],
                   [int(random()*GRID) for x in range(POINTS)]))
loners = np.array(([int(random()*GRID) for x in range(POINTS/100)],
                   [int(random()*GRID) for x in range(POINTS/100)]))
center_size = np.array([MINSIZE + int(random()*(MAXSIZE-MINSIZE)) for x in range(CENTERS)])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ANALYSIS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("Analysis \n--------------")
print("Number of centers : {0}".format(len(center[0,:])))
print("Number of cells : {0}".format(len(points[0,:])))
print("Number of loners : {0}".format(len(loners[0,:])))


attribution = voronoi_attribution(center,points)
attribution_l = voronoi_attribution(center,loners)

plt.subplot(2,1,1)
voronoi_scatter(center,points,center_size,attribution,show=False)
plt.subplot(2,1,2)
voronoi_scatter(center,loners,center_size,attribution_l)


cell_by_center = attribution_counter(attribution)
loner_by_center = attribution_counter(attribution_l)
groupsize = [T-L for T,L in zip(cell_by_center,loner_by_center)]

plt.subplot(2,2,1)
voronoi_hist(cell_by_center,show=False,title="Number of cells")
plt.subplot(2,2,2)
voronoi_hist(loner_by_center,show=False,title="Number of loners")
plt.subplot(2,2,3)
voronoi_hist(groupsize,show=False,title="Group size")
plt.subplot(2,2,4)
groupsize_corr(center_size,groupsize)
