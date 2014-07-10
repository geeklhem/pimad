""" pip.py - Pairwise invasibility plot functions """

from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

def agent_based_zstar(model=ToyContinuous,param={}):
    # Set the parameters.
    default = {
        "N":1000,
        "ip":0.01,
        "c":1,
        "mu":0,
        "g":100,
        "T":100
    }

    for k,v in default.items():
        if k not in param:
            param[k] = v

    
    b_range = np.arange(1,105,20) 
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
        
        z_range = np.arange(min(0.01,(2.0/b)-0.1),max(1,(2.0/b)-0.1),0.01)
        ess = 0
        j = 0
        while ess != 1 and j<len(z_range):
            print("Testing z={}".format(z_range[j]))
            param["pa"] = z_range[j]
            param["ps"] = z_range[j]+0.01

            m = ToyContinuous(param,[])
            m.play(param["g"])

            pmutants = np.sum(m.population.phenotype)/float(m.param["ip"])

            if pmutants>param["ip"]:
                ess = 1
                out.append((z_range[j],b))

            j += 1
    return out


def draw(points):

    z = np.arange(0.001,1.001,0.001)

    theo = 2.0/z
    plt.plot(z,theo, color="k",label="Analytical prediction")

    x,y = zip(*points)
    plt.scatter(x,y,label="Experimental threshold",color="red")
    plt.legend()
    plt.xlabel("z")
    plt.ylabel("b/c")
    plt.xlim((0,1))
    plt.ylim((0,100))
    plt.show()
    

if __name__ == "__main__":
    import sys

    points = agent_based_zstar()
    draw(points)

    #heatmap,param = agent_based_heatmap()
    #with open("heatmap_{}x{}.pkle".format(*heatmap.shape),"w") as fi:
    #    pickle.dump((heatmap,param),fi)
    #print("saved heatmap_{}x{}.pkle".format(*pip.shape))
