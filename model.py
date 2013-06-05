#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""
# Import built-in modules
import numpy

# Import custom modules
import population

class Model:
    """ A generic class that contains a model

    :param param: Parameters of the model. Must contain at least N, T (for :class:`Population` initialisation) and c et b (cost and benfits).
    :param tracked_values: Values to track at each re 
    :type param: dict
    :type tracked_values: list

    **Example:**::

        param = {"N":100000,
                 "T":1000,
                 "b":3,
                 "c":1,
                 "ps":0.3,
                 "pa":0.1,
                 "mu":0.001}

"""
    
    def __init__(self,param,tracked_values=[]):
        """ Model object constructor"""
        # Create a "Population" object with parameters given by the param dict.
        self.population = population.Population(param["N"],param["T"])
        
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


    def play(self,nb_generations):
        """Initialisation and call of the main loop"""
        print("Playing for {0} generations".format(nb_generations))

        #Create a new trace dict with a list by tracked values.
        self.traces.append({})
        for t in self.tracked:
            self.traces[-1][t] = []

        #Generation loop
        for g in range(nb_generations):
            print("{0}/{1}".format(g+1,nb_generations))
            self.step()
            # Add the values of tracked variable to the trace.
            for t in self.tracked:
                self.traces[-1][t].append(reduce(getattr,t.split("."),self))
    

    def __str__(self):
        s = "Generic model.\n"
        s += "Benefit b =  {0}, cost c = {1}".format(self.b,self.c)
        return s

    def __repr__(self):
        return "Generic model."

###############
## Test code ##
###############
# It will only run if the file is directly executed (>>python model.py)
if __name__ == "__main__":

    param = {"N":100000,
             "T":1000,
             "b":3,
             "c":1,
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
    a.play(5)
    print(a.traces)
