#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Continuous toy model with non linear cost function"""

import numpy
import random
import math

import models.model as model
from toycontinuous import ToyContinuous

class ContinuousNLCost(ToyContinuous):
    """ Continuous Toy model with a non linear cost function

    **Modification from the toycontinuous :**
    
    - Cost of the social trait is not linear (-cz) but tends toward infinty 
    as z tends toward 1.

    Take a new parameter cl (cost linearity). Higher cl means that the cost is
    linear like for greater z before rocketing to infinty.
"""

    def __init__(self,param,tracked_values=[]):
        """Constructor"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = """ContinuousNLCost, 
        Continuous Toy Model with a group size threshold """

        # The probability of attachment between a za and a zs individual is:
        self.param["pas"] = math.sqrt(self.param["pa"]*self.param["ps"])

        # Default value for cl is 4.
        if not "cl" in self.param:
            self.param["cl"] = 4


    def cost(self,z):
        """ Return the individual cost of a z-social individual"""
        return self.c * z * math.exp(1/(1-z)**(1/self.param["cl"]))

# Name of the model's Class (Required for import in main program)
model_class = ContinuousNLCost
