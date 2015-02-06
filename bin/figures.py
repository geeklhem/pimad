from __future__ import division
import os 

import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
import sys 
import platform
import time

from pimad import pip 
from pimad import invasion
import pimad.export.draw as draw 
from pimad.models.toycontinuous import ToyContinuous, ToyContinuousNLC, ToyContinuousGST, ToyContinuousSigB
MODEL = ToyContinuous
MODEL_CODE = "TOY"
            
param =  {"n": 500, # Number of patches
          "T": 100,  # Patch size
          "ip":0.01,   # Initial proportions of mutants
          "r":0.5,  # Resident trait value
          "mu":0,   # Mutation rate
          "b":20,   # Benefits coefficient
          "c":1,    # Cost coefficient
          "g":100,   # Number of generations
          "dz":0.01, 
          "replica": 5, #4
          "time": time.asctime(),
          "host": "|".join(platform.uname()),
          "precision":0.01,
          "invfitness_g":10,
          
          # Specific to threshold 
          "T_range": [20,100], #[100,200,500,1000,3000],
          "b_range": [2, 5, 10, 15 , 20, 25, 30, 35, 40],
          "kmax":10,

          #Specific to trajectories
          "range_ip":[0.001,0.005,0.01,0.05,0.1],
          "range_g":[10,50,100,200],

          #NLC & GST & SIG
          "chi": 4,
          "alpha":0.75,
          "k":.6,
          "s":1
      }



def get_definition(model,param,pre="%",su=""):
    s = "% MODEL: " + model.model_name+"\n %PARAMETERS:\n"
    s += "\n".join(["{} {}={} {}".format(pre,k,v,su)for k,v in param.items()])
    return s 

if __name__ == "__main__":
    DO = "ALL"
    print sys.argv
    if len(sys.argv) >= 2:
        DO = sys.argv[1]
    
    if len(sys.argv) >= 3:
        par = sys.argv[2].split("AND")
        #print par
        for st in par:
            k,v = st.split("=")
            param[k] = eval(v)
            print "{} set to {}".format(k,v)
    if len(sys.argv) >= 4:
        if sys.argv[3] == "NLC":
            MODEL = ToyContinuousNLC
            MODEL_CODE = sys.argv[3]
        if sys.argv[3] == "GST":
            MODEL = ToyContinuousGST
            MODEL_CODE = sys.argv[3]
        if sys.argv[3] == "SIG":
            MODEL = ToyContinuousSigB
            MODEL_CODE = sys.argv[3]

    print("DO: {} with model {}".format(DO,MODEL_CODE))
    param["m"] = param["r"] + param["dz"]
    
    ## Figure 2: Numerical PIP ##
    if DO == "pip" or DO == "ALL":
        print "{:-^80}".format(" PIP ")
        
        pip_file = "pip{}_T{}_n{}_step{}_repl_{}_b{}_ip{}".format(MODEL_CODE, param["T"],
                                                                  param["n"], param["precision"],
                                                                  param["replica"], param["b"],
                                                                  param["ip"])
        print pip_file
        if not os.path.exists(pip_file+".pkle"):
            pip_data,pip_param = pip.mp_pip(MODEL,param.copy(),param["precision"])
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
        heatmap_file = "heatmap_r_{}_m{}_repl{}".format(param["r"],param["m"],param["replica"])
        
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
        threshold_file = "threshold_kmax{}_{}T_{}b".format(param["kmax"],
                                                           len(param["T_range"]),
                                                           len(param["b_range"]))
        if not os.path.exists(threshold_file+".pkle"):
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

    ## Figure S1: Quelques trajectoires d'invasion (different ip) ## 
    if DO == "trajectoires":
        print "{:-^80}".format(" Trajectories ")
 

        traj_file = "trajectories_m{}_{}ip_{}g".format(param["m"],len(param["range_ip"]),len(param["range_g"]))
        if not os.path.exists(traj_file+".pkle"):
            data = [np.zeros((len(param["range_ip"]), len(param["range_g"]))),
                    np.zeros((len(param["range_ip"]), len(param["range_g"])))]
            for j,g in enumerate(param["range_g"]):
                for i,ip in enumerate(param["range_ip"]):
                    print i,j,data[0].shape,data[1].shape
                    param["g"] = g
                    param["ip"] = ip
                    data[0][i,j],data[1][i,j] = invasion.mp_invasion_fitness(MODEL,param)
                    
            with open(traj_file+".pkle","w") as fi:
                del param["g"]
                del param["ip"]
                pickle.dump((data,param),fi)
        else:
            with open(traj_file+".pkle","r") as fi:
                data,param = pickle.load(fi) 
                     
        if not os.path.exists(traj_file+"eps"):
            draw.trajectories(data,param)
            plt.savefig(traj_file+".eps")
            with open(traj_file+".eps","a") as fi:
                fi.write(get_definition(MODEL,param))
