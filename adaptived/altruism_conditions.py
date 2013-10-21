""" Plot of b/c min and b/c max as a function of hat{z} """

def sigma(z,T):
    s = 0
    for n in range(2,T):
        s += g(n,z+0.001,z,T)/n
    return s

def get_color():
       for item in ['r', 'g', 'b', 'c', 'm', 'y', 'k']:
          yield item

def altruismConditions(p,Tlist=(100,)): 
    z = [x/float(p) for x in range(p)]

    color = get_color()
    
    for T in Tlist :
        acolor = next(color)    
        y = [1/sigma(r,T) for r in z]
        y2 = [T/(r+0.0000000000000000001) for r in z]
        pl.plot(z,y, color= acolor, label="T = {0}".format(T))
        pl.plot(z,y2,'--', color=acolor)

    y3 = [2/(r+0.0000000001)for r in z]
    pl.plot(z,y3, color="k")

    ax = pl.gca()
    ax.axis((0,1,0,1250))
    pl.show()

if __name__ == "__main__":
    altruismConditions(100)

    
    
