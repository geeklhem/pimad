""" Graphical functions for pairwise invasibility plots"""

def draw_pip(array,show=True):
    
    cmap = mcolors.ListedColormap([(1, 1, 1), 
                                   (0.5, 0.5, 0.5)])
    pl.contourf(array, cmap=cmap, levels=[-1000,0,1000])

    cfin = pl.contour(array,np.arange(np.amin(array), np.amax(array), 0.1),colors="0.1")
    cfin.set_alpha(.2)
    c = pl.contour(array,colors="k")
    pl.clabel(c)

    def fraction_tick(y, pos=0):
        return '{:0.1f}'.format(float(y)/(len(array)-1))

    ax = pl.gca()
    ax.yaxis.set_major_formatter(FuncFormatter(fraction_tick))
    ax.xaxis.set_major_formatter(FuncFormatter(fraction_tick))
    pl.xlabel("$\hat{z}$")
    pl.ylabel("$z$")
    

    if show:
        pl.show()


def draw_array_of_pips(arrays,blist,Tlist,disp=False):
    xmax = len(set(blist))
    ymax = len(set(Tlist))
    n = 0
    for i, a in enumerate(arrays):
        n += 1
        pl.subplot(xmax,ymax,i+1)
        ax = pl.gca()
        draw_pip(a,False)
        ax.set_title("PIP b = {0}, T =  {1}".format(blist[i],Tlist[i]))
    if disp:
        pl.show()
