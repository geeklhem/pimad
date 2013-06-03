#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""
import numpy

class Population:
    """ A generic class that represent populations data.

    :param N: Population size.
    :param Z: Population resident phenotype.        
    :param G: Population resident genotype.
    :param T: Patch size.
    :type N: int
    :type Z: float        
    :type G: float        
    :type T: int

    **Attributes**

    ====================================== ===============================================
    Name                                   Value       
    ====================================== ===============================================
    :class:`Population`.N                  Population size (int) 
    :class:`Population`.T                  Aggregation patch size (int) 
    :class:`Population`.resident_phenotype Resident phenotype of the population (float) 
    :class:`Population`.resident_genotype  Resident genotype of the population (float) 
    :class:`Population`.phenotype          Individual phenotype (N np.array float)        
    :class:`Population`.genotype           Individual genotype (N np.array float)
    :class:`Population`.payoff             Individual payoff (N np.array float)
    :class:`Population`.group              Individual "is in a group ?" (N np.array bool)
    ====================================== ===============================================

    """

    def __init__(self,N,T,Z,G=None):
        """Population constructor."""
        self.N = N 
        self.resident_phenotype = Z
        if G != None:
            self.resident_genotype  = G
        else:
            self.resident_genotype  = 0.0
        self.T = T
        self.genotype = numpy.array([G]*N, dtype=numpy.float)
        self.phenotype = numpy.array([Z]*N, dtype=numpy.float)
        self.group = numpy.array([1]*N)
        self.payoff = numpy.array([0]*N)
        self.update()

    def _compute_groupsize(self):
        """Create the groupsize array."""
        self.group_size = numpy.array([0] * (self.N/self.T),dtype=numpy.int) 
        for n,i in enumerate(self.group):
            self.group_size[n/self.T] += i

    def update(self):
        """Update the internal cache variable after the aggregation proccess (i.e group_size)."""
        self._compute_groupsize()

    def flush(self):
        """ Shuffle individuals arrays and reset the group/payoff arrays."""
        np.random.shuffle(self.genotype)
        np.random.shuffle(self.phenotype)
	# TO DO : Keep the two values together columnwise.
        self.group = numpy.array([0]*N)
        self.payoff = numpy.array([0]*N)
        
    def group_number(self,i):
        """ Return the group of individual i, 0 if none.

        :param i: individual number < self.N.
        :type i: int 
        :return: int -- group number or 0 if alone."""
        
        if self.group[i]:
            return (i/self.T)+1
        else:
            return 0
    def traits_values(self):
        """ Return the list of phenotype values found in this population.

        :return: numpy array -- array of unique occurences in :class:`Population`.phenotype.
        """ 
        return numpy.unique(a.phenotype)

    def trait_number(self,z):
        """Return the number of individual having a social trait of z.

        :param z: social trait value.
        :type z: float
        :return: int -- number of "z-individuals". 
        """
        return np.histogram(self.phenotype,[z,z])[0][0]/self.N

    def group_density(self,z):
        """ Return the group distribution of z-social individuals.


        :param z: social trait value.
        :type z: float
        :return: numpy array [1,T] -- density of groups. """
        density = [0]*(self.T+1)
        for n,i in enumerate(self.phenotype):
            if i == z:
                if self.group[n]:
                    density[self.group_size[i/self.T]] += 1
                else:
                    density[0] += 1
        return density

    def __str__(self):
        s = "Generic population: \n"
        s += "Population size: {:1.0e}\n".format(self.N)
        s += "Patch size: {}\n".format(self.T)
        s += "Resident phenotype : {} and genotype : {}\n".format(self.resident_phenotype,self.resident_genotype)
        return s

    def __repr__(self):
        return "Generic population of {:1.0e} individuals.".format(self.N)

if __name__ == "__main__":
    a = Population(1000,100,0.1)

    print(a)
    print(a.group_size)
    print(a.group_density(0.1))

