#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
Pairwise invasibility plot functions

Usage:
  pairwiseiplot.py <file_name> [-p=<precision>] [-b=<bvalues>] [-T=<tvalues>]   [-f=<fitnessFunction>] [-o=<options>] 
 pairwiseiplot.py <file_name> load
Options:
  -f=<fitnessFunction>     Fitness function to use [default: s_simple] 
  -p=<precision>           Precision [default: 0.1]
  -b=<bvalues>             b values to loop through [default: 4,8,20,40]
  -T=<tvalues>             t values to loop through [default: 50,100,500]
  -o=<options>             Option for the fitness function [default: t=0.75,nl=4,pmax=1]
  -h --help                Show this screen.
"""

__version__ = "alpha"


import scipy.misc as sp
import numpy as np
import pylab as pl
import math
import matplotlib.colors as mcolors
import traceback
import ast
from docopt import docopt
import fitness_fct as fitness
from matplotlib.ticker import FuncFormatter



#~~~~~~~~~~~~~~~~~~~~~~~
# Compute
#~~~~~~~~~~~~~~~~~~~~~~~

def array(p=0.1,T=100,b=20,c=1,fitness_func="s_simple",options={}):
    """ Compute the fitness for all values """
    ff = getattr(fitness,fitness_func)
    size = int(1/p)
    a = np.zeros((size,size))
    for m in range(size):
        for r in range(size):
            a[m,r] = ff(m*p,r*p,T,b,c,options)
    return a


def routine(p=0.1,
            Tlist=[50,100,500,1000],blist=[4,8,20,40],c=1,
            ff="s_simple",fitnessOptions={}):
    arrays = []
    b_real_list = []
    T_real_list = []
    for b in blist:
        for T in Tlist:
            print("Computing PIP for b = {0}, T =  {1} ".format(b,T)) 
            try :
                arrays.append(array(p,T,b,c,ff,fitnessOptions))
            except :
                exc_type, exc_value, exc_traceback = sys.exc_info() 
                print("Error in b = {0}, T =  {1}".format(b,T))
                traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)
                
            else:
                b_real_list.append(b)
                T_real_list.append(T)
    return arrays,  b_real_list,  T_real_list


#~~~~~~~~~~~~~~~~~~~~~~~
# Draw
#~~~~~~~~~~~~~~~~~~~~~~~

def draw_array(array,show=True):
    
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0.5, 0.5, 0.5)])
    pl.contourf(array, cmap=cmap, levels=[-1000,0,1000])

    cfin = pl.contour(array,np.arange(np.amin(array), np.amax(array), 0.1),colors="0.1")
    cfin.set_alpha(.2)
    c = pl.contour(array,colors="k")
    pl.clabel(c)

    def fraction_tick(y, pos=0):
        return '{:0.1f}'.format(float(y)/(len(array)-1))

    ax = pl.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(fraction_tick))
    ax.xaxis.set_major_formatter(FuncFormatter(fraction_tick))
    pl.xlabel("$\hat{z}$")
    pl.ylabel("$z$")

    

    if show:
        pl.show()


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

#~~~~~~~~~~~~~~~~~~~~~~~
# Main
#~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    import sys 
    import glob
    import os.path
    args = docopt(__doc__, version=__version__)

    #~~~~~~~~New files~~~~~~#
    if not args["load"]:
       
        #----1----# Parsing parameters
        options = {}
        if args["-o"]:
            custom_p = args["-o"].split(",")
            for p in custom_p:
                p = p.split("=")
                try:
                    p[1] = ast.literal_eval(p[1])
                except:
                    print("Error in parsing {0} argument".format(p[0]))
                else:
                    options[p[0]]=p[1]
        
        #print options
        blist = map(int, args["-b"].split(","))
        tlist = map(int, args["-T"].split(","))
        pre = float(args["-p"])

        #----2----# Compute
        arrays, b, T = routine(pre,tlist,blist,ff=args["-f"],fitnessOptions=options)
        
        #----3----# Save
        for i,pip in enumerate(arrays) :
            param = "_b"+str(b[i])+"_T"+str(T[i])
            np.save("pip_"+args["<file_name>"]+param,pip)

    #~~~~~~~~Loading files~~~~~~#
    else:
        #----1----# Load
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

        #----2----# Sort 
        blist,Tlist,arrays = (list(t) for t in zip(*sorted(zip(blist,Tlist,arrays))))

        #----3----# Display
        draw_array_of_pips(arrays,blist,Tlist,disp=True)
