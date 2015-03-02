from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np


import multiprocessing as mp
import itertools
import os

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
    required_param = [("g","Number of generations."),
                      ("T","Generation used to compute invasion fitness."),
                      ("replica","Number of replica")]    
    for p in required_param:
        if p[0] not in param:
            raise ValueError("Missing parameter: {0[0]} ({0[1]})".format(p))

    args = itertools.repeat((model,param.copy()),param["replica"])
    k = POOL.map(invasion_fitness,args)
    fitness, proportion = zip(*k)
    proportion = np.mean(proportion)
    fitness = np.mean(fitness)
    return fitness, proportion 

def threshold_dicho(model,param):
    """Dichotomic computation of the social mutant invasion threshold

    Args: 
        model (pimad.model.Model): Model.
        param (dict): Model parameters.
    Returns:
        (float) z*_approx
    """
    required_param = [("kmax","Number of step for the dichotomic threshold measure.")]
    for p in required_param:
        if p[0] not in param:
            raise ValueError("Missing parameter: {0[0]} ({0[1]})".format(p))

    zright = 1.0
    zleft = 0.0
    for _ in range(param["kmax"]):
        param["r"] = 0.5*(zright+zleft)
        param["m"] = param["r"]+param["dz"]
        ftnss,prop = mp_invasion_fitness(model,param)
        print(("({:2.2}-{:2.2}) Resident: {:2.2}, Mutants: {:2.2}. "
               "{:2.2%} of invasion.  Fitness: {:2.3}").format(zleft, zright, param["r"],
                                                               param["m"], prop, ftnss))
        if ftnss>0:
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
            
            args = itertools.repeat((model,param.copy()),param["replica"])
            zstar = [threshold_dicho(*a) for a in args]
            zstar = np.mean(zstar)
            data[T].append((zstar,b))

    del param["T"]
    del param["b"]
    del param["r"]
    del param["m"]
    return data, param

## POOL 
POOL = mp.Pool()
