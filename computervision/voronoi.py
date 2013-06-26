#!/usr/bin/env/ python
# -*- coding: utf-8 -*-

import numpy as np
import math
from random import random
import matplotlib.pyplot as plt
import itertools

center = np.array(([int(random()*100) for x in range(5)],[int(random()*100) for x in range(5)]))
colors = ["r","b","g","y","k"]
points = np.array(([int(random()*100) for x in range(100)],[int(random()*100) for x in range(100)]))
colorlist = [""]*100

def d(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

plt.scatter(center[0,:],center[1,:],color=colors,s=75)

for k,x,y in itertools.izip(itertools.count(),points[0,:],points[1,:]):
  nearest = 0
  mdist = 100
  for i,cx,cy in itertools.izip(itertools.count(),center[0,:],center[1,:]):
      dist = d((cx,cy),(x,y))
      if dist < mdist:
          mdist = dist
          colorlist[k] = colors[i]

plt.scatter(points[0,:],points[1,:],color=colorlist)
ax = plt.gca()
plt.xlim(0,100)
plt.ylim(0,100) 
plt.show()
