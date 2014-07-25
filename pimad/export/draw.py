""" Graphical functions for pairwise invasibility plots"""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import numpy as np
plt.rc('font', size=12) 

def pip(array,show=True):
    """
    Use matplotlib to draw a pairwise_invasibility plot.

    Args:
        array (np.array): a matrix giving the i_nvasion fitness for different
        values of the resident and mutant traits.
    
    """
    
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0.5, 0.5, 0.5)])
    plt.contourf(array, cmap=cmap, levels=[-1000,0,1000])

    #cfin = plt.contour(array,np.arange(np.amin(array), np.amax(array)+1, 1),colors="0.1")
    #cfin.set_alpha(.2)
    c = plt.contour(array,np.arange(np.amin(array), np.amax(array)+1, 1),colors="k")
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


def heatmap(array,param, show=True):
    plt.rc('text', fontsize=15) 
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0, 0, 0)])
    array[0,0] = 1
    plt.imshow(array, cmap=cmap, vmin=0,vmax=1,interpolation='none')

    plt.xticks(range(array.shape[1]),param["b_range"],rotation=90)
    plt.yticks(range(array.shape[0]),param["T_range"])

    plt.xlabel("$b/c$")
    plt.ylabel("$T$")
    mi,ma = plt.ylim()
    plt.ylim(ma,mi)
    
    if show:
        plt.show()


def empirical_zstar(points):

    z = np.arange(0.001,1.001,0.001)
   
    theo = 2.0/z
    plt.plot(z,theo, color="k",label="Analytical prediction")

    c = ["red","green","blue"]
    for n,(k) in enumerate(sorted(points.keys())):
        x,y = zip(*points[k])
        plt.scatter(x,y,label='Experimental threshold, $T={}$'.format(k),
                    color=c[n],marker=".",s=20)

    plt.legend()
    plt.xlabel("z")
    plt.ylabel("b/c")
    plt.xlim((0,1))
    plt.ylim((0,100))

    
