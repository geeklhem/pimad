#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Model traces containers"""

import copy
import cPickle as pickle
import numpy as np


class Trace:
    """ A generic model trace container 
    
    :param: The "traces" attribute of the model to set.
    :type: list"""
    def __init__(self,model):
        """Constructor"""
        self.traces = copy.copy(model.traces)
        self.p = copy.copy(model.param)
        self._grpsize_density = np.zeros((1,1))
        self._grpsize_density_social = np.zeros((1,1))
        try :
            self.grpsize = self._compute_grpsize()
        except:
            print("Group information unavailable")
        else:
            self.grpsize_density = [(i * n)/self.p["N"] for i,n in enumerate(self.grpsize)]

    def _compute_grpsize(self,tracenb=0):
        """Return an array with A(k,g) = number of k-sized groups at generation g"""  
        trace = self.traces[tracenb]["population.proportions"]
        generations=len(trace)
        grps_size = np.zeros((self.p['T']+1,generations))

        for ng,g in enumerate(trace):
            #for a generation
            for i in g[:,3]:
                #alone individulals
                grps_size[1,ng] += i

            for i in g[:,1]:
                #grouped individuals
                grps_size[i,ng] += 1
        return grps_size
    

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
#    save_trace(test,"test2.data")

    
