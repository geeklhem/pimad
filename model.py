#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""
# Import built-in modules
import numpy
import types

# Import custom modules
import population
import component as comp #Load all files in /component folders as "comp.filename" 


class Model:
    """ A generic class that contains a model

:param fcts: modelisation methods to use.
:param fcts: Parameters of the model. Must contain at least N, T (for :class:`Population` initialisation) and c et b (cost and benfits). 
:type fcts: dict
:type param: dict

**Exemple of dicts**::

    fcts = {"attach": 'test.attach',
            "birthanddeath":"test.bad",
            "fpayoff":"test.payoff",
            "dispersion":"test.dispersion",
            "initialisation":"test.init"}

    param = {"N":100000,
             "T":1000,
             "b":3,
             "c":1,
             "ps":0.3,
             "pa":0.1,
             "mu":0.001}

"""
    
    def __init__(self, fcts,param):
        """ Model object constructor"""
        
        # Attach the modeling methods specified in the fcts dict to the model object. 
        self.attach = types.MethodType(reduce(getattr,fcts["attach"].split("."),comp),self)
        self.birthanddeath = types.MethodType(reduce(getattr,fcts["birthanddeath"].split("."),comp),self)
        self.fpayoff = types.MethodType(reduce(getattr,fcts["fpayoff"].split("."),comp),self)
        self.dispersion = types.MethodType(reduce(getattr,fcts["dispersion"].split("."), comp),self)
        self.initialisation = types.MethodType(reduce(getattr,fcts["initialisation"].split("."),comp),self)

        # Create a "Population" object with parameters given by the param dict. (and Z=1)
        self.pop = population.Population(param["N"],param["T"],1)
        
        # b and c are copied into the model namespace in order to access them with self.b 
        self.b = param["b"]
        self.c = param["c"]
        # Other parameters can be accessed by self.param["name"]
        self.param = param

    def step(self):
        """Runs one generation of the model

Use :class:`Population`.play to run it for more generations"""
        self.dispersion()
        self.attach()
        for n,i in enumerate(self.pop.phenotype):
            self.pop.payoff[n] = self.fpayoff(n)
        self.birthanddeath()

    def play(self,nb_generations):
        """Initialisation and call of the main loop"""
        print("Playing for {0} generations".format(nb_generations))
        self.initialisation()
        for g in range(nb_generations):
            print("{0}/{1}".format(g+1,nb_generations))
            self.step()
            

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
    fcts = {"attach": 'test.attach',
            "birthanddeath":"test.bad",
            "fpayoff":"test.payoff",
            "dispersion":"test.dispersion",
            "initialisation":"test.init"}

    param = {"N":100000,
             "T":1000,
             "b":3,
             "c":1,
             "ps":0.3,
             "pa":0.1,
             "mu":0.001}

    a = Model(fcts,param)
    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.pop)
    print("\n Run:")
    a.play(5)

