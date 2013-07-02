#!/usr/bin/env/ python
# -*- coding: utf-8 -*-

import numpy as np
import math
from random import random
import matplotlib.pyplot as plt
import itertools
import collections
from matplotlib.patches import Circle
import glob
import os

def get_color():
       return itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y', 'k'])


def d(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)


def voronoi_attribution(center,points):
    attribution = [0]*len(points[0,:])
    for k,x,y in itertools.izip(itertools.count(),points[0,:],points[1,:]):
        nearest = 0
        mdist = d((center[0,0],center[1,0]),(x,y))+1
        for i,cx,cy in itertools.izip(itertools.count(),center[0,:],center[1,:]):
            dist = d((cx,cy),(x,y))
            if dist < mdist:
                mdist = dist
                attribution[k] = i                
    return attribution

def attribution_counter(attribution,nb_centers):
    cc = collections.Counter(attribution)
    cell_by_center = [0] * nb_centers
    for k,v in cc.iteritems():
        cell_by_center[k] = v
    return cell_by_center


def voronoi_scatter(center,points,center_size,attribution,show=True):
    color_iter = get_color()
    colors = [next(color_iter) for c in center[0,:]]
    colorlist = [colors[i] for i in attribution]

    plt.scatter(points[0,:],points[1,:],color=colorlist)

    ax = plt.gca()
    for x,y,c,s in zip(center[0,:],center[1,:],colors,center_size):
           ax.add_artist(Circle(xy=(x,y),radius=math.sqrt(s/math.pi),facecolor=c,alpha=0.3))
        
    plt.xlim(0,9744*500/789)
    plt.ylim(7280*500/789,0) 
    if show:
        plt.show()

def voronoi_hist(cell_by_center,show=True,title="Number of cells"):
    color_iter = get_color()
    colors = [next(color_iter) for c in range(len(cell_by_center))]
    plt.bar(np.arange(len(cell_by_center)),cell_by_center,color=colors)
    ax = plt.gca()
    ax.set_xlabel("Center")
    ax.set_ylabel(title)
    if show:
        plt.show()

def groupsize_corr(center_size,groupsize,show=True):
    plt.scatter(groupsize,center_size)
    ax = plt.gca()
    ax.set_xlabel("Number of cell in  group")
    ax.set_ylabel("Center size")
    if show:
        plt.show()


def export_html(pointsfilelist,CENTERS):
       page = """
       <html>
       <head>
       <title>Experimental picture analysis</title>
       <style type="text/css">
        img {max-width:100%;}
       </style>
       </head><body>
       <h1>Experimental picture analysis</h1>
       """
       # CENTER
       center_html = """ <h2> Centers recognition</h2>
       Center found : {0}""".format(CENTERS)
       page += center_html

       # IMAGES
       for img in pointsfilelist:
              pics = ""
              for i in sorted(glob.glob(os.path.join("{0}_*.png".format(img)))):
                     pics += '<img src ="{path}"/>'.format(path=os.path.basename(i))
                     
              page += """
              <h2>{title}</h2>
              {pics}
              """.format(title=img,pics=pics)
    
       with open(os.path.join("index.html"), 'w') as f:
           f.write(page)

def main(centerfile,pointsfilelist,csl=1000):       
       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       # LOADING
       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       
       #Center
       final = np.genfromtxt(centerfile,
                             usecols=(1,5,6),
                             skip_header=1,names=("area","x","y"))

       center = np.transpose(np.array([(x,y) for ar,x,y in final if ar>csl]))
       center_size = np.array(([ar for ar,x,y in final if ar>csl]))
       CENTERS = len(center[0,:])

       #Points for successives images
       #pointsfilelist.append(centerfile)
       points = []
       for image in pointsfilelist:
              pts = np.genfromtxt(image,
                                  usecols=(1,5,6),
                                  skip_header=1,
                                  names=("area","x","y"))
              points.append(np.transpose(np.array([(x,y) for ar,x,y in pts if ar < csl])))
       
       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       # Export
       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

       for name,pts in zip(pointsfilelist,points):
              print("Analysis of Image {0}\n--------------".format(name))
              
              attribution = voronoi_attribution(center,pts)
              
              voronoi_scatter(center,pts,center_size,attribution,show=False)

              f = plt.gcf()
              f.set_dpi(150)
              d = f.get_size_inches()
              f.set_size_inches( (d[0],d[0]) )
              plt.savefig("{}_00scatter.png".format(name),bbox_inches="tight")
              plt.clf()

              cell_by_center = attribution_counter(attribution,CENTERS)
              #groupsize = [T-L for T,L in zip(cell_by_center,loner_by_center)]

              
              voronoi_hist(cell_by_center,show=False,title="Number of cells")

              plt.savefig("{}_01bar.png".format(name),bbox_inches="tight")
              plt.clf()
              
              groupsize_corr(center_size,cell_by_center,show=False)

              plt.savefig("{}_02corr.png".format(name),bbox_inches="tight")
              plt.clf()


       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       # Export HTML
       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

       export_html(pointsfilelist,CENTERS)
       
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
# MOCK DATA
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
center_size = np.array([MINSIZE + int(random()*(MAXSIZE-MINSIZE)) for x in range(CENTERS)])"""




