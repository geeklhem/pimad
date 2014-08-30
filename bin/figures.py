from __future__ import division
import matplotlib.pyplot as plt
import numpy as np

from pimad import pip 
import pimad.export.draw as draw 

PRECISION_PIP = 0.1
REPLICAS_PIP = 4

if __name__ == "__main__":
## Figure 1: Group Size distribution ##
## Figure 2: Numerical PIP ##

    fname = "pip_{}".format(PRECISION_PIP,REPLICAS_PIP)
    if not os.path.exist(pip_file+".pkle"):
        pip,param = mp_pip(repl=REPLICAS_PIP,precision=PRECISION_PIP)
        with open(fname+".pkle","w") as fi:
            pickle.dump((pip,param),fname+".pkle")
    else:
        with open(fname+".pkle","w") as fi:
            pip,param = pickle.load(fname+".pkle") 

    if not os.path.exist(pip_file+".eps"):
        draw.pip(pip,False)
        plt.savefig(fname+".eps")


## Figure 3: ESS Heatmap ##
## Figure 4: Sociality threshold ##
## Figure 5: Altruism threshold ##
## Figure 6: Numerical PIP with size-threshold ##
