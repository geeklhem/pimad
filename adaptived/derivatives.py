#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Pairwise invasibility plot functions"""

import scipy.misc as sp
import numdifftools as nd
import numpy as np

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


def ds(m,r,T=100,b=20,c=1):
    """Derivate of the relative growth rate of the m mutant trait in a z monomorphic population. 
    
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
    :return: (float) - Derivate of the relative growth rate of the m mutant trait in a z monomorphic population.  """
    
    def dd(n,t):
        def ddd(x):
            return d(n,x,T)
        return ddd

    loners = -b * m * float(nd.Derivative(dd(1,T))(r)) 
    grouped = 0
    for n in range(2,T+1):
        grouped += 1/float(n) + float(nd.Derivative(dd(n,T))(r))  
    
    return  loners + b * grouped - c


def array(p=0.1,T=100,b=20,c=1):
    size = int(1/p)
    a = np.zeros((size,size))
    for m in range(size):
        for r in range(size):
           a[m,r] = ds(m*p,r*p,T=100,b=20,c=1)
    return a
