#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
Adaptive dynamics functions

Usage:
  adyn.py <file> numerical_pip [-f=<fitnessFunction>] [-o=<options>] [-p=<precision>] [-b=<bvalues>] [-T=<tvalues>]
  adyn.py <file> agentBased_pip [-m=<model_name>] [-o=<options>] [-p=<precision>] [-b=<bvalues>] [-T=<tvalues>] 
  adyn.py <file> load
  adyn.py <file> altruism [-p=<precision>] [-T=<tvalues>]
Options:
  -f=<fitnessFunction>     Fitness function to use [default: s_simple] 
  -m=<model_name>          Model to use (see models/models_descriptions) [default: toymodel]
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
# Main
#~~~~~~~~~~~~~~~~~~~~~~~

def main(args):
    
    if args["numerical_pip"]:
        return numerical_pip(args)
    elif args["agentBased_pip"]:
        return agent_based_pip(args)
    elif args["load"]:
        return load(args)
    elif args["altruism"]:
        return altruism(args)


#~~~~~~~~~~~~~~~~~~~~~~~~
# Actions
#~~~~~~~~~~~~~~~~~~~~~~~~


def numerical_pip(args): 
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

    return arrays

def agent_based_pip(args):
    s = models.pip.model_pip(p,ip,g,N)
    if save:
        np.savetxt(name,s)
    else:
        adaptive.draw_array(s)
    return s


def load(args):
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

    return (blist,Tlist,arrays)

def altruism(args):
    return 0


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# If the file is launched from the command line.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    data = main(args)


