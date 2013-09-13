from __future__ import division 

import toymodel as toymodels
import numpy as np
import math

def model_pip(p = 100,ip = 0.01,g=10,N=100000):
    """Compute the pairwise invasibility plot by succesives runs
    of the continuous model 
    :param p: Precision
    :type p: int
    :param ip: Initial proportion of mutants
    :type ip: float"""
    z_range = [i/p for i in range(p+1)]
    s = np.zeros((p+1,p+1))

    param = {"N":N,
             "T":100,
             "ip":ip,
             "b":20,
             "c":1,
             "mu":0}

    i = 0
    imax = (p+1)*(p+1)
    for hatz in z_range:
        param["pa"] = hatz
        for z in z_range:
            i = i+1
            print("{}/{}".format(i,imax))
            param["ps"] = z
            m = toymodels.ToyContinuous(param,[])
            m.play(g,verbose=False)
            pmutants = sum(m.population.phenotype)/m.param["N"]
            if pmutants:
                fitness = math.log(pmutants/ip,10)
            else:
                fitness = -1
            s[int(z*p),int(hatz*p)] = fitness
    return s

def main(f,p=50,ip=0.1,g=10):
    s = model_pip(p,ip,g)
    np.savetxt(f,s)
    return s  
