from pimad.models.toycontinuous import ToyContinuous
import numpy as np


import multiprocessing as mp
import itertools
import os

def invasion(args):
    model = args[0]
    param = args[1]

    np.random.seed()

    m = model(param)
    m.play(param["g"])
    pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))

    return pmutants>param["ip"]

def mp_invasion(model,param):
    args = itertools.repeat((model,param),param["replica"])
    pool = mp.Pool()
    return np.median(pool.map(invasion_star,args))
    

def heatmap(model=ToyContinuous,param={}):
    # Set the parameters.
    default = {
        "n":100,
        "ip":0.01,
        "g":10,
        "r":0.2,
        "m":0.205,
        "c":1,
        "replica":10
    }

    for k,v in default.items():
        if k not in param:
            param[k] = v

    #po = np.arange(1,3.05,0.25)
    #T_range = [int(x) for x in np.power([10]*len(po),po)]
    T_range = [10,50,100,200,500,1000,3000]
    b_range = [2 ,5 ,10 ,25 ,50 ,75,  100]
    #b_range = np.arange(2,107,5) 
    out = np.zeros((len(T_range),len(b_range)))

    param["T_range"] = T_range 
    param["b_range"] = b_range

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
    return out,param


def threshold_dicho(model,param,kmax=10):
    """ Dichotomic computation of the invasion threshold

    Args: 
        model (pimad.model.Model): Model.
        param (dict): Model parameters.
        kmax (int): number of steps.
    """
  
    zright = 1
    zleft = 0
    for k in np.linspace(1,kmax,kmax):

        param["r"] = 0.5*(zright+zleft)
        param["m"] = param["r"]+param["dz"]

        m = model(param,[])

        pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))      
        m.play(param["g"])
        pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
        
        if mp_invasion(model,param):
            zright = param["r"]
        else:
            zleft = param["r"]
    
    return 0.5*(zright+zleft)
