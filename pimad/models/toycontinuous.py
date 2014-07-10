#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Continuous toy model"""

import numpy
import random
import math
from numba import jit

import pimad.model as model
from pimad.models.toymodel import ToyModel

class ToyContinuous(ToyModel):
    """ A model where the probability of attachment are conditioning both the
    payoff and the social cost.

    In this model there's still only two phenotypes at a time a resident 
    (the asocial of the toymodel) and a mutant (the social of the toymodel)

    **Modification from the toymodel :** 

    - In the aggregation phase the probaility of aggregation of two individuals 
    is the geometric mean of the phenotypes.
    - The social cost of an individual is -c*z
    - The group benefit of an individual is b*\overline{z} (mean of the social
    trait).

    """

    def __init__(self,param,tracked_values=[]):
        """Constructor"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "Continuous Toy Model"

        # The probability of attachment between a za and a zs individual is:
        self.param["pas"] = math.sqrt(self.param["pa"]*self.param["ps"])


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
        
           0. Payoff of zs individual in a group
           1. Payoff of za individual in a group
           2. Payoff of zs individual alone
           3. Payoff of za individual alone
        
        """
        ## For each patch
        for patch in range(self.population.Npatch):

            gb = self.group_benefits(patch)
            cost_s = self.cost(self.param["ps"])
            cost_a = self.cost(self.param["pa"])

            # Payoff of zs individual in a group
            
            self.population.payoff[patch,0] = gb - cost_s
            # Payoff of za individual in a group
            self.population.payoff[patch,1] = gb - cost_a
            
            # Payoff of zs individual alone
            self.population.payoff[patch,2] = -cost_s
            # Payoff of za individual alone
            self.population.payoff[patch,3] = -cost_a


    def group_benefits(self,p):
        """ Return the individual group-benefits in the p patch """
        # The group benefit is b * \overline{z} the mean social trait.
        meanZ = self.population.proportions[p,0]*self.param["ps"] 
        meanZ += ((self.population.proportions[p,1] -
                  self.population.proportions[p,0])*self.param["pa"]) 
        meanZ /= self.population.proportions[p,1]  

        return meanZ * self.b

    def cost(self,z):
        """ Return the individual cost of a z-social individual"""
        return self.c * z

# Name of the model's Class (Required for import in main program)
model_class = ToyContinuous
