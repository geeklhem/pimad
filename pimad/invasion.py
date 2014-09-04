from pimad.models.toycontinuous import ToyContinuous
import numpy as np


import multiprocessing as mp
import itertools
import os

def invasion_test(args):
    model = args[0]
    param = args[1]

    np.random.seed()
    m = model(param,[])
    
    m.play(param["g"])

    pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))

    return pmutants>param["ip"]

def mp_invasion(model,param):
    args = itertools.repeat((model,param),param["replica"])
    pool = mp.Pool()
    k = pool.map(invasion_test,args)
    return np.median(k)
    
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
            i +=1
            print("{:0.2%} - T:{},b:{}".format(i/imax,T,b))
            #--- 
    
            param["b"] = b
            out[x,y] = mp_invasion(model,param)

    del param["T"]
    del param["b"]
    return out,param


def threshold_dicho(model,param,kmax=10):
    """ Dichotomic computation of the invasion threshold

    Args: 
        model (pimad.model.Model): Model.
        param (dict): Model parameters.
        kmax (int): number of steps.
    """

    zright = 1.0
    zleft = 0.0
    for k in np.linspace(1,kmax,kmax):
        print("{} {:0.2}<z*<{:0.2}".format(k,zright,zleft))
        param["r"] = 0.5*(zright+zleft)
        param["m"] = param["r"]+param["dz"]

        if mp_invasion(model,param):
            zright = param["r"]
        else:
            zleft = param["r"]
    
    return 0.5*(zright+zleft)


def threshold(model,param):
    data = {}

    for T in param["T_range"]:
        data[T] = []
        param["T"] = T 
        for b in param["b_range"]:
            param["b"] = b
            zstar = threshold_dicho(model,param,param["kmax"])
            data[T].append((zstar,b))

    del param["T"]
    del param["b"]
    del param["r"]
    del param["m"]
    return data, param
