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
    
    def __init__(self, fcts):
        """ Model constructor"""
        self.attach = types.MethodType(getattr(comp.attach,fcts["attach"]),self)
        self.birthanddeath = types.MethodType(getattr(comp.birthanddeath,fcts["birthanddeath"]),self)
        self.fpayoff = types.MethodType(getattr(comp.fpayoff,fcts["fpayoff"]),self)
        self.dispersion = types.MethodType(getattr(comp.dispersion,fcts["dispersion"]),self)
        self.initialisation = types.MethodType(getattr(comp.initialisation,fcts["initialisation"]),self)

        self.pop = population.Population(100,10,0.1)

    def step(self):
        self.dispersion()
        self.attach()
        for n,i in enumerate(self.pop.phenotype):
            self.pop.payoff[n] = self.fpayoff(n)
        self.birthanddeath()

    def __str__(self):
        s = "Generic model."
        return s

    def __repr__(self):
        return "Generic model."


if __name__ == "__main__":
    # Test code
    fcts = {"attach": 'test',
            "birthanddeath":"test",
            "fpayoff":"test",
            "dispersion":"test",
            "initialisation":"test"}

    a = Model(fcts)
    print(a)
    print(a.pop)
    a.step()
