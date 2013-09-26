#!/bin/sh
for model in "ToyContinuous" "ContinuousSizeThreshold" ; do
    python experiment.py $model-z05p.data -m $model -p N=1000000,mu=0,ip=0.01,pa=0.5,ps=0.51
    python experiment.py $model-z05m.data -m $model -p N=1000000,mu=0,ip=0.01,pa=0.5,ps=0.49
    python experiment.py $model-z005p.data -m $model -p N=1000000,mu=0,ip=0.01,pa=0.05,ps=0.06
    python experiment.py $model-z005m.data -m $model -p N=1000000,mu=0,ip=0.01,pa=0.05,ps=0.04
done 
