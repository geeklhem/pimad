#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
PIMAD : Pimad Is Modeling Adaptive Dynamics
A modeling tool for studying adaptive evolution of grouping by adhesion.

Usage:
  main.py <file> [-g <number>] [-p <init_prop>]
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
  -g                       Number of generations to run
  -p                       Initial proportion of social individuals in [0,1]
  -h --help                Show this screen.
  --version                Show version.
  --license                Show license information.

"""

import sys
import math
from docopt import docopt
import traces as trace
from toymodel import ToyModel, ToyDictyo

__author__ = "Guilhem Doulcier"
__copyright__ = "Copyright 2013, Guilhem Doulcier"
__license__ = "GPLv3"

try:
    with open('version.txt', 'r') as f:
        __version__ = f.read()
except:
        __version__ = "unknown"

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


    if not args["-p"]:
        pi = 0.1
    else:
        pi = float(args["<init_prop>"])

    
    param = {"N":1000000,
             "T":100,
             "ip":pi,
             "b":20,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.8*0.3),
             "mu":0.01}

    tracked_values = ["population.proportions"]

        

    try :
        loaded = trace.load_trace(args['<file>'])
    except:
        print("File {0} not found, creating one.".format(args["<file>"]))
        #m = ToyModel(param, tracked_values)
        m = ToyDictyo(param, tracked_values)
        
        if not args["-g"]:
            g = 10
        else:
            g = int(args["<number>"])
        
        

        print("\n Model:")
        print(m)
        print("\n Population:")
        print(m.population)
        print("\n Run:")
        m.play(g)
        tr = trace.Trace(m)
        trace.save_trace(tr,args['<file>'])
        return(tr)
    else:
        print("File {0} loaded successfully.".format(args["<file>"]))
        return(loaded)

def rescue(r):
    """Recreate a trace object from an acient version"""
    param = {"N":1000000,
             "T":100,
             "b":20,
             "ip":0.5,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.8*0.3),
             "mu":0.01}
    tracked_values = ["population.proportions"]
    m = ToyModel(param, tracked_values)
    m.traces = r
    return trace.Trace(m)

if __name__ == '__main__':
    data = main()

