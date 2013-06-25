#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
PIMAD : Pimad Is Modeling Adaptive Dynamics
A modeling tool for studying adaptive evolution of grouping by adhesion.

Usage:
  main.py <file> [-g=<number>] [-p=<parameters>] [-m=<modelName>] [-e=<eqCondition>] [-t=<trackedValues>]
  main.py (-h | --help)
  main.py --version
  main.py --license

Pimad will try to load any trace data found in <file>. If it's unsuccessfull it 
will create one using the model defined in this file. It will play it for ten
generations unless the "-g" option is provided.

You should use this file with interactive python :
`ipython -i exepriment.py test.data`.
You will then be able to apply output function to the loaded or generated data
using the `data` object.

Options:
  -g=<number>              Number of generations to run
  -p=<parameters>          Model parmeters in the format "p1=value p2=value p3=v"
  -m=<modelName>           Model name (A subclass of Model)
  -e=<eqCondition>         Halting condition if number of generation is not precised [default: 1000]
  -t=<trackedValues>       Model attributes to save, separated by a comma [default: population.proportions]
  -h --help                Show this screen.
  --version                Show version.
  --license                Show license information.
"""

import sys
import math
import ast
from docopt import docopt
import models.traces as trace
import models.toymodel as toymodels
from models.model import Model

__author__ = "Guilhem Doulcier"
__copyright__ = "Copyright 2013, Guilhem Doulcier"
__license__ = "GPLv3"

try:
    with open('version.txt', 'r') as f:
        __version__ = f.read()
except:
        __version__ = "unknown version"

__email__ = "guilhem.doulcier@ens.fr"
__date__ = "2013"


def main():
    args = docopt(__doc__, version=__version__)
    if  args["--license"]:
        print('\n    PIMAD : Pimad is modeling adaptive dynamics - v'+__version__)
        print("    Copyright (C) 2013 Guilhem DOULCIER")
        print("    This program comes with ABSOLUTELY NO WARRANTY.")
        print("    This program is free software: you can redistribute it and/or modify")
        print("    it under the terms of the GNU General Public License as published by") 
        print("    the Free Software Foundation, either version 3 of the License, or") 
        print("    (at your option) any later version.\n")
        sys.exit(2)

    #Default values
    param = {"N":100,
             "T":100,
             "ip":0.1,
             "b":20,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.8*0.3),
             "mu":0.01}

    # Parsing parameters
    if args["-p"]:
        custom_p = args["-p"].split(",")
        for p in custom_p:
            p = p.split("=")
            try:
                p[1] = ast.literal_eval(p[1])
            except:
                print("Error in parsing {0} argument".format(p[0]))
            else:
                param[p[0]]=p[1]
                
    tracked_values = args['-t'].split(",")
    #print(tracked_values)

    try :
        loaded = trace.load_trace(args['<file>'])
    except:
        print("File {0} not found, creating one.".format(args["<file>"]))
        if args["-m"]:
            try:
                m = getattr(toymodels,args["-m"])(param, tracked_values)
            except:
                print "model not found, using toymodel"
                m = toymodels.ToyModel(param, tracked_values)
        else:
            m = toymodels.ToyModel(param, tracked_values)
        
        print("\n Model:")
        print(m)
        print("\n Population:")
        print(m.population)
        print("\n Run:")

        if not args["-g"]:
            m.equilibrium(int(args["-e"]))
        else:
            m.play(int(args["-g"]))

        tr = trace.Trace(m)
        trace.save_trace(tr,args['<file>'])
        return(tr)
    else:
        print("File {0} loaded successfully.".format(args["<file>"]))
        return(loaded)

def rescue(r):
    """Recreate a trace object from an acient version"""
    m = Model(r.p)
    m.traces = r
    return trace.Trace(m)

if __name__ == '__main__':
    data = main()

