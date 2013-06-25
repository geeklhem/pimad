#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Export tools for trace object as an experimental report. 

Create a html file report with figures"""

import matplotlib.pyplot as plt
import output.plots as trace_plots
import models.traces as traces
import glob
import os.path
import numpy as np

def export(tr,name):
    #supress the extension if any.
    try:
        name = name.split(".")[0]
    except:
        pass
    try:
        export_csv(tr,name)
    except:
        print("Error in exporting raw data")
        print sys.exc_info()

    try:
        export_fig(tr,name)
    except:
        print("Error in creating plots")
        print sys.exc_info()

    with open(os.path.join("reports/",name+"_report.html"), 'w') as f:
        f.write(export_html(tr,name))
    with open(os.path.join("reports/","index.html"), 'w') as f:
        page = """<html>  <head>
        <title>Experimental reports index</title>
        <style type="text/css">
        img {max-width:100%;}
        </style>
        </head><body>
        <h1>Experimental reports index</h1>
        <ul>
        """
        
        for i in sorted(glob.glob(os.path.join("reports/","*_report.html"))):
            path_i = os.path.basename(str(i))
            name_i = str(path_i).split(".")[0]
            page += '\n<li><a href="{path}">{name}</a></li>'.format(path=path_i,
                                                                    name=name_i)

        page += "</ul></body>"

        f.write(page)

def export_fig(tr,base_filename):
    base_filename = os.path.join("reports/" + base_filename)
    if "population.proportions" in tr.traces[0]:
        print("Generating population.proportions plots...")
        trace_plots.proportions(tr,True,False,False)
        f = plt.gcf()
        f.set_dpi(150)
        d = f.get_size_inches()
        f.set_size_inches( (d[0]*1.5,d[1]) )
        plt.savefig(base_filename+"_repartitions.png",bbox_inches="tight")
        plt.clf()
        trace_plots.proportions(tr,False,True,False)
        plt.savefig(base_filename+"_phenotype.png",bbox_inches="tight")
        plt.clf()
        trace_plots.proportions(tr,True,True,False)
        plt.savefig(base_filename+"_proportions.png",bbox_inches="tight")
        plt.clf()
        trace_plots.group_level_cov(tr,False)
        plt.savefig(base_filename+"_grpLvlCov.png",bbox_inches="tight")
        plt.clf()
        trace_plots.groupsize_surface(tr,False)
        plt.savefig(base_filename+"_surface.png",bbox_inches="tight")
        plt.clf()
    if "global_proportions" in tr.traces[0]:
        print("Generating global_proportions plots...")

def export_csv(tr,name):
    with open(os.path.join("reports/",name+"_parameters.csv"), 'w') as f:
        for k,v in sorted(tr.p.items()):    
            f.write('"{0}",{1}\n'.format(k,v))

    for k,v in tr.traces[0].items():
        k=k.replace(".","_")
        try:
            np.savetxt(os.path.join("reports/",name+"_"+k+".csv"), v, delimiter=",")
        except: 
            with open(os.path.join("reports/",name+"_"+k+".csv"),"w") as f:
                for i, data_slice in enumerate(v):
                    np.savetxt(f, data_slice, delimiter=",")

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
        version = "unknown version number"


    try:
        host = tr.host
    except:
        host = "an unknown computer"

    p = "<ul>"
    for k,v in sorted(tr.p.items()):
        p += "<li><strong>{0}</strong> :  {1}</li>".format(k,v)
    p += "</ul>"
 
    csv_list = "<ul>"
    for i in sorted(glob.glob(os.path.join("reports/",name+"*.csv")),reverse=True):
        csv_list += '<li><a href="{path}">{path}</a>'.format(path=os.path.basename(i))
    csv_list += "</ul>"

    page = """<html><head>  
    <title>{name}</title>
    <style type="text/css">
        img {{max-width:100%;}}
        </style>
        </head>
    <body><h1>Experimental report : {name}</h1>
    <h2>Informations</h2>
    <strong>Model name</strong> : {mn}<br/>
    <strong>Date </strong> : {date} <strong> on </strong> {host} <strong> running</strong> pimad {version}<br/>
    <strong>Generations</strong> : {g} <br/>
    <strong>Parameters</strong> : {p}<br/>
   <strong>Raw data</strong> : {csv}<br/> <h2>Figures:</h2>""".format(name=name,p=p,mn=mname,date=date,g=g,version=version,host=host,csv=csv_list)
    
    for i in sorted(glob.glob(os.path.join("reports/",name+"*.svg")),reverse=True):
        page += '\n<img src="{path}"/><br/>'.format(path=os.path.basename(i))
    for i in sorted(glob.glob(os.path.join("reports/",name+"*.png")),reverse=True):
        page += '\n<img src="{path}"/><br/>'.format(path=os.path.basename(i))


    page += "</body>"
    return page

if __name__ == "__main__":
    import sys 
    
    if len(sys.argv) == 2: 
        try:
            data = traces.load_trace(sys.argv[1])
        except : 
            print("Error in {0} file import.".format(sys.argv[1]))
        else:
            print("{0} import successfull.".format(sys.argv[1]))
            export(data,sys.argv[1])

    else:
        for f in glob.glob("*.data"):
            try:
                data = traces.load_trace(f)
            except : 
                print("Error in {0} file import.".format(f))
            else:
                print("  {0} import successfull.".format(f))
                export(data,f)
