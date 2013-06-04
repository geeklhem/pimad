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
    """Group formation
    Called on"""
    print("Fonction attach in module :  {0}".format(__name__))



def payoff(self,n):
    return(0)


def bad(self):
    print("Fonction bad in module :  {0}".format(__name__))


