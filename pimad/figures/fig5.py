""" Plot of b/c min and b/c max as a function of hat{z} """
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as sp


#########################################
# DENSITY
#########################################
def g(n,z,r,T,pmax=1):
    """Group size distribution experienced by rare z players in a r monomorphic population""

    :param n: Group size \in [0,T].
    :type n: int
    :param z: Value of the rare mutant social trait.
    :type z: float
    :param r: Value of the social trait in the monomorphic population \in [0,1].
    :type r: float
    :param T: Patch size (Default = 100).
    :type T: int
    :param pmax: Maximum attachment probability. 
    :type pmax: float
    :return: (float) - proportion of rare z individuals experiencing a n-sized group in a r-monomorphic population."""

    ## Highest probability possible
    if pmax:
        z *= pmax 
        r *= pmax

    ## A mutant recruiter has a n group size when n-1 residents individuals
    # over the T-1 attached to it. 
    recruiter = sp.comb(T-1,n-1) * r ** (n-1) * (1-r) ** (T-n)
    
    if n == 1:
        # A non recruiter mutant alone didn't attach when it was given the chance.
        non_recruiter = 1 - np.sqrt(z*r)
    else: 
        # The focal mutant player is recruited
        non_recruiter = np.sqrt(z * r) 
        # n-2 other residents individuals are recruited over the T-2 left.
        non_recruiter *= sp.comb(T-2,n-2) * r ** (n-2) * (1-r) ** (T-n)
    return 1/T * recruiter + (1 - 1/T) * non_recruiter


def sigma(z,T):
    s = 0
    for n in range(2,T):
        s += g(n,z+0.001,z,T)/n
    return s


def draw(p,T=100): 
    z = np.arange(0.001,1.001,0.001)

    y = [1/sigma(r,T) for r in z]
    plt.plot(z,y, color= "red", label="T = {0}".format(T))

    y2 = [T]*len(z)
    plt.plot(z,y2,'--', color="red")


    y3 = 2.0/z
    plt.plot(z,y3, color="k")

    ax = plt.gca()
    ax.axis((0,1,0,1250))
    plt.show()

if __name__ == "__main__":
    draw(1000)
