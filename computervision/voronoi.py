#!/usr/bin/env/ python
# -*- coding: utf-8 -*-

import numpy as np
import math
from random import random
import matplotlib.pyplot as plt
import itertools
import collections

center = np.array(([int(random()*100) for x in range(5)],[int(random()*100) for x in range(5)]))

points = np.array(([int(random()*100) for x in range(100)],[int(random()*100) for x in range(100)]))


def d(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

plt.scatter(center[0,:],center[1,:],color=colors,s=75)


def voronoi_attribution(center,points):
    attribution = [0]*len(points[0,:])
    colors = ["r","b","g","y","k"]
    for k,x,y in itertools.izip(itertools.count(),points[0,:],points[1,:]):
        nearest = 0
        mdist = 100
        for i,cx,cy in itertools.izip(itertools.count(),center[0,:],center[1,:]):
            dist = d((cx,cy),(x,y))
            if dist < mdist:
                mdist = dist
                attribution[k] = i                
    return attribution


attribution = voronoi_attribution(center,points)
colorlist = [colors[i] for i in attribution]

plt.scatter(points[0,:],points[1,:],color=colorlist)

ax = plt.gca()
plt.xlim(0,100)
plt.ylim(0,100) 
plt.show()

h = collections.Counter(colorlist)
plt.clf()
ax = plt.gca()
plt.bar(np.arange(len(h.values())),h.values(), color= h.keys())
ax.set_xlabel("Center")
ax.set_ylabel("Number of cells")
plt.show()
