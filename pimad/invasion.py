from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np


import multiprocessing as mp
import itertools
import os
POOL = mp.Pool()



def mp_invasion_fitness(model,param):
    """Run the simulation for param["g"] generation (default = 100) and
    compute the exponential growth rate in the param["invfitness_g"]
    (default = 10) generations for the ones that are not extinct.
    
    Returns a tuple (invasion fitness, proportion of extinct simulations).
    If all are extinct return (0,1). 

    Args:
        model (pimad.Model): The model to run.
        param (dict): model parameters.
    """
    default = {
        "g": 100,
        "invfitness_g":10}
    for k,v in default:
        if k not in param:
            param[k] = v
    args = itertools.repeat((model,param.copy()),param["replica"])
    k = POOL.map(invasion_fitness,args)
    fitness, proportion = zip(*k)
    proportion = np.mean(proportion)
    fitness = np.mean(fitness)
        
    return fitness, proportion 

def invasion_fitness(args):
    model = args[0]
    param = args[1]

    np.random.seed()
    m = model(param,[])

    m.play(param["invfitness_g"])
    pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
    m.play(param["g"]-param["invfitness_g"])

    invaded = bool(np.sum(m.population.phenotype))

    if invaded:
        fitness = np.log10(pmutants/param["ip"])
    else:
        fitness = 0 
    
    return fitness, invaded 


def heatmap(model=ToyContinuous,param={}):
    # Set the parameters
    T_range = param["T_range"] 
    b_range = param["b_range"]

    out = np.zeros((len(T_range),len(b_range)))


    #--- Display
    i = 0
    imax = float(len(T_range)*len(b_range))
    #---

    for x,T in enumerate(T_range):
        param["T"] = T
        for y,b in enumerate(b_range):
            
            #--- Display
            i += 1
            print("{:0.2%} T:{},b:{}".format(i/imax,T,b))
            #--- 
    
            param["b"] = b
            out[x,y] = mp_invasion_fitness(model,param)[1]

    del param["T"]
    del param["b"]
    return out,param


def threshold_dicho(model,param,kmax=10):
    """Dichotomic computation of the social mutant invasion threshold

    Args: 
        model (pimad.model.Model): Model.
        param (dict): Model parameters.
        kmax (int): number of steps.
    Returns:
        (float) z*_approx
    """

    zright = 1.0
    zleft = 0.0
    for k in np.linspace(1,kmax,kmax):
        param["r"] = 0.5*(zright+zleft)
        param["m"] = param["r"]+param["dz"]
        invade = mp_invasion_fitness(model,param)[1]
        if invade:
            zright = param["r"]
        else:
            zleft = param["r"]
    return 0.5*(zright+zleft)


def threshold(model=ToyContinuous,param={}):
    data = {}

    ## Display
    imax = len(param["T_range"])*len(param["b_range"])
    i = 0
    ##

    for T in param["T_range"]:
        data[T] = []
        param["T"] = T 
        for b in param["b_range"]:
            param["b"] = b

            ## Display
            i += 1
            print("{:0.2%} | T: {}, b: {}".format(i/imax,T,b))
            ##

            zstar = threshold_dicho(model,param,param["kmax"])
            data[T].append((zstar,b))

    del param["T"]
    del param["b"]
    del param["r"]
    del param["m"]
    return data, param
