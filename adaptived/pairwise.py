import models.pip 
import adaptived.pairwiseiplot as adaptive
import numpy as np
import options

print(options.test_v)

def main(name,p=100,ip=0.1,g=10,N=100000,save=False):
    s = models.pip.model_pip(p,ip,g,N)
    if save:
        np.savetxt(name,s)
    else:
        adaptive.draw_array(s)
    return s

def load(name):
    s = np.loadtxt(name)
    adaptive.draw_array(s)
    return s

