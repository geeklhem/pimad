""" pip.py - Pairwise invasibility plot functions """

from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import pimad.invasion as invasion
import numpy as np
import cPickle as pickle
import multiprocessing as mp
import itertools
import os

def mp_pip(model=ToyContinuous,param={},precision=0.1):
    """
    Compute the pairwise invasibility plot by successives runs
    of a model.
    """
    param["model_name"] = str(model)
    param["pip_step"] = precision
    
    z_range = np.arange(0,1+param["pip_step"],param["pip_step"]) 
    pip = np.zeros((len(z_range),len(z_range)))

    #--- Display
    i = 0
    imax = float(len(z_range)**2)
    #---

    s_cache  = invasion.simulated(param["lk_R"],param["n"]*param["T"],
                                 param["invfitness_g"],param["ip"])

    for y,hatz in enumerate(z_range):
        param["r"] = hatz
        for x,z in enumerate(z_range):
            
            #--- Display
            i +=1
            if i % int(imax/10)== 0:
                print("{:0.2%}".format(i/imax))
            #--- 
    
            param["m"] = z
            pip[x,y] = invasion.mp_invasion_fitness(model,param,s_cache)
    del param["r"]
    del param["m"]
         
    return pip,param
 
