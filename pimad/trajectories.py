from __future__ import division
from pimad.models.toycontinuous import ToyContinuous
import matplotlib.pyplot as plt
import pimad.export.draw as draw
import numpy as np
import multiprocessing as mp 
import itertools
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import os

# Probes functions
def mutants_prop(model):
    return model.population.mutants.sum() / (model.p["n"] * model.p["T"])

def mutants_pop(model):
    return model.population.mutants.sum() 

def trajectoire(model=ToyContinuous,probe_function=mutants_prop,**kargs):
    # Default parameters:
    param = {"n":100,"T":1000,"ip":0,"m":0.5,"r":0.5,"b":20,"c":1,"g":1000,"mu":1e-5,"replicas":6}
    
    # Overiding default parameters
    for k,v in kargs.items():
        param[k] = v

    # Parallel computation
    pool = mp.Pool()
    args = itertools.repeat((model,probe_function,param),param["replicas"])
    all_traj = pool.map(trajectoire_star,args)

    # Mean and STD
    #print(all_traj)
    all_traj = np.array(all_traj)
    #print(all_traj)
    mean = all_traj.mean(0)
    std = all_traj.std(0)
    return mean,std,all_traj



def trajectoire_star(args):
    #print("PID: {}".format(os.getpid()))
    model = args[0]
    probe_function = args[1]
    param = args[2]

    np.random.seed()
    m = model(param)
    traj = np.zeros(m.p["g"])

    for i in range(m.p["g"]):
        m.step()
        traj[i] = probe_function(m)
    return traj


def fitness(traj,t0=0,t1=10):
    f = np.nan_to_num(np.log10(traj[:,t1]/traj[:,t0]))
    return f.mean(), f.std()

def disp_trajectoire(traj,label="unnamed",color="blue"):
    plt.plot(range(len(traj[0])),traj[0],label=label,color=color)
    plt.fill_between(range(len(traj[0])),traj[0]-traj[1],traj[0]+traj[1],color=color,alpha=0.1)
    print "{0} trajectory : {1[1]}  generations, {1[0]} replicas".format(label,traj[2].shape)
    print "Fitness (0/10) : {} std={}".format(*fitness(traj[2]))
    print "Fitness (1/11) : {} std={}".format(*fitness(traj[2],1,11))
  #  plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.0%'))

def test():
    disp_trajectoire(trajectoire(T=100,g=200,m=0.49,ip=0.1),"0.49","red")
    disp_trajectoire(trajectoire(T=100,g=200,ip=0.1),"0.5")

    disp_trajectoire(trajectoire(T=100,g=200,m=0.51,ip=0.1),"0.51","green")
    disp_trajectoire(trajectoire(T=100,g=200,ip=0.1),"0.5","k")
  
    plt.legend()
    plt.show()
