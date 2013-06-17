#!/bin/sh
for f in "s_simple" "s_sizeThreshold"
do
    echo $f
    python pairwiseiplot.py $f -f $f -o t=1
    echo "-------------------------"
done
