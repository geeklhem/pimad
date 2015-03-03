from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np


import multiprocessing as mp
import itertools
import os

def lk_estimate(observed,svalues,simul):
    """ Give the likelihood estimate of the invasion fitness 
    
    Args:
        observed (np.array): number of mutants observed in different trajectories.
        svalues (np.array): values of the invasion fitness used in distrib.
        simul (np.array): results of simulations.
        
    Returns:
        (float): maximum likelihood estimate of the invasion fitness
    """

    lk = np.zeros(len(svalues))
    for i,s in enumerate(svalues):
        Pmax = 0

        for o in observed:
            p = np.sum(simul[i,:]==o)

            if p > Pmax:
                Pmax = p
            if Pmax:
                lk[i] += np.log(Pmax)
            else:
                lk[i] = -np.inf
                break

    s_estimate = svalues[np.argmax(lk)]

    return s_estimate


def simulated(R,N,g,ip,step=200):
    """Return simulated number of mutants"""
    generation = lambda M,s,N: np.random.binomial(N,((M/N)*s)/(1+(M/N)*(s-1)))
    out = np.zeros((step,R))
    svalues = np.linspace(0,2,num=step)
    for i,s in enumerate(svalues):
        for r in range(R):
            M = int(ip*N)
            for _ in range(10):
                p = generation(M,s,N)
            out[i,r] = p
    return out,svalues


def invasion_fitness(args):
    model = args[0]
    param = args[1]
    np.random.seed()
    m = model(param,[])
    m.play(param["invfitness_g"])
    mutants = np.sum(m.population.phenotype)
    return mutants 



def mp_invasion_fitness(model,param,s_cache=None):
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
    observed = POOL.map(invasion_fitness,args)

    if s_cache is None:
        simul, svalues = simulated(param["lk_R"],param["n"]*param["T"],
                                   param["invfitness_g"],param["ip"])
    else:
        simul, svalues = s_cache

    fitness = lk_estimate(observed,svalues,simul)
    
    return fitness

def threshold_dicho(model,param,s_cache=None):
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
        ftnss = mp_invasion_fitness(model,param,s_cache)
        print(("({:2.2}-{:2.2}) Resident: {:2.2}, Mutants: {:2.2}. "
               "  Fitness: {:2.3}").format(zleft, zright, param["r"],
                                           param["m"],  ftnss))
        if ftnss>=1:
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
        print("Computing likelihood cache (T={})...").format(T) 
        s_cache = simulated(param["lk_R"],param["n"]*param["T"],
                            param["invfitness_g"],param["ip"])

        for b in param["b_range"]:
            param["b"] = b

            ## Display
            i += 1
            print("{:0.2%} | T: {}, b: {}".format(i/imax,T,b))
            ##
            
            args = itertools.repeat((model,param.copy(),s_cache),param["thres_r"])
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
