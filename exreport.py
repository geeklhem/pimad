#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Export tools for trace object as an experimental report. 

Create a html file report with figures"""

import matplotlib.pyplot as plt
import plots as trace_plots

def export(tr,name):
    base_filename = name #tr.model_name.split(" ")
    trace_plots.proportions(tr,True,False,False)
    plt.savefig(base_filename+"_repartitions.svg")
    plt.clf()
    trace_plots.proportions(tr,False,True,False)
    plt.savefig(base_filename+"_phenotype.svg")
    plt.clf()
    trace_plots.proportions(tr,True,True,False)
    plt.savefig(base_filename+"_proportions.svg")
    plt.clf()
    trace_plots.group_level_cov(tr,False)
    plt.savefig(base_filename+"_grpLvlCov.svg")
    plt.clf()
    trace_plots.groupsize_surface(tr,False)
    plt.savefig(base_filename+"_surface.svg")
    plt.clf()

if __name__ == "__main__":
    import sys 
    import traces

    if len(sys.argv) == 2: 
        try:
            data = traces.load_trace(sys.argv[1])
        except : 
            print("Error in {} file import.".format(sys.argv[1]))
        else:
            print(" {} import successfull.".format(sys.argv[1]))
            export(data,sys.argv[1])
