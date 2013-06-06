#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""
import numpy

class Population:
    """ A generic class that represents populations data.

    :param N: Population size.
    :param T: Patch size.
    :type N: int
    :type T: int

    **Attributes**

    ====================================== ===============================================
    Name                                   Value       
    ====================================== ===============================================
    **Integer**
    -------------------------------------- -----------------------------------------------
    :class:`Population`.N                  Population size (int).
    :class:`Population`.T                  Aggregation patch size (int). 
    :class:`Population`.Npatch             Number of patches (int).
    :class:`Population`.ip                 Initial proportion of social (float).
    **Individuals data**
    -------------------------------------- -----------------------------------------------
    :class:`Population`.phenotype          Individual phenotype (N np.array bool).        
    :class:`Population`.genotype           Individual genotype (N np.array bool).
    :class:`Population`.repartition        Individual "is in a group ?" (N np.array bool).
    :class:`Population`.genealogy          Index of individual parent (N np.array int).    
    **Patch data**
    -------------------------------------- -----------------------------------------------
    :class:`Population`.proportions        Group comp proportions (N/T*4 np.array float).    
    :class:`Population`.payoff             Payoffs by patch (N/T*4 np.array float).
    ====================================== ===============================================
    
    .. note ::
      Nb. :class:`Population`.genealogy[i]  is the index of the individual i parent in the individuals arrays of precedent generation. If the individual survived for more than one generation, it's -1. 

    """

    def __init__(self,N,T,ip=0.5):
        """Population constructor."""
        self.N = N 
        self.T = T
        self.Npatch = N/T
        self.ip = ip 
        if N%T:
            self.Npatch += 1

        #Individuals data
        self.genotype = numpy.array([0]*(N-int(N*ip))+[1]*int(N*ip), dtype=numpy.bool)
        self.phenotype = numpy.array([0]*(N/2)+[1]*(N/2), dtype=numpy.bool)
        self.repartition = numpy.array([0]*N, dtype=numpy.bool)
        self.genealogy = numpy.array([0]*N, dtype=numpy.int)
       
        #Patch data
        self.payoff = numpy.zeros((self.Npatch,4),dtype=numpy.float)
        self.proportions = numpy.zeros((self.Npatch,4),dtype=numpy.float)

    def flush_patch_arrays(self):
        #Patch data
        self.payoff = numpy.zeros((self.Npatch,4),dtype=numpy.float)
        self.proportions = numpy.zeros((self.Npatch,4),dtype=numpy.float)


    def __str__(self):
        s = "Generic population: \n"
        s += "Population size: {0:1.0e}\n".format(self.N)
        s += "Patch size: {0}\n".format(self.T)
        return s

    def __repr__(self):
        return "Generic population of {0:1.0e} individuals.".format(self.N)

if __name__ == "__main__":
    # Test code
    a = Population(1000,100)
    print(a)
   
