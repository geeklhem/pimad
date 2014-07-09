""" pip.py - Pairwise invasibility plot functions """

from pimad.models.ToyContinuous import ToyContinuous
import numpy as np

def agent_based_pip(model=ToyContinuous,param={},precision=0.01):
    """
    Comute th pairwise invasibility plot by successives runs
    of a model.
    
    Args:
    
    """

    # Set the parameters.
    default = {
        "N":10000,
        "T":100,
        "ip":0.01,
        "b":20,
        "c":1,
        "mu":0,
        "g":10,
    }

    for k,v in default:
        if k not in param:
            param[k] = v

    z_range = np.arange(0,1+precision,precision) 
    
    #--- Display
    i = 0
    imax = float(len(z_range)**2)
    #---

    for hatz in z_range:
        param["pa"] = hatz
        for z in z_range:
            
            #--- Display
            i +=1
            print("{:0.2%}".format(i/imax))
            #--- 
    
