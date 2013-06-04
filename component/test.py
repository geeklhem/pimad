#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Test components"""

def attach(self):
    print("Fontion attach in module :  {}".format(__name__))


def bad(self):
    print("Fontion bad in module :  {}".format(__name__))


def payoff(self,n):
    return(0)

def dispersion(self):
    print("Fontion dispersion in module :  {}".format(__name__))

def init(self):
    print("Fontion init in module :  {}".format(__name__))

