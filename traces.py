#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Model traces containers"""

import copy
import cPickle as pickle
import numpy as np


class Trace:
    """ A generic model trace container 
    
    :param: The model instance.
    :type: Model"""
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
            self.covPrice= self._compute_covPrice()

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
    
    def _compute_covPrice(self,tracenb=0):
        trace = self.traces[tracenb]["population.proportions"]
        generations=len(trace)
        zk = np.zeros((self.p['T'],generations),dtype=float)
        wk = np.zeros((self.p['T'],generations),dtype=float)
        for ng,g in enumerate(trace):
            ## Compute number of socials in each class :
            for i in g[:,2]: #alone individulals
                zk[1,ng] += i
            for ni,i in enumerate(g[:,0]): #grouped individuals
                zk[g[ni,1],ng] += i
            ## Normalize it :
            zk[:,ng] = [j/(nj*self.grpsize[nj,ng]) if self.grpsize[nj,ng] and nj else 0  for nj,j in enumerate(zk[:,ng])]  
            
            #compute wk the group-level fitness
            if ng < generations-1:
                for nw in range(self.p["T"]):
                    if self.grpsize[nw,ng]:
                        wk[nw,ng] = self.grpsize[nw,ng+1]/self.grpsize[nw,ng]
                    else:
                        #Case where this size class didn't exist at the previous step.
                        wk[nw,ng] = 0
                    
                        

        
        
        cov_zw = np.zeros(generations,dtype=float)
        for g in range(generations):
            cov_zw[g] = np.cov(zk[:,g],wk[:,g],1)[0,1]
        return cov_zw
        

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
    param = {"N":10000,
             "T":50,
             "ip":0.5,
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
    #save_trace(test,"test2.data")

    
