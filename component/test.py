#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Test components"""

def attach(self):
    print("Fonction attach in module :  {0}".format(__name__))


def bad(self):
    print("Fonction bad in module :  {0}".format(__name__))


def payoff(self,n):
    return(0)

def dispersion(self):
    print("Fonction dispersion in module :  {0}".format(__name__))

def init(self):
    print("Fonction init in module :  {0}".format(__name__))

