""" Graphical functions for pairwise invasibility plots"""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import numpy as np
plt.rc('text', fontsize=15) 

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


def heatmap(array,show=True):
    plt.rc('text', fontsize=15) 
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0, 0, 0)])
    array[0,0] = 1
    plt.imshow(array, cmap=cmap, vmin=0,vmax=1,interpolation='nearest')
    #array = array[::-1,:]
    po = np.arange(0,3.1,0.1)
    T_range = [int(x) for x in np.power([10]*len(po),po)]

    b_range = np.arange(2,105,3)  

    plt.xticks(range(array.shape[1]),b_range,rotation=90)
    plt.yticks(range(array.shape[0]),T_range)

    print len(T_range), array.shape,len(b_range)
    plt.xlabel("$b/c$")
    plt.ylabel("$T$")
    mi,ma = plt.ylim()
    plt.ylim(ma,mi)
    
    if show:
        plt.show()


def empirical_zstar(points,test_zone):

    z = np.arange(0.001,1.001,0.001)
    
    theo = 2.0/z
    plt.plot(z,theo, color="k",label="Analytical prediction")
    #    plt.plot(test_zone[1],test_zone[0], color="g",)
    #     plt.plot(test_zone[2],test_zone[0], color="b",)

    x,y = zip(*points)
    plt.scatter(x,y,label="Experimental threshold",color="red")
    plt.legend()
    plt.xlabel("z")
    plt.ylabel("b/c")
    plt.xlim((0,1))
    plt.ylim((0,100))
    plt.show()
    
