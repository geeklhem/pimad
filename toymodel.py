#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""The toy model as defined by Garcia & De Monte 2012."""

import numpy
import model

class ToyModel(model.Model):
    """A toy model of group formation by differential attachment. [Garcia & De Monte 2012]


    Needs the following parameters in *model.param* dict : 
    
    =====  ========================================================
    Name   Parameter
    =====  ========================================================
    b      Benefits in the pgg (int)
    c      Linear cost of altruism (int)
    ps     Attachment probability of a social individual   (float).
    pa     Attachment probability of an asocial individual (float).
    mu     Mutation rate
    =====  ========================================================
    
    """

    def step(self):
        """Runs one generation of the model
    
        Called by :class:`Population`.play at each generation """
        
        self.dispersion()

        self.aggregation()
        self.payoff()
        self.demographic()
        

    def aggregation(self):
        """ Define the aggregation process.
        
        =========  ============================
        **Read**   self.population.phenotype.
        **Write**  self.population.repartition, 
                   self.population.proportions.
        =========  ============================
  
        """
        pass

    def payoff(self):
        """
        Compute the payoff for each patch and each combinaison of repartition and phenotype.
        
        =========  ============================
        **Read**   self.population.phenotype.
                   self.population.repartition, 
        **Write**  self.population.payoff.
        =========  ============================
        
        .. note ::
           By line in self.population.payoff:
        
           1. Payoff of social individual in a group
           2. Payoff of asocial individual in a group
           3. Payoff of social individual alone
           4. Payoff of asocial individual alone
        
        """
        pass

    def demographic(self):
        """Life, Death, Mutation, Heredity and genealogy processes
        
        =========  ============================
        **Read**   self.population.phenotype,
                   self.population.genotype,
                   self.population.repartition,
                   self.population.payoff.
        **Write**  self.population.phenotype,
                   self.population.genotype,
                   self.population.repartition,
                   self.population.genealogy,
        =========  ============================
        """     
        
        pass

    def dispersion(self):
        """Global shuffling and reset of individuals population.arrays
        
        =========  ============================
        **Write**  self.population.phenotype,
                   self.population.genotype,
                   self.population.repartition,
                   self.population.genealogy,
        =========  ============================
        """ 
        pass

    def phenotype_heredity(self,phenotype):
        """Return the phenotype of the child cell given the one of the parent.
        
        :param phenotype: Phenotype of the parent. 
        :type phenotype: bool
        :return: (bool) - Phenotype of the child. 
        .. note ::
          Here it's an identity, this method should be overrided in a inherited model.
        """
        return phenotype

if __name__ == "__main__":

    param = {"N":100000,
             "T":1000,
             "b":3,
             "c":1,
             "ps":0.3,
             "pa":0.1,
             "mu":0.001}

    tracked_values = ["population.N"]

    a = ToyModel(param, tracked_values)

    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.population)
    print("\n Run:")
    a.play(5)
    print(a.traces)
