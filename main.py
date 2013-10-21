#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""
PIMAD : Pimad Is Modeling Adaptive Dynamics
A modeling tool for studying adaptive evolution of grouping by adhesion.

Usage:
  main.py <file> [-g=<number>] [-p=<parameters>] [-m=<modelName>] [-e=<eqCondition>] [-t=<trackedValues>] [--export] [-v|-q]
  main.py load <file> [--export] [-v|-q]
  main.py (-h | --help)
  main.py --version
  main.py --license

Options:
  -g=<number>              Number of generations to run
  -p=<parameters>          Model parmeters in the format "p1=value p2=value p3=v"
  -m=<modelName>           Model name - File name in models/model_definitions (without extension).
  -e=<eqCondition>         Halting condition if number of generation is not precised [default: 1000]
  -t=<trackedValues>       Model attributes to save, separated by a comma [default: population.proportions]
  --export                 HTML Export 
  -q                       Quiet mode (No confirmation that things are working as expected.)
  -v                       Verbose mode (Detailed information for diagnosing problems.)
  -h --help                Show this screen.
  --version                Show version.
  --license                Show license information.
"""

import sys
import ast
import copy
import logging

from components.docopt import docopt

import models.traces
import models.model
import models.model_definitions.toymodel as default_model
import options
import output.exreport as exporter

__author__ = "Guilhem Doulcier"
__copyright__ = "Copyright 2013, Guilhem Doulcier"
__license__ = "GPLv3"

try:
    with open('version.txt', 'r') as f:
        __version__ = f.read()
except:
        __version__ = 0

def main(args):
    """ Main function, providing the modeling features of pimad """

    # -Logging options----------------------------------------------------------
    log_level = logging.INFO # default
    if args["-q"]:
        log_level = logging.WARNING
    elif args["-v"]:
        log_level = logging.DEBUG
    logging.root.handlers = []
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=log_level)
    #---------------------------------------------------------------------------

    # -License------------------------------------------------------------------
    if  args["--license"]:
        print('\n    PIMAD : Pimad is modeling adaptive dynamics - v'+__version__)
        print("    Copyright (C) 2013 Guilhem DOULCIER")
        print("    This program comes with ABSOLUTELY NO WARRANTY.")
        print("    This program is free software: you can redistribute it and/or modify")
        print("    it under the terms of the GNU General Public License as published by") 
        print("    the Free Software Foundation, either version 3 of the License, or") 
        print("    (at your option) any later version.\n")
        sys.exit(2)
    # --------------------------------------------------------------------------


    # -Loading-------------------------------------------------------------------
    if args["load"]:
        try:
            data = models.traces.load_trace(args['<file>'])
        except : 
            logging.error("Error in {0} file import.".format(args['<file>']))
            data = "Error"
        else:
            logging.info("{0} import successfull.".format(args['<file>']))
    # --------------------------------------------------------------------------


    # -Run Model----------------------------------------------------------------
    else:
        tracked_values = args['-t'].split(",")
        
        # Getting default parameters 
        param = copy.copy(options.p_default)

        # Parsing parameters
        if args["-p"]:
            custom_p = args["-p"].split(",")
            for p in custom_p:
                p = p.split("=")
                try:
                    p[1] = ast.literal_eval(p[1])
                except:
                    logging.error("Error in parsing {0} argument. Set to default.".format(p[0]))
                else:
                    param[p[0]]=p[1]

        # Selecting model
        if args["-m"]:
            try:
                module_name = "models.model_definitions."+args["-m"]
                module = __import__(module_name,fromlist='.') 
                m = module.model_class(param, tracked_values)
            except:
                logging.error("Model {0} not found. Using Default.".format(args["-m"]))
                module = __import__("models.model_definitions."+options.default_model,fromlist='.') 
                m = module.model_class(param, tracked_values)
        else:
            module = __import__("models.model_definitions."+options.default_model,fromlist='.') 
            m = module.model_class(param, tracked_values)

        # Info
        logging.info("Using model: {0}".format(m))
        logging.info("Population: {0}".format(m.population))
        logging.info("Running...")

        # Running 
        if not args["-g"]:
            m.equilibrium(int(args["-e"]))
        else:
            m.play(int(args["-g"]))

        # Saving
        data = models.traces.Trace(m)
        models.traces.save_trace(data,args['<file>'])
    # --------------------------------------------------------------------------

    # ---Export-----------------------------------------------------------------
    if  args["--export"]:
        logging.info("Exporting...")
        exporter.export(data,args['<file>'])
    # --------------------------------------------------------------------------
    
    return(data)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# If the file is launched from the command line.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    args = docopt(__doc__, version=__version__)
    data = main(args)

 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Examples of inputs. 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# These are fake values for the "args" arguments of main() (as outputted by docopt). 
# Useful in interactive mode.
default_args = {'--help': False,
                '--license': False,
                '--version': False,
                '-e': '1000',
                '-g': None,
                '-m': None,
                '-p': None,
                '-t': 'population.proportions',
                '<file>': None}
