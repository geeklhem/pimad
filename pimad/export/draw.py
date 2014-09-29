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
                                   (0.2, 0.2, 0.2)])
    plt.contourf(array, cmap=cmap, levels=[-1000,0,1000])

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


def threshold(points):

    z = np.arange(0.001,1.001,0.001)
   
    theo = 2.0/z
    plt.plot(z,theo, color="k",label="Analytical prediction")

    c = ["red","green","blue","orange","purple","pink"]
    for n,(k) in enumerate(sorted(points.keys())):
        x,y = zip(*points[k])
        plt.scatter(x,y,label='Experimental threshold, $T={}$'.format(k),
                    color=c[n],marker=".",s=20)

    plt.legend()
    plt.xlabel("z")
    plt.ylabel("b/c")
    plt.xlim((0,1))
    plt.ylim((0,100))

    
def trajectories(data,param):
    """ 
    Args:
       data (2-tuple of np.array)
    """

    plt.figure(figsize=(10,6))
    plt.subplot(2,1,1)
    plt.title("Proportion of non extinct trajectories ($\hatz={}, z={}$)".format(param["r"],param["m"]))
    plt.plot(data[1]*100)

    plt.legend(param["range_g"],title="Number of generations" ,
               prop={'size':6},loc="lower right")

    plt.xticks(range(len(param["range_ip"])),param["range_ip"])
    plt.xlabel("Initial proportion of mutants")
    plt.ylim(50,101)
    plt.subplot(2,1,2)
    plt.title("Invasion fitness on the 10 first generation of the non extinct trajectories")
    plt.plot(data[0])
    #plt.legend(param["range_g"],title="Number of generations")
    plt.xlabel("Initial proportion of mutants")
    plt.xticks(range(len(param["range_ip"])),param["range_ip"])
    plt.tight_layout()
