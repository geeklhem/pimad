#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Visualisation functions"""

import itertools

def get_color():
       return itertools.cycle(['r', 'g', 'b', 'c', 'm', 'y', 'k'])

def plot_particle(attribution,groups=None,x,y,show=True):
    #Colors
    color_iter = get_color()
    if groups:
        colors = [next(color_iter) for c in range(groups["N"])]
    else:
        colors = [next(color_iter) for c in range(max(attribution))]
    colorlist = [colors[i] for i in attribution]

    # Points
    plt.scatter(points[0,:],points[1,:],color=colorlist)

    if groups:
        # Groups
        ax = plt.gca()
        for x,y,c,s in zip(center[0,:],center[1,:],colors,center_size):
            ax.add_artist(Circle(xy=(x,y),
                                 radius=math.sqrt(s/math.pi),
                                 facecolor=c,
                                 alpha=0.3))
    # Axis details
    plt.xlim(x)
    plt.ylim(y)

    if show:
        plt.show()

def correlation(x,y,regline,xlab,ylab,show=True):
    plt.plot(x,regline)
    plt.scatter(x,y)
    ax = plt.gca()
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    if show:
        plt.show()

