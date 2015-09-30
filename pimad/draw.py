"""Some graphical functions for quick result visualization."""
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.ticker import FuncFormatter
import numpy as np
plt.rc('font', size=12) 

def pip(array,show=True,contour_lines=False):
    """
    Use matplotlib to draw a pairwise invasibility plot.
    

    Args:
        array (np.array): a matrix giving the i_nvasion fitness for different
        values of the resident and mutant traits.
        show: call plt.show in the end.
        contour_lines: if false draw only a black and white pip.
    """
    
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0.2, 0.2, 0.2)])
    plt.contourf(array, cmap=cmap, levels=[-1000,1,1000])

    if contour_lines:
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

def threshold(points):

    z = np.arange(0.001,1.001,0.001)
   
    theo = 2.0/z
    plt.plot(theo,z, color="k",label="Analytical prediction $z^*=2b/c$")

    markers=[".","+"]
    c = ["red","green","blue","orange","purple","pink"]
    for n,(k) in enumerate(sorted(points.keys())):
        x,y= zip(*points[k])
        if len(points) <= 2:
            plt.plot(y,x,color="k",alpha=.1)
            plt.scatter(y,x,label='$T={}$'.format(k),
                        color="k",marker=markers[n],s=20)
        else:
            plt.plot(y,x,color=c[n],alpha=.1)
            plt.scatter(x,y,label='$T={}$'.format(k),
                        color=c[n],marker=".",s=20)


        
    plt.legend()
    plt.ylabel("z")
    plt.xlabel("b/c")
    plt.ylim((0,1))
    plt.xlim((0,50))

    
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
    plt.ylim(-1,101)
    plt.subplot(2,1,2)
    plt.title("Invasion fitness on the 10 first generation of the non extinct trajectories")
    plt.plot(data[0])
    #plt.legend(param["range_g"],title="Number of generations")
    plt.xlabel("Initial proportion of mutants")
    plt.xticks(range(len(param["range_ip"])),param["range_ip"])
    plt.tight_layout()


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

