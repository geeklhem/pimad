#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Epigenetic toy model"""

import numpy
import random
import math
import logging

import models.model as model
from toymodel import ToyModel


class ToyEpigenetic(ToyModel):
    """ [Orso 2013]
    
    A model with epigenetic heredity. 

    Needs the following supplementary parameters in *model.param* dict : 
    
    =====  =====================================================================
    Name   Parameter
    =====  =====================================================================
    alpha  Probability of direct phenotipic inheritance.
    q0     Probability for a genotype 0 individual to have a 1 phenotype*
    q1     Probability for a genotype 1 individual to have a 1 phenotype*
    =====  =====================================================================

    * If there is no direct phenotypic inheritance.


    .. note ::
           If alpha is not set in input, it's set to 0. (No direct phenotypical
       inheritance) 
           If only q0 or q1 is set in input, q1=q0
           If neither q0 nor q1 is set in input,  Q = [0,1] (direct genotypic
       inheritance without switch).

    Exemple:
    python experiment.py test -m ToyEpigenetic -p alpha=0.1,q0=0.5,q1=0.1
    """

    def __init__(self,param,tracked_values=[]):
        """Constructeur"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "ToyEpigenetic [Modified Toymodel]"
        
        # If parameters are not defined, set default values...
        if not "alpha" in self.param:
            self.param["alpha"] = 0
            logging.warning("Alpha not precised, set to 0.")

        if not "q1" in self.param:
            if "q0" in self.param:
                self.param["Q"]= [self.param["q0"],self.param["q0"]]
                logging.warning("q1 not precised, setting it to q0.")
            else:
                self.param["Q"]= [0,1]
                logging.warning("q0 and q1 not precised, setting them to (O,1).")
        else:
            if "q0" in self.param:
                self.param["Q"]= [self.param["q0"],self.param["q1"]]
            else:
                self.param["Q"]= [self.param["q1"],self.param["q1"]]
                logging.warning("q0 not precised, setting it to q1.")


    def step(self):
        self.global_proportions = [sum(self.population.genotype)/float(self.population.N),
                                   sum(self.population.phenotype)/float(self.population.N)]
        ToyModel.step(self)

    def phenotype_heredity(self,phenotype,genotype):
        """Return the phenotype of the child cell given the one of the parent.
        
        :param phenotype: Phenotype of the parent. 
        :type phenotype: bool
        :param genotype: genotype of the parent. 
        :type genotype: bool
        :return: (bool) - Phenotype of the child. 
        """
        # Phenotipic heridity
        if random.random() < self.param["alpha"]:
            return phenotype
        # Switch probability
        else: 
            if random.random() < self.param["Q"][genotype]:
                return 1 
            else: 
                return 0

# Name of the model's Class (Required for import in main program)
model_class = ToyEpigenetic

