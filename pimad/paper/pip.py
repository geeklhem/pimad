""" pip.py - Pairwise invasibility plot functions """

from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle

def agent_based_pip(model=ToyContinuous,param={},precision=0.1):
    """
    Comute th pairwise invasibility plot by successives runs
    of a model.
    
    Args:
    
    """

    # Set the parameters.
    default = {
        "n":100,
        "T":100,
        "ip":0.1,
        "b":20,
        "c":1,
        "g":10,
    } 

    for k,v in default.items():
        if k not in param:
            param[k] = v
        
    z_range = np.arange(0,1+precision,precision) 
    pip = np.zeros((len(z_range),len(z_range)))

    #--- Display
    i = 0
    imax = float(len(z_range)**2)
    #---

    for y,hatz in enumerate(z_range):
        param["r"] = hatz
        for x,z in enumerate(z_range):
            
            #--- Display
            i +=1
            print("{:0.2%}".format(i/imax))
            #--- 
    
            param["m"] = z

            m = ToyContinuous(param,[])
            m.play(param["g"])
            pmutants = np.sum(m.population.phenotype)/float(len(m.population.phenotype.flat))
            if pmutants:
                fitness = np.log10(pmutants/param["ip"])
            else:
                fitness = -1
            pip[x,y] = fitness
         
    return pip,param

if __name__ == "__main__":
    import sys


    if len(sys.argv) > 1:
        pip,param = agent_based_pip(precision=float(sys.argv[1]))
    else:    
        pip,param = agent_based_pip()
    with open("pip_{}x{}.pkle".format(*pip.shape),"w") as fi:
        pickle.dump((pip,param),fi)
    print("saved pip_{}x{}.pkle".format(*pip.shape))

    try:
        import pimad.export.draw as draw
        draw.pip(pip)
    except Exception as e:
        print("draw failed {}".format(e))
