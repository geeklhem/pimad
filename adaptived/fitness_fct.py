#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
Invasion fitness functions for pairwise invasibility plots.
"""

import scipy.misc as sp
import numpy as np
import math




#########################################
# DENSITY
#########################################
def g(n,z,r,T):
    """Group size distribution experienced by rare z players in a r monomorphic population""

    :param n: Group size \in [0,T].
    :type n: int
    :param z: Value of the rare mutant social trait.
    :type z: float
    :param r: Value of the social trait in the monomorphic population \in [0,1].
    :type r: float
    :param T: Patch size (Default = 100).
    :type T: int
    :return: (float) - proportion of rare z individuals experiencing a n-sized group in a r-monomorphic population."""
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

def s_simple(m,r,T=100,b=20,c=1,options={}):
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
    loners = g(1,r,r,T) - g(1,m,r,T)

    #Grouped individuals proportion 
    group_sum = 0
    for n in range(2,T+1):
        group_sum += g(n,m,r,T)/n

    ## Mean Individual Benefits
    benefits = (  r   *  b * loners + 
                (m-r) * b * group_sum)
 
    ## Individual Cost
    cost = c * (m-r)
    

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
