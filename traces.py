#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Model traces containers"""

import copy
import cPickle as pickle

class Trace:
    """ A generic model trace container 
    
    :param: The "traces" attribute of the model to set.
    :type: list"""
    def __init__(self,model):
        """Constructor"""
        self.traces = copy.copy(model.traces)


def save_trace(trace,name):
        with open(name, 'wb') as fichier:
            pickler = pickle.Pickler(fichier)
            pickler.dump(trace)
    
def load_trace(name):
        with open(name, 'rb') as fichier:
            unpickler = pickle.Unpickler(fichier)
            return unpickler.load()

if __name__ == "__main__":
    import math
    from toymodel import ToyModel
    param = {"N":1000,
             "T":100,
             "b":20,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.8*0.3),
             "mu":0.01}

    tracked_values = ["population.proportions"]

    a = ToyModel(param, tracked_values)

    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.population)
    print("\n Run:")
    a.play(10)
    test = Trace(a)
    save_trace(test,"test2.data")

    
