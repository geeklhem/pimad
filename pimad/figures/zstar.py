""" threshold.py """

from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt


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
        
        if pmutants > param["ip"]:
            zright = param["r"]
        else:
            zleft = param["r"]
    
    return 0.5*(zright+zleft)


def threshold_figure(model=ToyContinuous,param={}):
    # Set the parameters.
    default = {
        "n":100,
        "ip":0.01,
        "c":1,
        "g":10,
        "T":1000,
        "dz":0.01,
        "mu":0
    }

    for k,v in default.items():
        if k not in param:
            param[k] = v

    
    b_range = np.concatenate((np.arange(3,20,3),np.arange(20,105,5)))
    out = []

    #--- Display
    i = 0
    imax = float(len(b_range))
    #---
    test_zone = [[],[],[]]

    for y,b in enumerate(b_range):
        #--- Display
        i +=1
        print("{:0.2%}: b/c = {}, predicted: {}".format(i/imax,b,2/b))
        #--- 
        param["b"] = b
        zstar = threshold_dicho(model,param)
        out.append((zstar,b))

    return out



if __name__ == "__main__":
    import sys


    points = {}
    for T in [10,100,1000,10000]:
        points[T] =  agent_based_zstar(param={"T":T})
    
    fname = "zstar_T{}.pkle".format("-".join([str(x) for x in points.keys()]))
    with open(fname,"w") as fi:
        pickle.dump(points,fi)
    print("saved {}".format(fname))


    try:
        import pimad.export.draw as draw
        draw.empirical_zstar(points)
        plt.savefig(fname.split(".")[0]+".eps")
        plt.show()
    except Exception as e:
        print("draw failed {}".format(e))


