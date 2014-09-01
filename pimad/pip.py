""" pip.py - Pairwise invasibility plot functions """

from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle
import multiprocessing as mp
import itertools
import os

def mp_pip(model=ToyContinuous,param={},precision=0.1):
    param["model_name"] = str(model)
    param["pip_step"] = precision

    args = itertools.repeat((model,param),param["replica"])

    pool = mp.Pool()
    pips = pool.map(pip,args)

    #Average over the different replicas 
    output = np.sum(pips,axis=0)/len(pips)

    return output,param
 
def pip(args):
    """
    Compute the pairwise invasibility plot by successives runs
    of a model.
    """
    model = args[0]
    param = args[1]
    

    z_range = np.arange(0,1+param["pip_step"],param["pip_step"]) 
    pip = np.zeros((len(z_range),len(z_range)))

    #--- Display
    i = 0
    imax = float(len(z_range)**2)
    #---

    for y,hatz in enumerate(z_range):
        param["r"] = hatz
        for x,z in enumerate(z_range):
            
            #--- Display
            i +=1
            if i % int(imax/10)== 0:
                print("{:0.2%}".format(i/imax))
            #--- 
    
            param["m"] = z

            m = model(param,[])
            m.play(param["g"])
            pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
            if pmutants:
                fitness = np.log10(pmutants/param["ip"])
            else:
                fitness = -1
            pip[x,y] = fitness
         
    return pip
 
