""" pip.py - Pairwise invasibility plot functions """

from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

def agent_based_zstar(model=ToyContinuous,param={}):
    # Set the parameters.
    default = {
        "n":1000,
        "ip":0.01,
        "c":1,
        "g":5,
        "T":100,
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
        
        z_range = np.arange(max(0.01,(2.0/b)-0.2), min(1-0.01,(2.0/b)+0.2),0.05)
        ess = 0
        j = 0
        test_zone[1].append(z_range[0])
        test_zone[2].append(z_range[1])
        test_zone[0].append(b)
        while ess != 1 and j<len(z_range):
            param["r"] = z_range[j]
            param["m"] = z_range[j]+0.01

            m = ToyContinuous(param,[])

            pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
            #print("init {}/{}".format(pmutants,param["ip"]))
            
            m.play(param["g"])

            pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
            print("Testing z={}. {}/{}".format(z_range[j],pmutants,param["ip"]))
            if pmutants>param["ip"]:
                ess = 1
                out.append((z_range[j],b))
                print "point !"
            j += 1
    return out, test_zone



if __name__ == "__main__":
    import sys

    points,test_zone = agent_based_zstar()
    
    with open("zstar_{}.pkle".format(len(points)),"w") as fi:
        pickle.dump(points,fi)
    print("saved zstar_{}.pkle".format(len(points)))

    

    try:
        import pimad.export.draw as draw
        draw.empirical_zstar(points,test_zone)
    except Exception as e:
        print("draw failed {}".format(e))


