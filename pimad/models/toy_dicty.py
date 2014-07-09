#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Dictyo toy model"""

import numpy
import random
import math

import models.model as model
from toymodel import ToyModel

class ToyDictyo(ToyModel):
    """ Based on the toy model but a part of the group don't reproduce. (spore/stem).

    .. note::
    - Only 80% of the group (cheaters first) get a chance to reproduce.
    - Alone individuals reproduce only if the parmeter alone_repro = True (Does not change the fitness normalization fonction. [Default = TRUE] 
    """

    def __init__(self,param,tracked_values=[]):
        """Constructeur"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "ToyDictyo [Modified Toymodel]"
        if not "alone_repro" in self.param:
            self.param["alone_repro"]=True
        if self.param["alone_repro"]:
            self.model_name += "Loners can reproduce"
        else:
            self.model_name += "Loners can't reproduce"

    def demographic(self):
            """Global life, Death, Mutation, Heredity and genealogy processes

            Only 80% of the group get a chance to reproduce. Asocial first.

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

            ########### MODIFIED PART ##########################################
            ## Each alone individual has a chance to reproduce once           ##
            ## 80% of the grouped individuals (asocial first) has a chance to ##
            ## reproduce once.                                                ##
            ####################################################################
            
            ## Keep a track of the number of allowed potential reproducer in each
            ## patch's group.
            nb_repro_group = numpy.zeros((self.population.Npatch,1))
            nb_repro_group_p = numpy.zeros((self.population.Npatch,2))

            for np,patch in enumerate(self.population.proportions):
                nb_repro_group[np] = int(patch[1]*0.8)
                nb_repro_group_p[np,0] = patch[1]-patch[0]
                if nb_repro_group_p[np,0] > nb_repro_group[np]:
                    nb_repro_group_p[np,0] = nb_repro_group[np]
                    nb_repro_group_p[np,1] = 0
                else:
                    nb_repro_group_p[np,1] = nb_repro_group[np] - nb_repro_group_p[np,0]
            
            # Each individual is maybe allowed to reproduce once.
            for n,g in enumerate(self.population.genotype):
                p = self.population.phenotype[n] 
                r = self.population.repartition[n]
                patch = n/self.population.T
                
                allowed = 1

                # Only 80% of the group is allowed to try !
                if r: #If attached.
                    if nb_repro_group_p[patch,p]:
                        nb_repro_group_p[patch,p] -= 1
                    else:
                        allowed = 0
                else:
                    allowed = self.param["alone_repro"]
                
                
                if allowed and random.random()<fitness[patch,fitness_index[(p,r)]]:
                
                    ######### END OF MODIFIED PART #####################################"
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

# Name of the model's Class (Required for import in main program)
model_class = ToyDictyo
