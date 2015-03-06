"""convergence.py : convergence plot"""

from __future__ import division
import numpy as np
from  scipy.stats import binom 

from pimad.models.toycontinuous import ToyContinuous
import matplotlib.pyplot as plt

def g(n,m,r,T):
    """Group size distribution experienced by an individual of trait m in
    a resident poulation r.

    Args:
        n (int): group size
        m (float): mutant trait
        r (float): resident trait
        T (int): patch size
    
    Return:
        float: proportion of group of size n"""

    if 0<n<=T:
        attach = np.sqrt(m*r)

        # the focal cell is recruiter:
        R = binom.pmf(n-1,T-1,attach)

        # the focal cell is not recruiter
        if n==1:
            # the cell is alone
            r = 1-attach
        else:
            # the cell is in a group
            r = attach * binom.pmf(n-2,T-2,attach)

        return 1/T * R + (1-(1/T))*r
    else:
        return 0

def analytical_mono(param={}):
    default = {
        "n":100,
        "T":100,
        "ip":0.1,
        "b":20,
        "c":1,
        "g":1,
        "r":0.5,
        "m":0.5
    } 

    for k,v in default.items():
        if k not in param:
            param[k] = v

    x = np.arange(param["T"]+1)
    y = param["r"]*np.array([(binom(param["T"],k) * param["r"]**k * (1-param["r"])**(param["T"]-k)) 
         for k in x])
    y[1] = 1-param["r"]
    return y


def analytical(param={}):
    default = {
        "n":100,
        "T":100,
        "ip":0.1,
        "b":20,
        "c":1,
        "g":1,
        "r":0.5,
        "m":0.5,
        "mu":0,
    } 

    for k,v in default.items():
        if k not in param:
            param[k] = v

    x = range(param["T"]+1)
    y_a = [g(i,param["r"],param["m"],param["T"]) for i in x]
    return y_a

def numerical(param={}):
    default = {
        "n":100,
        "T":100,
        "ip":0.1,
        "b":20,
        "c":1,
        "g":1,
        "r":0.5,
        "m":0.5,
        "mu":0,
    } 

    for k,v in default.items():
        if k not in param:
            param[k] = v

    m = ToyContinuous(param,[])
    m.play(param["g"])
    
    g = np.zeros(param["T"]+1)
    g[1] = m.population.aggregated.sum()
    for s in  m.population.aggregated.sum(0):
        g[s] += s
    g /= g.sum()
    return g


def simple(n=10):

    T = 100
    x = range(T+1)

    y_a = np.array([g(i,0.5,0.5,T) for i in x])
    #y_a /= y_a.sum()
    y_n = numerical({"T":T,"n":n})
    #    print len(x),len(y_a),len(y_n)

    plt.subplot(2,1,1)
    plt.bar(x,y_a,label="analytical",alpha=0.5,color="orange")
    plt.bar(x,y_n,label="numerical",alpha=0.5,color="green")
    plt.legend()
    plt.subplot(2,1,2)
    plt.plot(x,(y_a-y_n)**2)
    plt.ylabel("square error")
    plt.show()

def convergence(n_range,T=100):
    error = []
    pp = {"T":T}
    y_a = analytical(pp)

    for n in n_range:
        pp["n"] = n
        ee = []
        for i in range(5):
            y_n = numerical(pp)
            e = np.sum((y_a-y_n)**2)
            ee.append(e)
        error.append(np.mean(ee))
    
    plt.plot(n_range,error)
    plt.xlabel("n")
    plt.ylabel("Cumulated square error")
    plt.show()

def main():
    n_range = np.arange(2,1000,1)
    #print n_range
    convergence(n_range)

if __name__ == "__main__":
    main()
