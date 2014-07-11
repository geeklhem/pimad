""" pip.py - Pairwise invasibility plot functions """

from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

def agent_based_zstar(model=ToyContinuous,param={}):
    # Set the parameters.
    default = {
        "n":100,
        "ip":0.01,
        "c":1,
        "g":100,
        "T":100,
    }

    for k,v in default.items():
        if k not in param:
            param[k] = v

    
    b_range = np.arange(2,105,20) 
    out = []

    #--- Display
    i = 0
    imax = float(len(b_range))
    #---

    for y,b in enumerate(b_range):
        #--- Display
        i +=1
        print("{:0.2%}: b/c = {}".format(i/imax,b))
        #--- 
    
        param["b"] = b
        
        z_range = np.arange(max(0.025,(2.0/b)-0.2), min(1,(2.0/b)+0.2),0.025)
        ess = 0
        j = 0
        while ess != 1 and j<len(z_range):
            print("Testing z={}".format(z_range[j]))
            param["r"] = z_range[j]
            param["m"] = z_range[j]+0.01

            m = ToyContinuous(param,[])
            m.play(param["g"])

            pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
            if pmutants>param["ip"]:
                ess = 1
                out.append((z_range[j],b))
                print "ess !"
            j += 1
    return out



if __name__ == "__main__":
    import sys

    points = agent_based_zstar()


    try:
        import pimad.export.draw as draw
        draw.empirical_zstar(points)
    except Exception as e:
        print("draw failed {}".format(e))


    #heatmap,param = agent_based_heatmap()
    #with open("heatmap_{}x{}.pkle".format(*heatmap.shape),"w") as fi:
    #    pickle.dump((heatmap,param),fi)
    #print("saved heatmap_{}x{}.pkle".format(*pip.shape))
