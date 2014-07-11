""" pip.py - Pairwise invasibility plot functions """

from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle

def agent_based_heatmap(model=ToyContinuous,param={}):
    # Set the parameters.
    default = {
        "n":100,
        "ip":0.1,
        "g":50,
        "r":0.2,
        "m":0.21,
        "c":1,
    }

    for k,v in default.items():
        if k not in param:
            param[k] = v

    po = np.arange(0,3.05,0.05)
    T_range = [int(x) for x in np.power([10]*len(po),po)]

    b_range = np.arange(2,107,5) 
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

            m = ToyContinuous(param,[])
            m.play(param["g"])
            pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
            if pmutants>param["ip"]:
                ess = 1
            else:
                ess = 0
            out[x,y] = ess
    return out,param

if __name__ == "__main__":
    import sys

    heatmap,param = agent_based_heatmap()
    with open("heatmap_{}x{}.pkle".format(*heatmap.shape),"w") as fi:
        pickle.dump((heatmap,param),fi)
    print("saved heatmap_{}x{}.pkle".format(*heatmap.shape))

    try:
        import pimad.export.draw as draw
        draw.heatmap(heatmap)
    except Exception as e:
        print("draw failed {}".format(e))

