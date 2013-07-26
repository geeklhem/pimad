#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
Invasion fitness functions for pairwise invasibility plots.
"""

import scipy.misc as sp
import numpy as np
import math
import matplotlib.pylab as pl


#########################################
# DENSITY
#########################################
def g(n,z,r,T,pmax=1):
    """Group size distribution experienced by rare z players in a r monomorphic population""

    :param n: Group size \in [0,T].
vv    :type n: int
    :param z: Value of the rare mutant social trait.
    :type z: float
    :param r: Value of the social trait in the monomorphic population \in [0,1].
    :type r: float
    :param T: Patch size (Default = 100).
    :type T: int
    :param pmax: Maximum attachment probability. 
    :type pmax: float
    :return: (float) - proportion of rare z individuals experiencing a n-sized group in a r-monomorphic population."""

    ## Highest probability possible
    if pmax:
        z *= pmax 
        r *= pmax

    ## A mutant recruiter has a n group size when n-1 residents individuals
    # over the T-1 attached to it. 
    recruiter = sp.comb(T-1,n-1) * r ** (n-1) * (1-r) ** (T-n)
    
    if n == 1:
        # A non recruiter mutant alone didn't attach when it was given the chance.
        non_recruiter = 1 - math.sqrt(z*r)
    else: 
        # The focal mutant player is recruited
        non_recruiter = math.sqrt(z * r) 
        # n-2 other residents individuals are recruited over the T-2 left.
        non_recruiter *= sp.comb(T-2,n-2) * r ** (n-2) * (1-r) ** (T-n)
    return 1/T * recruiter + (1 - 1/T) * non_recruiter
    

##########################################################
# FITNESS FUNCTIONS
#########################################################

def s_simple(m,r,T=100,b=20,c=1,options={"pmax":1}):
    """Fitness of a m z = mutant trait in a z=r monomorphic population. Using exact analytical distributions.
    
    :param m: Value of the mutant social trait \in [0,1].
    :type m: float
    :param r: Value of the social trait in the monomorphic population \in [0,1].
    :type r: float
    :param T: Patch size (Default = 100).
    :type T: int
    :param b: Benefits coefficient (Default = 20).
    :type b: int
    :param c: Cost coefficient (Default = 1).
    :type c: int
    :return: (float) - Fitness of a m z = mutant trait in a z=r monomorphic population.  

    Based on *Garcia 2013 : Evolution of a continuous social trait* Equation (8)"""
    
    
    # loners proportion
    loners = g(1,r,r,T,options["pmax"]) - g(1,m,r,T,options["pmax"])

    #Grouped individuals proportion 
    group_sum = 0
    for n in range(2,T+1):
        group_sum += g(n,m,r,T,options["pmax"])/n

    ## Mean Individual Benefits
    benefits = (  r   *  b * loners + 
                (m-r) * b * group_sum)
 
    ## Individual Cost
    cost = c * (m-r)
    
    return benefits - cost


def s_nlcost(m,r,T=100,b=20,c=1,options={"pmax":1,"cl":4}):
    """Fitness of a m z = mutant trait in a z=r monomorphic population. Using exact analytical distributions.
    
    :param m: Value of the mutant social trait \in [0,1].
    :type m: float
    :param r: Value of the social trait in the monomorphic population \in [0,1].
    :type r: float
    :param T: Patch size (Default = 100).
    :type T: int
    :param b: Benefits coefficient (Default = 20).
    :type b: int
    :param c: Cost coefficient (Default = 1).
    :type c: int
    :return: (float) - Fitness of a m z = mutant trait in a z=r monomorphic population.  

    **Options :**
 
    - pmax :
    - cl : cost linearity. Higher cl means that the cost is  linear like for 
    greater z before rocketing to infinty.
    """
    

    
    # loners proportion
    loners = g(1,r,r,T,options["pmax"]) - g(1,m,r,T,options["pmax"])

    #Grouped individuals proportion 
    group_sum = 0
    for n in range(2,T+1):
        group_sum += g(n,m,r,T,options["pmax"])/n

    ## Mean Individual Benefits
    benefits = (  r   *  b * loners + 
                (m-r) * b * group_sum)
 

    def cost_function(c,nl,z):
        """ Return the individual cost of a z-social individual"""
        if z == 1:
            z = 1-0.001
        return c * z * math.exp(1/((1-z)**(1/float(nl))))

    ## Individual Cost
    cost = cost_function(c,options["nl"],m) - cost_function(c,options["nl"],r)
    
    return benefits - cost
   

def s_sizeThreshold(m,r,T=100,b=20,c=1,options={}):
    """Fitness of a m z = mutant trait in a z=r monomorphic population. 
    Only groups smaller than t/T provide benefits.

    
    :param m: Value of the mutant social trait \in [0,1].
    :type m: float
    :param r: Value of the social trait in the monomorphic population \in [0,1].
    :type r: float
    :param T: Patch size (Default = 100).
    :type T: int
    :param b: Benefits coefficient (Default = 20).
    :type b: int
    :param c: Cost coefficient (Default = 1).
    :type c: int
    :return: (float) - Fitness of a m z = mutant trait in a z=r monomorphic population.  
    :param t: Maximal patch fraction \in [0,1] that form a beneficial group.
    :type t: float
    """
    try:
        t = options["t"]
    except:
        t = 0.75
    #
    sum_one = 0
    sum_two= 0
    for n in range(2,int(t*T)):
        g_mutant = g(n,m,r,T)
        sum_one += g_mutant - g(n,r,r,T)
        sum_two += g_mutant/n

    ## Mean Individual Benefits
    benefits = (  r   *  b * sum_one + 
                  (m-r) * b * sum_two)
 
    ## Individual Cost
    cost = c * (m-r)
    return benefits - cost



def sigma(z,T):
    s = 0
    for n in range(2,T):
        s += g(n,z+0.001,z,T)/n
    return s

def get_color():
       for item in ['r', 'g', 'b', 'c', 'm', 'y', 'k']:
          yield item

def altruismConditions(p): 
    z = [x/float(p) for x in range(p)]

    color = get_color()
    
    for T in (100,):
        acolor = next(color)    
        y = [1/sigma(r,T) for r in z]
        y2 = [T/(r+0.0000000000000000001) for r in z]
        pl.plot(z,y, color= acolor, label="T = {0}".format(T))
        pl.plot(z,y2,'--', color=acolor)

    y3 = [2/(r+0.0000000001)for r in z]
    pl.plot(z,y3, color="k")

    ax = pl.gca()
    ax.axis((0,1,0,1250))
    pl.show()

if __name__ == "__main__":
    altruismConditions(100)

    
    
