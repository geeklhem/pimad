""" Graphical functions for pairwise invasibility plots"""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import numpy as np


def draw_pip(array,show=True):
    """
    Use matplotlib to draw a pairwise_invasibility plot.

    Args:
        array (np.array): a matrix giving the i_nvasion fitness for different
        values of the resident and mutant traits.
    
    """
    
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0.5, 0.5, 0.5)])
    plt.contourf(array, cmap=cmap, levels=[-1000,0,1000])

    cfin = plt.contour(array,np.arange(np.amin(array), np.amax(array)+0.1, 0.1),colors="0.1")
    cfin.set_alpha(.2)
    c = plt.contour(array,colors="k")
    plt.clabel(c)

    def fraction_tick(y, pos=0):
        return '{:0.1f}'.format(float(y)/(len(array)-1))

    ax = plt.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(fraction_tick))
    ax.xaxis.set_major_formatter(FuncFormatter(fraction_tick))
    plt.xlabel("$\hat{z}$")
    plt.ylabel("$z$")
    
    if show:
        plt.show()


def draw_array_of_pips(arrays,blist,Tlist,disp=False):
    xmax = len(set(blist))
    ymax = len(set(Tlist))
    n = 0
    for i, a in enumerate(arrays):
        n += 1
        plt.subplot(xmax,ymax,i+1)
        ax = plt.gca()
        draw_pip(a,False)
        ax.set_title("PIP b = {0}, T =  {1}".format(blist[i],Tlist[i]))
    if disp:
        plt.show()
