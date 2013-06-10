#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""
# Import built-in modules
import numpy
import copy
import math

# Import custom modules
import population

class Model:
    """ A generic class that contains a model

    :param param: Parameters of the model. Must contain at least N, T, ip (for :class:`Population` initialisation) and c et b (cost and benfits).
    :param tracked_values: Values to track at each re 
    :type param: dict
    :type tracked_values: list

    **Example:**::

        param = {"N":100000,
                 "T":1000,
                 "ip":0.5,
                 "b":3,
                 "c":1,
                 "ps":0.3,
                 "pa":0.1,
                 "mu":0.001}

"""
    
    def __init__(self,param,tracked_values=[]):
        """ Model object constructor"""
        self.model_name = "Generic model"

        # Create a "Population" object with parameters given by the param dict.
        self.population = population.Population(param["N"],param["T"],param["ip"])
        
        # b and c are copied into the model namespace in order to access them with self.b 
        self.b = param["b"]
        self.c = param["c"]
        # Other parameters can be accessed by self.param["name"]
        self.param = param

        # Creating a tracking dict. with an entry by tracked value.
        self.traces = []
        self.tracked = tracked_values
        
    def step(self):
        """Runs one generation of the model
        
        Must be overrided by the class herited from model.
        Called by :class:`Population`.play at each generation """
        pass

    def equilibrium(self):
        """play until the equilibrium"""
        print("Playing until equilibrium")

        #Create a new trace dict with a list by tracked values.
        self.traces.append({})
        for t in self.tracked:
            self.traces[-1][t] = []

        coef = 100
        g = 0
        criterion = [111,222,333]

        #Generation loop
        while coef > 0.0001 or g < 3:
            self.step()
            
            # Compute halting cirterion.
            criterion[2] =  criterion[1] #T+2
            criterion[1] =  criterion[0]#T+1
            criterion[0] =  sum(self.population.proportions[:,1]) #T
            if g > 2:
                try:
                    coef = math.fabs( math.log((math.fabs(criterion[0]-criterion[1]))/(math.fabs(criterion[2]-criterion[1])),10))
                except:
                    coef = 0

            print("{0} | Halting criterion : {1}".format(g+1,coef))

            
            

            # Add the values of tracked variable to the trace.
            for t in self.tracked:
                self.traces[-1][t].append(copy.copy(reduce(getattr,t.split("."),self)))
            
            g +=1
        
    
    def play(self,nb_generations):
        """Initialisation and call of the main loop"""
        print("Playing for {0} generations".format(nb_generations))

        #Create a new trace dict with a list by tracked values.
        self.traces.append({})
        for t in self.tracked:
            self.traces[-1][t] = [0]*nb_generations

        #Generation loop
        for g in range(nb_generations):
            print("{0}/{1}".format(g+1,nb_generations))
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

###############
## Test code ##
###############
# It will only run if the file is directly executed (>>python model.py)
if __name__ == "__main__":

    param = {"N":10000,
             "T":100,
             "b":3,
             "c":1,
             "ip":0.5,
             "ps":0.3,
             "pa":0.1,
             "mu":0.001}

    tracked_values = ["population.N"]

    a = Model(param, tracked_values)

    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.population)
    print("\n Run:")
    #a.play(5)
    a.equilibrium()
    print(a.traces)
