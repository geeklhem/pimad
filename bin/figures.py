from __future__ import division
import os 

import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle

from pimad import pip 
from pimad import invasion
import pimad.export.draw as draw 
from pimad.models.toycontinuous import ToyContinuous

PRECISION_PIP = 0.01
REPLICAS_PIP = 4
PRECISION_HEATMAP = 0.1
REPLICAS_HEATMAP = 4
PRECISION_THRESHOLD = 0.1
REPLICAS_THRESHOLD = 4
STEP_THRESHOLD_DICHO = 3
MODEL = ToyContinuous

T_RANGE = [50,100,200,500,1000,3000,5000]
B_RANGE = [2 ,5 ,10 ,20 ,40 ,80,  100]
param =  {"n":100,  # Number of patches
          "T":5000, # Patch size
          "ip":0.01,   # Initial proportions of mutants
          "m":0.5,  # Mutant trait value
          "r":0.5,  # Resident trait value
          "mu":0,   # Mutation rate
          "b":20,   # Benefits coefficient
          "c":1,    # Cost coefficient
          "g":10,   # Number of generations
          "dz":0.01, #used in threshold
          "replica": 4 #used in threshold
}


if __name__ == "__main__":
## Figure 1: Group Size distribution ##
## Figure 2: Numerical PIP ##
    print "{:-^80}".format(" PIP ")
    pip_file = "pip_{}".format(PRECISION_PIP,REPLICAS_PIP)
    if not os.path.exists(pip_file+".pkle"):
        pip_data,pip_param = pip.mp_pip(MODEL,param,PRECISION_PIP)
        with open(pip_file+".pkle","w") as fi:
            pickle.dump((pip_data,pip_param),fi)
    else:
        with open(pip_file+".pkle","r") as fi:
            pip_data,pip_param = pickle.load(fi) 

    if not os.path.exists(pip_file+".eps"):
        draw.pip(pip_data,False)
        plt.savefig(pip_file+".eps")


## Figure 3: INVASION Heatmap ##
    print "{:-^80}".format(" HEATMAP ")
    heatmap_file = "heatmap_{}".format(PRECISION_HEATMAP,REPLICAS_HEATMAP)

    param["r"] = 0.2 
    param["m"] = 0.21
    param["T_range"] = T_RANGE
    param["b_range"] = B_RANGE

    if not os.path.exists(heatmap_file+".pkle"):
        data,out_param = invasion.heatmap(MODEL,param=param)
        with open(heatmap_file+".pkle","w") as fi:
            pickle.dump((data,out_param),fi)
    else:
        with open(heatmap_file+".pkle","r") as fi:
            data,out_param = pickle.load(fi) 

    if not os.path.exists(heatmap_file+".eps"):
        draw.heatmap(data,out_param,False)
        plt.savefig(heatmap_file+".eps")


## Figure 4: Sociality threshold ##
    print "{:-^80}".format(" SCORE THRESHOLD ")
    threshold_file = "threshold_{}".format(PRECISION_THRESHOLD,)
    if not os.path.exists(threshold_file+".pkle"):
        b_range = np.concatenate((np.arange(3,20,3),np.arange(20,105,5)))
        data = {}
        
        for T in T_RANGE:
            data[T] = []
            param["T"] = T 
            for b in b_range:
                param["b"] = b
                zstar = invasion.threshold_dicho(MODEL,param,STEP_THRESHOLD_DICHO)
                data[T].append((zstar,b)) 

        with open(threshold_file+".pkle","w") as fi:
            pickle.dump((data,out_param),fi)
    else:
        with open(threshold_file+".pkle","r") as fi:
            data,out_param = pickle.load(fi) 


    if not os.path.exists(threshold_file+".eps"):
        draw.threshold(data)
        plt.savefig(threshold_file+".eps")

## Figure 5: Altruism threshold ##
## Figure 6: Numerical PIP with size-threshold ##
