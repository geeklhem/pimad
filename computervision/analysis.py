#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Data Analysis"""

import collections
import numpy as np
import scipy as sp


def cell_by_section(attribution,nb_sections):
    cc = collections.Counter(attribution)
    cell_by_center = [0] * nb_sections
    for k,v in cc.iteritems():
        cell_by_center[k] = v
    return cell_by_center


def group_size_distrib(cellBySection,lonersBySection,nb_sections):
    g = [0] * max(cellBySection)
    g[1] = sum(lonersBySection)

    for c in cellBySection:
        g[c] += c
    gs = [i./n if n
          else 0
          for n,i in enumerate(g)]

    return {"group_size_distrib":gs,
            "crowding":g,
            "mean_gs":np.mean(gs),
            'mean_crowding':np.mean(g)}


def lin_correlate(x,y):

    (a,b)=sp.polyfit(xy,1)
    xr=sp.polyval([a,b],t)
    #compute the mean square error
    err=np.sqrt(sum((xr-xn)**2)/n)

    return {"a":a,"b":b,"regline":xr,"rho":err}
