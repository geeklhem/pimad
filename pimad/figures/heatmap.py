""" pip.py - Pairwise invasibility plot functions """

from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle

import multiprocessing as mp
import itertools
import os




def ess(param):
    m = ToyContinuous(param,[])
    m.play(param["g"])
    pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
    return pmutants>param["ip"]
            

def mp_heatmap(param={}):
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

            args = itertools.repeat(param,10)
            pool = mp.Pool()
            out[x,y] = np.median(pool.map(ess,args))
    return out,param



def agent_based_heatmap(model=ToyContinuous,param={}):
    # Set the parameters.
    default = {
        "n":100,
        "ip":0.01,
        "g":10,
        "r":0.2,
        "m":0.205,
        "c":1,
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

            out[x,y] = ess(param)
    return out,param

if __name__ == "__main__":
    import sys

    heatmap,param = mp_heatmap()
    with open("heatmap_{}x{}.pkle".format(*heatmap.shape),"w") as fi:
        pickle.dump((heatmap,param),fi)
    print("saved heatmap_{}x{}.pkle".format(*heatmap.shape))

    try:
        import pimad.export.draw as draw
        import matplotlib.pyplot as plt
        draw.heatmap(heatmap,param,show=False)
        plt.savefig("EESfixedz.eps")
        plt.show()
    except Exception as e:
        print("draw failed {}".format(e))

