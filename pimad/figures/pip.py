""" pip.py - Pairwise invasibility plot functions """

from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import numpy as np
import cPickle as pickle
import multiprocessing as mp
import itertools
import os

def mp_pip(repl=4,model=ToyContinuous,param={},precision=0.1):
    args = itertools.repeat((model,param,precision),repl)
    pool = mp.Pool()
    out = pool.map(agent_star,args)
    pips = [x[0] for x in out]
    param = out[0][1]
    param["replica"] = repl
    output = np.sum(pips,axis=0)/len(pips)
    return output,param

def agent_star(args):
    print "PID =", os.getpid(),
    return agent_based_pip(*args)
            
def agent_based_pip(model=ToyContinuous,param={},precision=0.1):
    """
    Comute th pairwise invasibility plot by successives runs
    of a model.
    
    Args:
    
    """
    print "go"
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
            #print("{:0.2%}".format(i/imax))
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
    r = ''
    if len(sys.argv) == 3:
        repl = int(sys.argv[2])
        r = '_{}repl'.format(repl)
        pip,param = mp_pip(repl=repl,precision=float(sys.argv[1]))

    elif len(sys.argv) == 2:
        pip,param = agent_based_pip(precision=float(sys.argv[1]))
    else:    
        pip,param = agent_based_pip()

    fname = "pip_{0[1]}x{0[1]}{1}.pkle".format(pip.shape,r)
    with open(fname,"w") as fi:
        pickle.dump((pip,param),fi)
    print(fname.format(*pip.shape))

    try:
        import pimad.export.draw as draw
        draw.pip(pip)
    except Exception as e:
        print("draw failed {}".format(e))
