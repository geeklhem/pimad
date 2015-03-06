from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import scipy.stats 

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

    lk = [likelihood(observed,sim) for sim in simul]
    s_estimate = svalues[np.argmax(lk)]
    return s_estimate

def likelihood(observed,sim):
    """Return the likelihood of the parameters wich gave the distribution
    sim given the data.

    Args:
        observed (np.array): number of mutants observed in different observed
            trajectories.
        simul (np.array):  number of mutants observed in different simulated 
            trajectories.

    Returns:
        (float) likelihood. 
    """
    if np.std(sim):
        pdf = scipy.stats.distributions.norm(np.mean(sim),np.std(sim)).pdf
    else:
        pdf = lambda x: x == np.mean(sim)
        
    return np.sum(np.log(pdf(observed)))
                  
    # L = 0

    # for o in observed:
    #     p = np.sum(sim==o)/len(sim)
    #     if p:
    #         L += np.log(p)
    #     else:
    #         L += -np.inf
    #         break
    # return L 


def simulated(R,N,g,ip,step=200):
    """Return simulated number of mutants"""
    print("Computing likelihood cache for generation {}. (N:{:1.2e}, R:{}, ip:{}, step:{})...").format(g,N,R,ip,step) 
    generation = lambda M,s,N: np.random.binomial(N, (M*s)/(N+M*(s-1)) )
    out = np.zeros((step,R))
    svalues = np.linspace(0,2,num=step)
    for i,s in enumerate(svalues):
        for r in range(R):
            M = int(ip*N)
            for _ in range(10):
                M = generation(M,s,N)
            out[i,r] = M 
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
    param["kmax"] = int(np.log(1/param["dz"])/np.log(2))+1
    print "kmax set to {}".format(param["kmax"])
    for p in required_param:
        if p[0] not in param:
            raise ValueError("Missing parameter: {0[0]} ({0[1]})".format(p))

    zright = 1.0
    zleft = 0.0
    for _ in range(param["kmax"]):
        param["r"] = 0.5*(zright+zleft)
        param["m"] = param["r"]+param["dz"]
        ftnss = mp_invasion_fitness(model,param,s_cache)
        print(("({:02.3f}-{:02.3f}) Resident: {:2.3f}, Mutants: {:2.2f}. "
               "  Fitness: {: 2.5f}").format(zleft, zright, param["r"],
                                           param["m"],  ftnss))
        if ftnss>1:
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

        s_cache = simulated(param["lk_R"],param["n"]*param["T"],
                            param["invfitness_g"],param["ip"])

        for b in param["b_range"]:
            param["b"] = b
            
            args = itertools.repeat((model,param.copy(),s_cache),param["thres_r"])
            zstar = [threshold_dicho(*a) for a in args]
            zstar = np.mean(zstar)

            ## Display
            i += 1
            print("{:0.2%} | T: {}, b: {} - Threshold {} (analytical: {})".format(i/imax,T,b,zstar,2*param["c"]/(param["b"])))
            ##


            data[T].append((zstar,b))

    del param["T"]
    del param["b"]
    del param["r"]
    del param["m"]
    return data, param

## POOL 
POOL = mp.Pool()
