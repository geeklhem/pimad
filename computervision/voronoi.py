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
    #print(points)
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
    to_sort = zip(cell_by_center,colors)
    to_sort.sort(key = lambda x: -x[0])
    values, colors = zip(*to_sort)
    plt.bar(np.arange(len(cell_by_center)),values,color=colors)
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
                             usecols=(1,2,3),
                             skip_header=1,
                             delimiter=",",
                             names=("area","x","y"))

       center = np.transpose(np.array([(x,y) for ar,x,y in final if ar>csl]))
       center_size = np.array(([ar for ar,x,y in final if ar>csl]))
       CENTERS = len(center[0,:])

       #Points for successives images
       #pointsfilelist.append(centerfile)
       points = []
       points_names = []
       images = np.genfromtxt(pointsfilelist,
                              skip_header=1,
                              delimiter=",",
                              usecols=(1,2,3,4),
                              names=("area","x","y","img"))

       for img in range(1,int(images["img"][-1])+1):
              points.append((np.transpose(np.array([(x,y) 
                                                    for ar,x,y,sl 
                                                    in images
                                                    if (ar < csl and sl == img)]))))
              points_names.append("slice_{}".format(img))


       
       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       # Export
       # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       attributions = []
       for pts in points:
              print("Analysis of Image {0}\n--------------".format(name))
              attributions.append(voronoi_attribution(center,pts))
                     
       for name,pts,attribution in zip(points_names,points,attributions):
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

       export_html(points_names,CENTERS)


class Experiment(object):
       """Hold data about a film """
       def __init__(self,centerfile,pointsfile,csl=1000):
              # LOADING
              self.X = 9744*500/789
              self.Y = 7280*500/789
              self.load_data(centerfile,pointsfile,csl=1000)
              

       def _topoints(self,x,y):
              return np.transpose(np.array(zip(x,y)))
      
       def edges(self):
              x = range(int(self.X))
              y = range(int(self.Y))
              x0 = [0] * int(self.X) 
              y0 = [0] * int(self.Y)
              xmax = [self.X] * int(self.X) 
              ymax = [self.Y] * int(self.Y)
              
              # Set have only one occurance of each element
              top = frozenset(voronoi_attribution(self.centers,self._topoints(x,ymax)))
              left = frozenset(voronoi_attribution(self.centers,self._topoints(x0,y)))
              right = frozenset(voronoi_attribution(self.centers,self._topoints(xmax,y)))
              bottom = frozenset(voronoi_attribution(self.centers,self._topoints(x,y0)))
              return list(frozenset().union(top,left,right,bottom))

       def process(self):
              self.edges_centers = self.edges()
              self.attributions = []
              self.cell_by_center = []

              for pts,name in zip(self.points,self.frame_names):
                     print("Analysis of Image {0}\n--------------".format(name))
                     att = voronoi_attribution(self.centers,pts)
                     self.attributions.append(att)
                     self.cell_by_center.append(attribution_counter(att,self.C))
                                  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# LOAD  DATA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

       def load_data(self,centerfile,pointsfile,csl=1000):

              final = np.genfromtxt(centerfile,
                                    usecols=(1,2,3),
                                    skip_header=1,
                                    delimiter=",",
                                    names=("area","x","y"))

              images = np.genfromtxt(pointsfile,
                                     skip_header=1,
                                     delimiter=",",
                                     usecols=(1,2,3,4),
                                     names=("area","x","y","img"))


              # Centers
              self.centers = np.transpose(np.array([(x,y) for ar,x,y in final if ar>csl]))
              self.center_size = np.array(([ar for ar,x,y in final if ar>csl]))
              self.C = len(self.centers[0,:])
              
              # Points for successives images
              self.points = []
              self.frame_names = []
              self.N = []
              
              for img in range(1,int(images["img"][-1])+1):
                     self.points.append((np.transpose(np.array([(x,y) 
                                                           for ar,x,y,sl 
                                                           in images
                                                           if (ar < csl and sl == img)]))))
                     self.frame_names.append("slice_{}".format(img))
                     self.N.append(len(self.points[-1]))

              self.frame_nb = len(self.frame_names)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# VISUALISATION
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

       def areaplot(self,exclude=[],show=True):
              x = range(self.frame_nb)
              y = []
              for cbc in self.cell_by_center:
                     y.append([c 
                               for i,c in enumerate(cbc)
                               if i not in exclude])
              y = np.transpose(np.array(y))
              print y
              try : 
                     plt.stackplot(x,y,colors=["k","w"])
              except Exception:
                     print "Error in creating stacked plot"
              if show:
                     self.show()
 
       def graphs(self):
             
              self.areaplot(show=False)
              f = plt.gcf()
              f.set_dpi(150)
              d = f.get_size_inches()
              f.set_size_inches( (d[0],d[0]) )
              plt.savefig("all.png",bbox_inches="tight")
              self.areaplot(exclude=self.edges_center,show=False)
              plt.savefig("edges_excluded.png",bbox_inches="tight")
             
              for name,pts,attribution,cbc in jhzip(self.frame_names,self.points,self.attributions,self.cell_by_center):
                     voronoi_scatter(self.centers,pts,
                                     self.center_size,
                                     attribution,
                                     show=False)
                     plt.savefig("{}_00scatter.png".format(name),bbox_inches="tight")
                     plt.clf()

                     voronoi_hist(cbc,
                                  show=False,
                                  title="Number of cells")

                     plt.savefig("{}_01bar.png".format(name),bbox_inches="tight")
                     plt.clf()

                     groupsize_corr(self.center_size,cbc,show=False)

                     plt.savefig("{}_02corr.png".format(name),bbox_inches="tight")
                     plt.clf()


       def domains(self):
              x = range(0,self.X,100)*100
              
              def ylist(maximum):
                     y = 0
                     while y < maximum:
                            for n in range(100):
                                   yield y
                            y = y+100
              
              y = [i for i in ylist(self.Y)]

              points = self._topoints(x,y)
              attribution = voronoi_attribution(self.centers,points)
              cz =  [0 if i in self.edges_centers 
                     else x
                     for i,x in enumerate(self.center_size)]
              voronoi_scatter(self.centers,points,cz,attribution,True)

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




