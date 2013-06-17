#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Pairwise invasibility plot functions"""

import scipy.misc as sp
import numpy as np
import pylab as pl
import math
import matplotlib.colors as mcolors

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
        non_recruiter = 1 - math.sqrt(z*r)
    else: 
        # The focal mutant player is recruited
        non_recruiter = math.sqrt(z * r) 
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
    
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0.5, 0.5, 0.5)])
    pl.contourf(array, cmap=cmap, levels=[-1000,0,1000])

    cfin = pl.contour(array,np.arange(np.amin(array), np.amax(array), 0.1),colors="0.1")
    cfin.set_alpha(.2)
    c = pl.contour(array,colors="k")
    pl.clabel(c)
    if disp:
        pl.show()

def routine(p=0.1,Tlist=[50,100,200,1000],blist=[2,4,8,16,20,40,100],c=1):
    arrays = []
    b_real_list = []
    T_real_list = []
    for b in blist:
        for T in Tlist:
            print("Computing PIP for b = {0}, T =  {1}".format(b,T)) 
            try :
                arrays.append(array(p,T,b,c,True))
            except : 
                print("Error in b = {0}, T =  {1}".format(b,T)) 
            else:
                b_real_list.append(b)
                T_real_list.append(T)
    return arrays,  b_real_list,  T_real_list

def draw_array_of_pips(arrays,blist,Tlist,disp=False):
    xmax = len(set(blist))
    ymax = len(set(Tlist))
    n = 0
    for i, a in enumerate(arrays):
        n += 1
        pl.subplot(xmax,ymax,i+1)
        ax = pl.gca()
        draw_array(a,False)
        ax.set_title("PIP b = {0}, T =  {1}".format(blist[i],Tlist[i]))
    if disp:
        pl.show()


if __name__ == "__main__":
    import sys 
    import glob
    import os.path
    if len(sys.argv) == 2: 
        arrays, b, T = routine(0.1)
        for i,pip in enumerate(arrays) :
            param = "_b"+str(b[i])+"_T"+str(T[i])
            np.save("pip_"+sys.argv[1]+param,pip)
    elif len(sys.argv) == 3: 
        arrays = []
        blist = []
        Tlist = []
        for f in sorted(glob.glob("pip_"+sys.argv[1]+"*")):
            sf = os.path.basename(f).split(".")[0]
            sf = sf.split("_")
            b = int(sf[-2][1:])
            T = int(sf[-1][1:])
            
            print("Loading file {0}, parameters : b = {1} and T = {2}".format(f,b,T))
            try:
                arrays.append(np.load(f))
            except:
                print("Error Loading file {0}".format(f))
            else:
                blist.append(b)
                Tlist.append(T)
        blist,Tlist,arrays = (list(t) for t in zip(*sorted(zip(blist,Tlist,arrays))))
        draw_array_of_pips(arrays,blist,Tlist,disp=True)
    else:
        array(p=0.1,T=100,b=20,c=1,exact=True)
