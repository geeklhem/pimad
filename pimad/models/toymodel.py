#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""The toy model as defined by Garcia & De Monte 2012."""

import numpy
import random
import math

import pimad.model as model


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Toy model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

    def __init__(self,param,tracked_values=[]):
        """Constructeur"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "Toymodel [Garcia & De Monte 2012]"

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

        .. note ::
           By line in self.population.proportions:
        
           0. Social individual in the group.
           1. Individuals in the group.
           2. Social individuals alone.
           3. Individuals alone.
  
        """
        
        ## For each patch
        for patch in range(self.population.Npatch):
            # Here patch size is assumed to always be T.
            patch_begin = patch * self.population.T
            patch_end = patch_begin + self.population.T 

            ## Choose a random recruiter and compute the probabilities to attach.
            recruiter_index = random.randint(patch_begin,patch_end-1)
            
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
        
           0. Payoff of social individual in a group
           1. Payoff of asocial individual in a group
           2. Payoff of social individual alone
           3. Payoff of asocial individual alone
        
        """
        ## For each patch
        for patch in range(self.population.Npatch):
            group_benefit = (self.b*self.population.proportions[patch,0])
            group_benefit /= self.population.proportions[patch,1]  
            
            # Payoff of social individual in a group
            self.population.payoff[patch,0] = group_benefit - self.c 
            # Payoff of asocial individual in a group
            self.population.payoff[patch,1] = group_benefit
            # Payoff of social individual alone
            self.population.payoff[patch,2] = - self.c # and not b-c 
            # Payoff of asocial individual alone
            self.population.payoff[patch,3] = 0 

            

    def demographic(self):
        """Global life, Death, Mutation, Heredity and genealogy processes
        
        =========  ============================
        **Read**   self.population.phenotype,
                   self.population.genotype,
                   self.population.repartition,
                   self.population.payoff.
        **Write**  self.population.phenotype,
                   self.population.genotype,
                   self.population.genealogy.
        =========  ============================
        """     
        
        newborn_genotype = []
        newborn_phenotype = []
        newborn_genealogy = []

        ## Normalize the payoff to give the fitness
        fitness = numpy.array(self.population.payoff, dtype=numpy.float)
        fitness -= numpy.min(fitness)
        fitness /= numpy.max(fitness)
        
        #fitness index for the couples of (phenotype, repartition).
        fitness_index = {(1,1):0, #social in group.
                         (0,1):1, #asocial in group.
                         (1,0):2, #social alone.
                         (0,0):3} #asocial alone.

        ## Each individual has a chance to reproduce once.
        for n,g in enumerate(self.population.genotype):
            p = self.population.phenotype[n] 
            r = self.population.repartition[n]
            patch = n/self.population.T
            if random.random()<fitness[patch,fitness_index[(p,r)]]:
                #The genotype is inherited or flipped if mutated.
                if random.random()<self.param["mu"]:
                    # Mutated : if g = 1, not g = 0 and if g = 0, not g = 1 
                    newborn_genotype.append(not g)
                else:
                    newborn_genotype.append(g)
                
                # Phenotype is inherited according to the rules of phenotype_heredity().
                newborn_phenotype.append(self.phenotype_heredity(p,g))
                
                # Genealogy is the index of the parent in the previous generation.
                newborn_genealogy.append(n)

        ## Death process : newborn are inserted in random position inside the new population, thus killing the one whose place they take.
        for i in range(len(newborn_genotype)):
            n = random.randint(0,self.population.N-1)
            self.population.phenotype[n] = newborn_phenotype[i]
            self.population.genotype[n]  = newborn_genotype[i]
            self.population.genealogy[n] = newborn_genealogy[i]


    def dispersion(self):
        """Global shuffling and reset population.arrays
        
        =========  ============================
        **Write**  self.population.phenotype,
                   self.population.genotype,
                   self.population.repartition,
                   self.population.genealogy,
                   self.population.payoff.
                   self.population.proportions.
        =========  ============================
        """ 

        ## Reset of the individuals population arrays
        self.population.repartition[:] = 0
        self.population.genealogy[:] = -1

        ## Flush the arrays patches.
        self.population.flush_patch_arrays()

        ## Shuffling the individuals ! 
        p = numpy.random.permutation(self.population.N)
        self.population.phenotype = self.population.phenotype[p] 
        self.population.genotype = self.population.genotype[p]

                   
    def phenotype_heredity(self,phenotype,genotype):
        """Return the phenotype of the child cell given the one of the parent.
        
        :param phenotype: Phenotype of the parent. 
        :type phenotype: bool
        :param genotype: genotype of the parent. 
        :type genotype: bool
        :return: (bool) - Phenotype of the child. 
        .. note ::
          Here it's an identity, this method should be overrided in a inherited model.
        """
        return genotype

# Name of the model's Class (Required for import in main program)
model_class = ToyModel

