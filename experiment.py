#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
PIMAD : Pimad Is Modeling Adaptive Dynamics
A modeling tool for studying adaptive evolution of grouping by adhesion.

Usage:
  main.py <file> [-g <number>]
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
  -h --help                Show this screen.
  --version                Show version.
  --license                Show license information.

"""
import sys
import math
from docopt import docopt

import traces as trace
import plots
from toymodel import ToyModel

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

def routine_pl(loaded):
     plots.proportions(loaded.traces[0]["population.proportions"],True,False)
     plots.proportions(loaded.traces[0]["population.proportions"],False,True)
     plots.proportions(loaded.traces[0]["population.proportions"],True,True)

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
    
    param = {"N":1000,
             "T":10,
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
        m = ToyModel(param, tracked_values)
        if not args["-g"]:
            g = 10
        else:
            g = args["-g"]

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


if __name__ == '__main__':
    data = main()


