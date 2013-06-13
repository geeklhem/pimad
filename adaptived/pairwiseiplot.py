#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Pairwise invasibility plot functions"""

import scipy.misc as sp
import numpy as np
import pylab as pl

################################################################################
# ESTIMATION #
################################################################################


def d(n,z,T=100):
    """Group size distribution experienced by players in a z-monomorphic population
    
    :param n: Group size \in [0,T].
    :type n: int
    :param z: Value of the social trait in the monomorphic population \in [0,1].
    :type z: float
    :param T: Patch size (Default = 100).
    :type T: int
    :return: (float) - proportion of individuals of a z-monomorphic population experiencing a n-sized group."""

    # A recruiter has a n group size when n-1 individuals over the T-1 attached to it. 
    recruiter = sp.comb(T-1,n-1) * z ** (n-1) * (1-z) ** (T-n+1)
    
    if n == 1:
        # A non recruiter alone didn't attach when it was given the chance.
        non_recruiter = 1 - z
    else: 
        # The focal player is recruited
        non_recruiter = z 
        # n-2 other individuals are recruited over the T-2 left.
        non_recruiter *= sp.comb(T-2,n-2) * z ** (n-2) * (1-z) ** (T-n+2)
    return 1/T * recruiter + (1 - 1/T) * non_recruiter


def s(m,r,T=100,b=20,c=1):
    """Fitness of a m z = mutant trait in a z=r monomorphic population. Approximated for near m and z
    
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
    :return: (float) - Fitness of a m z = mutant trait in a z=r monomorphic population.   """
    
    group_sum = 0
    for n in range(2,T+1):
        group_sum += d(n,r,T)/n 
    return (m-r) * b * group_sum - c

################################################################################
# EXACT #
################################################################################
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
    recruiter = sp.comb(T-1,n-1) * r ** (n-1) * (1-r) ** (T-n+1)
    
    if n == 1:
        # A non recruiter mutant alone didn't attach when it was given the chance.
        non_recruiter = 1 - z
    else: 
        # The focal mutant player is recruited
        non_recruiter = z 
        # n-2 other residents individuals are recruited over the T-2 left.
        non_recruiter *= sp.comb(T-2,n-2) * r ** (n-2) * (1-r) ** (T-n+2)
    return 1/T * recruiter + (1 - 1/T) * non_recruiter
    

def s_exact(m,r,T=100,b=20,c=1):
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
    loners = d(1,r,T) - g(1,m,r,T)

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
   



################################################################################
# DISPLAY #
################################################################################

def array(p=0.1,T=100,b=20,c=1,exact=True):
    """ Compute the fitness for all values """
    size = int(1/p)
    a = np.zeros((size,size))
    if exact:
        for m in range(size):
            for r in range(size):
                a[m,r] = s_exact(m*p,r*p,T,b,c)
    else:
        for m in range(size):
            for r in range(size):
                a[m,r] = s(m*p,r*p,T,b,c)
    return a

def draw_array(array,disp=True):
    pl.pcolor(array)
    c = pl.contour(array,colors="k")
    pl.clabel(c)
    if disp:
        pl.show()
