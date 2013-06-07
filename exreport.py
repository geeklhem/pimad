#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Export tools for trace object as an experimental report. 

Create a html file report with figures"""

import matplotlib.pyplot as plt
import plots as trace_plots
import glob

def export(tr,name):
    try:
        export_fig(tr,name)
    except:
        print("Error in creating plots")
    with open("reports/"+name+"_report.html", 'w') as f:
        f.write(export_html(tr,name))

def export_fig(tr,base_filename):
    base_filename = "reports/" + base_filename
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

def export_html(tr,name):
    try:
        mname = tr.model_name
    except:
        mname = "Unknown"

    try:
        date = tr.date
    except:
        date = "Unknown"

    try:
        g = len(tr.traces[0]["population.proportions"])
    except:
        g = "Unknown"

    try:
        version = tr.version
    except:
        version = "Unknown"

    p = "<ul>"
    for k,v in tr.p.items():
        p += "<li><strong>{0}</strong> :  {1}</li>".format(k,v)
    p += "</ul>"

    page = """<html>  
    <title>{name}</title>
    <body><h1>Experimental report : {name}</h1>
    <h2>Informations</h2>
    <strong>Model name</strong> : {mn}<br/>
    <strong>Date </strong> : {date} <br/>
    <strong>Version nb </strong> : {version} <br/>
    <strong>Generations</strong> : {g} <br/>
    <strong>Parameters</strong> : {p}<br/>
    <h2>Figures:</h2>""".format(name=name,p=p,mn=mname,date=date,g=g,version=version)
    
    for i in glob.glob(name+"*.svg"):
        page += '\n<img src="{path}"/><br/>'.format(path=i)

    page += "</body>"
    return page

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
