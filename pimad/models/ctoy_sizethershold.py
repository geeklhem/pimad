#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Continuous toy model with group size threshold"""

import numpy
import random
import math

import models.model as model
from toycontinuous import ToyContinuous


class ContinuousSizeThreshold(ToyContinuous):
    """ Continuous Toy Model with a group size threshold

    **Modification from the toycontinuous :**
    
    - if groupsize is greater than param["t"]/param["T"] group benefits are null.
    Default value for t is 0.75.

    """

    def __init__(self,param,tracked_values=[]):
        """Constructor"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = """ContinuousSizeThreshold, 
        Continuous Toy Model with a group size threshold """

        # The probability of attachment between a za and a zs individual is:
        self.param["pas"] = math.sqrt(self.param["pa"]*self.param["ps"])

        # Default value for t is 0.75.
        if not "t" in self.param:
            self.param["t"] = 0.75

    def group_benefits(self,p):
        """ Return the individual group-benefits in the p patch """
        # The group benefit is b * \overline{z} the mean social trait. if the 
        # group is small enough.
        if self.population.proportions[p,1] < self.param["t"]/self.param["T"]:

            meanZ = self.population.proportions[p,0]*self.param["ps"] 
            meanZ += ((self.population.proportions[p,1] -
                      self.population.proportions[p,0])*self.param["pa"]) 
            meanZ /= self.population.proportions[p,1]  

            return meanZ * self.b

        # Or it's null.
        else:
            return 0

# Name of the model's Class (Required for import in main program)
model_class = ContinuousSizeThreshold

