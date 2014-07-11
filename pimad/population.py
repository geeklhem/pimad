#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""
import numpy as np

class Population:
    """A generic class that represents populations data.

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
      Nb. :class:`Population`.genealogy[i] is the index of
      the individual i parent in the individuals arrays of precedent
      generation. If the individual survived for more than one
      generation, it's -1.

    """

    def __init__(self,T=100,n=50,ip=0.5):
        """Population constructor.

        Args:
        
            n (int): Number of patches.
            T (int): Patch size.
            ip (int): Initial proportion of mutants (phenotype 1) individuals.
        """

        
        self.T = T
        self.n = n
        self.N = T * n 
        self.ip = ip 

        #Individuals data
        self.genotype = np.zeros((self.T,self.n))
        self.genotype.flat[0:int(self.N*self.ip)] = 1
        np.random.shuffle(self.genotype.flat)
        
        self.phenotype = np.zeros((self.T,self.n))
        self.phenotype.flat[0:int(self.N*self.ip)] = 1
        np.random.shuffle(self.phenotype.flat)

        self.repartition = np.zeros((self.T,self.n),dtype=np.bool)
        self.genealogy = np.zeros((self.T,self.n))
        
        #Patch data
        self.payoff = np.zeros((self.n,4),dtype=np.float)
        self.proportions = np.zeros((self.n,4),dtype=np.float)

    @property
    def mutants_by_patch(self):
        return self.phenotype.sum(0)

    
    def __str__(self):
        s = "Generic population: \n"
        s += "Population size: {0:1.0e}\n".format(self.N)
        s += "Patch size: {0} ({1} patches)\n".format(self.T,self.n)
        return s

    def __repr__(self):
        return "Generic population of {0:1.0e} individuals.".format(self.N)

if __name__ == "__main__":
    # Test code
    a = Population(1000,100,0.1)
    print(a)
   
