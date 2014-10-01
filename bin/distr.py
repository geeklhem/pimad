
# coding: utf-8

# In[1]:

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from  scipy.stats import binom 
from pimad.models.toycontinuous import ToyContinuous
from pimad.figures.convergence import *
import os


## Fiugure 1: Group size distribution

# In[2]:
if not os.path.exists("sizedistr.eps"):
    x = range(101)
    z = 1/3
    T = 100
    y = analytical({"m":1/3,"r":1/3})
    plt.plot(x,y,color="red",label="$\hat{z}_1=1/3T$",ls = "steps")

    ax = plt.gca()
    ax.annotate(r'$1-\hat{z}_1$', xy=(0,1-z),xycoords="data", textcoords="offset points",
                xytext=(+40,0),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    z = 2/3
    y = analytical({"m":2/3,"r":2/3})
    plt.plot(x,y,color="blue",label="$\hat{z}_2=2/3T$",ls = "steps")


    ax.annotate(r'$1-\hat{z}_2$', xy=(0,1-z),xycoords="data", textcoords="offset points", xytext=(+40,0),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

    ax.axis([-5,T,0,1-0.33+0.1])
    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")
    ax.xaxis.set_ticks([1,T])
    ax.set_xticklabels(['$1$','$T$'])
    ax.yaxis.set_ticks([])
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_coords(.45, -0.025)
    ax.set_xlabel("Group size")
    ax.set_ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("sizedistr.eps")
    plt.clf()

def sigma(z,T):
    s = 0
    for n in range(2,T+1):
        s += g(n,z+0.001,z,T)/n
    return s


# In[5]:
if not os.path.exists("altruism.eps"):
    T = 100
    z = np.arange(0.001,1.001,0.001)
    minz = 2.0/z
    maxz = [1/sigma(r,T) for r in z]


    # In[35]:

    plt.plot(z,minz, "r",label="$z_{min}$")
    plt.plot(z,maxz, "g",label="$z_{max}$")
    plt.hlines(T,color="b",*plt.xlim(),label="$T$")

    bbox = dict(boxstyle="round,pad=0.3", fc="white", ec="k", lw=0.5)

    plt.xlabel("$\hat z$")
    plt.ylabel("$b/c$")
    plt.xlim((0,1))
    plt.ylim((0,200))
    plt.legend(title="$T={}$".format(T))
    plt.annotate("$A$",(0.5,150),size=10,bbox=bbox)
    plt.annotate("$B$",(0.5,50),size=10,bbox=bbox)
    plt.annotate("$C$",(0.02,10),size=10,bbox=bbox)

    plt.savefig("altruism.eps")




