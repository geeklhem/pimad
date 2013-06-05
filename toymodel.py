#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""The toy model as defined by Garcia & De Monte 2012."""

import numpy
import random

import model


class ToyModel(model.Model):
    """A toy model of group formation by differential attachment. [Garcia & De Monte 2012]


    Needs the following parameters in *model.param* dict : 
    
    =====  =====================================================================
    Name   Parameter
    =====  =====================================================================
    b      Benefits in the pgg (int)
    c      Linear cost of altruism (int)
    ps     Attachment probability of two social individuals  (float).
    pa     Attachment probability of two asocial individuals (float).
    pas    Attachment probability of an social and an asocial individual (float).
    mu     Mutation rate (float).
    =====  =====================================================================

    
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
        
        ## For each patch
        for patch in range(self.population.Npatch):
            # Here patch size is assumed to always be T.
            patch_begin = patch * self.population.T
            patch_end = patch_begin + self.population.T

            ## Choose a random recruiter and compute the probabilities to attach.
            recruiter_index = random.randint(patch_begin,patch_end)
            
            if self.population.phenotype[recruiter_index]:
                # The recruiter is social.
                proba = (self.param["pas"],self.param["ps"])
            else: 
                # The recruiter is asocial.
                proba = (self.param["pa"],self.param["pas"])

            ## Loop on patch individuals and give them a chance to attach to the group.
            for n,i in enumerate(self.population.phenotype[patch_begin:patch_end]):
                if random.random() < proba[i]:
                    self.population.repartition[n+patch_begin] = 1
                    self.population.proportions[patch,0] += i #= 1 if social
                    self.population.proportions[patch,1] += 1
                else:
                    self.population.proportions[patch,2] += i #= 1 if social
                    self.population.proportions[patch,3] += 1
                       
            # The recruiter is always in the group. 
            if not self.population.repartition[recruiter_index]:
                self.population.repartition[recruiter_index] = True
                self.population.proportions[patch,0] += i #= 1 if social
                self.population.proportions[patch,1] += 1
                self.population.proportions[patch,2] -= i #= 1 if social
                self.population.proportions[patch,3] -= 1

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
    import math

    param = {"N":100,
             "T":10,
             "b":3,
             "c":1,
             "ps":0.3,
             "pa":0.1,
             "pas":math.sqrt(0.3*0.1),
             "mu":0.001}

    tracked_values = ["population.N","population.proportions"]

    a = ToyModel(param, tracked_values)

    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.population)
    print("\n Run:")
    a.play(5)
    print(a.traces)
