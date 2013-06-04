#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Test components

A mock set of modeling methods.

**Order :**

1. intitialise

*Generation loop :*

1. disperse
2. attach
3. loop on payoff
4. life and death


**To use it** ::

    fcts = {"attach": 'test.attach',
            "birthanddeath":"test.bad",
            "fpayoff":"test.payoff",
            "dispersion":"test.dispersion",
            "initialisation":"test.init"}

"""

def init(self):
    print("Fonction init in module :  {0}".format(__name__))


def dispersion(self):
    print("Fonction dispersion in module :  {0}".format(__name__))



def attach(self):
    """Group formation. Set the population.repartition array.
    Called on every generation loop."""
    print("Fonction attach in module :  {0}".format(__name__))



def payoff(self,n):
    """ Returns the payoff of individual n.
    Called every generation loop for each individual."""
    return(0)


def bad(self):
    """ Brith and death function.
    Called every generation loop.
    """
    print("Fonction bad in module :  {0}".format(__name__))


