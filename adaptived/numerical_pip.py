def array(p=0.1,T=100,b=20,c=1,fitness_func="s_simple",options={"pmax":1}):
    """ Compute the fitness for all values """
    ff = getattr(fitness,fitness_func)
    size = int(1/p)
    a = np.zeros((size,size))
    for m in range(size):
        for r in range(size):
            a[m,r] = ff(m*p,r*p,T,b,c,options)
    return a
