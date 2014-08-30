from __future__ import division
import os 

import matplotlib.pyplot as plt
import numpy as np

from pimad import pip 
from pimad import invasion
import pimad.export.draw as draw 

PRECISION_PIP = 0.1
REPLICAS_PIP = 4
PRECISION_HEATMAP = 0.1
REPLICAS_HEATMAP = 4

if __name__ == "__main__":
## Figure 1: Group Size distribution ##
## Figure 2: Numerical PIP ##

    pip_file = "pip_{}".format(PRECISION_PIP,REPLICAS_PIP)
    if not os.path.exists(pip_file+".pkle"):
        pip_data,param = pip.mp_pip(repl=REPLICAS_PIP,precision=PRECISION_PIP)
        with open(pip_file+".pkle","w") as fi:
            pickle.dump((pip_data,param),fname+".pkle")
    else:
        with open(pip_file+".pkle","w") as fi:
            pip_data,param = pickle.load(fname+".pkle") 

    if not os.path.exist(pip_file+".eps"):
        draw.pip(pip_data,False)
        plt.savefig(fname+".eps")


## Figure 3: INVASION Heatmap ##

    heatmap_file = "heatmap_{}".format(PRECISION_HEATMAP,REPLICAS_HEATMAP)
    if not os.path.exists(heatmap_file+".pkle"):
        data,param = invasion.heatmap()
        with open(heatmap_file+".pkle","w") as fi:
            pickle.dump((data,param),fname+".pkle")
    else:
        with open(heatmap_file+".pkle","w") as fi:
            data,param = pickle.load(fname+".pkle") 

    if not os.path.exist(heatmap_file+".eps"):
        draw.heatmap(data,False)
        plt.savefig(fname+".eps")


## Figure 4: Sociality threshold ##
    threshold_file = "threshold_{}".format(PRECISION_THRESHOLD,REPLICAS_THRESHOLD)
    if not os.path.exists(threshold_file+".pkle"):
        data,param = invasion.threshold_dicho(model,param,STEP_THRESHOLD_DICHO)
        with open(threshold_file+".pkle","w") as fi:
            pickle.dump((data,param),fname+".pkle")
    else:
        with open(threshold_file+".pkle","w") as fi:
            data,param = pickle.load(fname+".pkle") 

    if not os.path.exist(threshold_file+".eps"):
        draw.threshold(data,False)
        plt.savefig(fname+".eps")

## Figure 5: Altruism threshold ##
## Figure 6: Numerical PIP with size-threshold ##
