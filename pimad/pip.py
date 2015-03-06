""" pip.py - Pairwise invasibility plot functions """

from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import pimad.invasion as invasion
import numpy as np
import cPickle as pickle
import multiprocessing as mp
import itertools
import os
import scipy.ndimage as nd

def increase_precision(pip):
    # Get the contour 
    pp = nd.filters.uniform_filter(np.array(pip>1,dtype=float),size=2)
    mask_contour = np.logical_and((pp != 0),(pp != 1))

    # Double the precision...
    pip = pip.repeat(2, axis=0).repeat(2, axis=1)
    mask_contour = mask_contour.repeat(2, axis=0).repeat(2, axis=1)
    n = pip.shape[1]

    # Add the diagonal (diagonal)
    mask_diag =  np.abs(np.add.outer(np.arange(n), -np.arange(n))) < 3

    to_compute = np.logical_or(mask_diag,mask_contour)
    return pip,to_compute
    
def mp_pip(model=ToyContinuous,param={},precision=0.1):
    """
    Compute the pairwise invasibility plot by successives runs
    of a model.
    """
    print "pip"
    param["model_name"] = str(model)
    param["computed"] = []
    if not "pip_step" in param:
        param["pip_step"] = precision

    required_param = [("pip_step","PIP precision"),
                      ("invfitness_g","Generation used to compute invasion fitness."),
                      ("lk_R","Number of replicas for likelihood estimation.")]    
    for p in required_param:
        if p[0] not in param:
            raise ValueError("Missing parameter: {0[0]} ({0[1]})".format(p))

    
    s_cache  = invasion.simulated(param["lk_R"],param["n"]*param["T"],
                                 param["invfitness_g"],param["ip"])


    pip = np.zeros((11,11))
    z_range = np.linspace(0,1,pip.shape[0])
    step = z_range[1]
    to_compute = np.zeros((len(z_range),len(z_range))) + 1
    param["computed"].append(to_compute.copy())
    while step > param["pip_step"]:
        n = int(to_compute.sum())
        print("\nPrecision: {}, {} invasion fitness to compute.".format(step,n))
        j = 0 
        for x,y in zip(*np.nonzero(to_compute)):
            param["r"] = z_range[x]
            param["m"] = z_range[y]
            pip[x,y] = invasion.mp_invasion_fitness(model,param,s_cache)

            #print "fitness({},{}) = {}".format(z_range[x], z_range[y], pip[x,y])
            # - Display 
            j+=1
            if j%(int(n/10)) == 0:
                print "{:02.0%}".format(j/n)
            # - end Display
            
        pip,to_compute = increase_precision(pip)
        step /= 2
        z_range = np.linspace(0,1,pip.shape[0]) 
        param["computed"].append(to_compute.copy())

    del param["r"]
    del param["m"]
    
    return pip,param
 
