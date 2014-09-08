from __future__ import division
import os 

import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
import sys 

from pimad import pip 
from pimad import invasion
import pimad.export.draw as draw 
from pimad.models.toycontinuous import ToyContinuous

PRECISION_PIP = 0.01 #0.01
PRECISION_HEATMAP = 0.1
PRECISION_THRESHOLD = 0.1
STEP_THRESHOLD_DICHO = 10
MODEL = ToyContinuous
T_RANGE_THRES = [100,200,500,1000,3000]
T_RANGE = [50,100,200,500,1000,3000,5000]
B_RANGE = [2 ,5 ,10 ,20 ,40 ,80,  100]
B_RANGE_THRES = [2,4,8,10,20,40,]
param =  {"n": 500, # Number of patches
          "T": 100,  # Patch size
          "ip":0.01,   # Initial proportions of mutants
          "m":0.5,  # Mutant trait value
          "r":0.5,  # Resident trait value
          "mu":0,   # Mutation rate
          "b":20,   # Benefits coefficient
          "c":1,    # Cost coefficient
          "g":10,   # Number of generations
          "dz":0.01, 
          "replica": 5 #4 
}

def get_definition(model,param,pre="%",su=""):
    s = "\n".join(["{} {}={} {}".format(pre,k,v,su)for k,v in param.items()])
    return s 


if __name__ == "__main__":
    DO = "ALL"
    if len(sys.argv) == 2:
        DO = sys.argv[1]
    print("DO: {}".format(DO))
    

    ## Figure 2: Numerical PIP ##
    if DO == "pip" or DO == "ALL":
        print "{:-^80}".format(" PIP ")
        
        pip_file = "pip_T{}_n{}_step{}_repl_{}_b{}_ip{}".format(param["T"],param["n"],PRECISION_PIP,param["replica"],param["b"],param["ip"])
        print pip_file
        if not os.path.exists(pip_file+".pkle"):
            pip_data,pip_param = pip.mp_pip(MODEL,param.copy(),PRECISION_PIP)
            with open(pip_file+".pkle","w") as fi:
                pickle.dump((pip_data,pip_param),fi)
                print "saved {}.pkle".format(pip_file)
        else:
            with open(pip_file+".pkle","r") as fi:
                pip_data,pip_param = pickle.load(fi) 

        if not os.path.exists(pip_file+".eps"):
            draw.pip(pip_data,False)
            plt.savefig(pip_file+".eps")
            with open(pip_file+".eps","a") as fi:
                fi.write(get_definition(MODEL,pip_param))
            print "saved {}.eps".format(pip_file)

    ## Figure 3: INVASION Heatmap ##
    if DO == "heatmap" or DO == "ALL":
        print "{:-^80}".format(" HEATMAP ")
        heatmap_file = "heatmap_{}".format(PRECISION_HEATMAP,REPLICAS_HEATMAP)

        param["r"] = 0.2 
        param["m"] = 0.21
        param["T_range"] = T_RANGE
        param["b_range"] = B_RANGE

        if not os.path.exists(heatmap_file+".pkle"):
            data,out_param = invasion.heatmap(MODEL,param.copy())
            with open(heatmap_file+".pkle","w") as fi:
                pickle.dump((data,out_param),fi)
        else:
            with open(heatmap_file+".pkle","r") as fi:
                data,out_param = pickle.load(fi) 

        if not os.path.exists(heatmap_file+".eps"):
            draw.heatmap(data,out_param,False)
            plt.savefig(heatmap_file+".eps")
            with open(heatmap_file+".eps","a") as fi:
                fi.write(get_definition(MODEL,out_param))



    ## Figure 4: Sociality threshold ##
    if DO == "threshold" or DO == "ALL":
        print "{:-^80}".format(" SCORE THRESHOLD ")
        threshold_file = "threshold_{}".format(PRECISION_THRESHOLD,)
        if not os.path.exists(threshold_file+".pkle"):
            param["T_range"] = T_RANGE_THRES
            param["b_range"] = B_RANGE_THRES
            param["kmax"] = STEP_THRESHOLD_DICHO

            data,out_param = invasion.threshold(MODEL,param.copy())
            with open(threshold_file+".pkle","w") as fi:
                pickle.dump((data,out_param),fi)
        else:
            with open(threshold_file+".pkle","r") as fi:
                data,out_param = pickle.load(fi) 


        if not os.path.exists(threshold_file+".eps"):
            draw.threshold(data)
            plt.savefig(threshold_file+".eps")
            with open(threshold_file+".eps","a") as fi:
                fi.write(get_definition(MODEL,out_param))


## Figure 5: Altruism threshold ##
## Figure 6: Numerical PIP with size-threshold ##

