#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Class to represent poulations data."""
import numpy
import component as comp
import types
import population

class Model:
    """ A generic class that contains a model

:param fcts: modelisation methods to use.
:type fcts: dict

"""
    
    def __init__(self, fcts,param):
        """ Model constructor"""
        reduce(getattr,"test.attach".split("."),comp)
        self.attach = types.MethodType(reduce(getattr,fcts["attach"].split("."),comp),self)
        self.birthanddeath = types.MethodType(reduce(getattr,fcts["birthanddeath"].split("."),comp),self)
        self.fpayoff = types.MethodType(reduce(getattr,fcts["fpayoff"].split("."),comp),self)
        self.dispersion = types.MethodType(reduce(getattr,fcts["dispersion"].split("."), comp),self)
        self.initialisation = types.MethodType(reduce(getattr,fcts["initialisation"].split("."),comp),self)

        self.pop = population.Population(param["N"],param["T"],1)
        self.b = param["b"]
        self.c = param["c"]
        self.param = param

    def step(self):
        self.dispersion()
        self.attach()
        for n,i in enumerate(self.pop.phenotype):
            self.pop.payoff[n] = self.fpayoff(n)
        self.birthanddeath()

    def play(self,nb_generations):
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


if __name__ == "__main__":
    # Test code
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

