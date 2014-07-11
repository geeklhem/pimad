#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""

# Import built-in modules
import numpy as np
import copy
import logging

# Import custom modules
import pimad.population as population

class Model(object):
    """A generic class that contains a model
    
    You need to subclass this in the folder models to implement your
    own models.

    Attributes:
        population (popualtion.Population): Population object. 
        b (float): Benefits coefficient.
        c (float): Cost coefficient.
        param (dict): Model parameters.
        traces (list): A list of dict, an entry of the list by generation,
            an entry of the dict by tracked value.
        tracked_values (list):
    """
    
    def __init__(self,param,tracked_values=[]):
        """Model object constructor
        
        Args: 
            param (dict): Parameters of the model. Must contain at
                least N, T, ip (for population.Population initialisation)
                and c et b (cost and benfits).
            tracked_values (list): Values to recored.
        """

        self.model_name = "Generic model"

        # Parameters can be accessed by self.p["name"]
        self.p = param


        required_param = [("n","Number of patches."),
                          ("T","Patch size."),
                          ("ip","Initial proportion of mutants.")]
        for p in required_param:
            if p[0] not in self.p:
                raise ValueError("Missing parameter: {0[0]} ({0[1]})".format(p))
            
        # Create a "Population" object with parameters given by the param dict.
        self.population = population.Population(n=param["n"],
                                                T=param["T"],
                                                ip=param["ip"])
        
                                    

        # Creating a tracking list of dict with an entry by generation.
        self.traces = []
        self.tracked = tracked_values
        
    def step(self):
        """Runs one generation of the model
        
        Must be overrided by the class herited from model.
        Called by :class:`Population`.play at each generation """
        pass

    
    '''    def equilibrium(self,condition,nb_gen=10):
        """Play until the equilibrium
        
        Args: 
            condition (float): The halting criterion is:
                P(T) - 0.5(P(T-1)+P(T-2)) < N/condtition 
            nb_gen (int): Number of generation the criterion must be
            fullfilled for the simulation to stop.

        """
        condition = float(condition)
        logging.info(("Playing until equilibrium (Criterion limit" 
                      ": {0} for 10 generations)"
                      "").format(self.population.N/condition))

        #Create a new trace dict with a list by tracked values.
        self.traces.append({})
        for t in self.tracked:
            self.traces[-1][t] = []

        coef = 100
        g = 0
        criterion = [0,0,0]
        c = 0

        #Generation loop
        while c < 10:
            self.step()
            
            # Compute halting cirterion.
            criterion[2] =  criterion[1] #T-2
            criterion[1] =  criterion[0] #T-1
            criterion[0] =  sum(self.population.proportions[:,1]) #T
            coef =  math.fabs(criterion[0]-math.fabs(criterion[1]+criterion[2])/2)
            if coef < self.population.N/condition and g > 10:
                c += 1
            logging.debug("{0} | Halting criterion : {1} [{2}/10]".format(g+1,coef,c))


            # Add the values of tracked variable to the trace.
            for t in self.tracked:
                self.traces[-1][t].append(copy.copy(reduce(getattr,t.split("."),self)))
            
            g +=1'''
        
    
    def play(self,nb_generations):
        """Initialisation and call of the main loop.

        Args:
            nb_generation (int): Number of generation to play.
        """

        logging.info("Playing for {0} generations".format(nb_generations))

        #Create a new trace dict with a list by tracked values.
        self.traces.append({})
        for t in self.tracked:
            self.traces[-1][t] = [0]*nb_generations

        #Generation loop
        for g in range(nb_generations):
            logging.info("{0}/{1}".format(g+1,nb_generations))
            self.step()
            # Add the values of tracked variable to the trace.
            for t in self.tracked:
                self.traces[-1][t][g] = copy.copy(reduce(getattr,t.split("."),self))

    def __str__(self):
        s = "{0}.\n".format(self.model_name)
        s += "Benefit b =  {0}, cost c = {1}".format(self.b,self.c)
        return s

    def __repr__(self):
        return "{0}".format(self.model_name)

