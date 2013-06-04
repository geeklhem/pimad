#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Orso's functions"""

import math
import random
from random import randint
from random import shuffle


def initialize(self):
	for i in range(self.param["N"]):
		self.population.patch_du[i] = int(i/self.param["T"])
		self.population.genotype[i] = randint(0,1)			#random choice between genotypes 0 and 1
		self.population.phenotype[i] = self.population.genotype[i]
		#self.population.repartition[i] = 0				#not necessary (see the population constructor)
		#self.population.payoff[i] = 0					#not necessary (see the population constructor)



def attach(self):
	for i in range(self.param["NPATCH"]):
		if ((i != self.param["NPATCH"]-1) | ((self.param["N"]%self.param["T"]) == 0)):
			for j in range(1, self.param["T"]):
				if random.random() <= math.sqrt((self.param["ps"]**(self.population.phenotype[i*self.param["T"]]+self.population.phenotype[(i*self.param["T"])+j]))*(self.param["pa"]**(2-self.population.phenotype[i*self.param["T"]]-self.population.phenotype[(i*self.param["T"])+j]))):
					self.population.repartition[i*self.param["T"]] = 1
					self.population.repartition[(i*self.param["T"])+j] = 1
		else:
			for j in range(1, (self.param["N"]%self.param["T"])):
				if random.random() <= math.sqrt((self.param["ps"]**(self.population.phenotype[i*self.param["T"]]+self.population.phenotype[(i*self.param["T"])+j]))*(self.param["pa"]**(2-self.population.phenotype[i*self.param["T"]]-self.population.phenotype[(i*self.param["T"])+j]))):
					self.population.repartition[i*self.param["T"]] = 1
					self.population.repartition[(i*self.param["T"])+j] = 1
	self.patch = comp.functions-o.evaluator(self)	#creates an object patch calling the "evaluator" function



#def evaluator(N, T, NPATCH, patch_du, phenotype, repartition):
def evaluator(self):
	patch = []
	subpatch = []
	phenaux = []
	phenrepaux = []
	repaux = []
	for j in range(param["N"]):
		for i in range(param["NPATCH"]):
			if self.population.patch_du[j] == i:
				if ((i != param["NPATCH"]-1) | ((param["N"]%param["T"]) == 0)):
					for l in range(param["T"]):
						phenaux.append(self.population.phenotype[(i*param["T"])+l])
						phenrepaux.append(self.population.phenotype[(i*param["T"])+l]*self.population.repartition[(i*param["T"])+l])
						repaux.append(self.population.repartition[(i*param["T"])+l])
				else:
					for l in range(param["N"]%param["T"]):
						phenaux.append(self.population.phenotype[(i*param["T"])+l])
						phenrepaux.append(self.population.phenotype[(i*param["T"])+l]*self.population.repartition[(i*param["T"])+l])
						repaux.append(self.population.repartition[(i*param["T"])+l])
		if ((j%param["T"]) == 0):
			subpatch.append(phenrepaux.count(1))				#Field 1: number of socials among the ingroups in the patch i
			subpatch.append(repaux.count(1))				#Field 2: total number of ingroups in the patch i
			subpatch.append(phenaux.count(1) - phenrepaux.count(1))		#Field 3: number of socials among the loners in patch i	
			subpatch.append(repaux.count(0))				#Field 4: total number of loners in the patch i
			patch.append(subpatch[:])
		while phenaux: phenaux.pop()
		while phenrepaux: phenrepaux.pop()
		while repaux: repaux.pop()
		while subpatch: subpatch.pop()
	return patch



#def fpay(patch, patch_du, repartition, phenotype, index, benefit, cost):
def fpay(self, patch, index):
	if patch[self.population.patch_du[index]][1] == 0:
		return round(param["b"]*(1.0*patch[self.population.patch_du[index]][0])*self.population.repartition[index]-(1.0*param["c"]*self.population.phenotype[index]), 3)
	else:
		return round(param["b"]*(1.0*patch[self.population.patch_du[index]][0]/patch[patch_du[index]][1])*self.population.repartition[index]-(1.0*param["c"]*self.population.phenotype[index]), 3)



def normalize(self):
	minimum = min(self.population.payoff)
	maximum = max(self.population.payoff)
	for i in range(param["N"]):
		self.population.payoff[i] -= minimum
		if ((minimum==0) & (maximum==0)):
			self.population.payoff[i] = 0
		else:
			self.population.payoff[i] = self.population.payoff[i]/(maximum-minimum)



#def localbirthdeath(N, T, NPATCH, MU, patch_du, genotype, phenotype, repartition, payoff):
def localbirthdeath(self)):

	nnew = []
	for i in range(param["NPATCH"]-1, -1, -1):

		cont = 0

		if ((i != param["NPATCH"]-1) | ((param["N"]%param["T"]) == 0)):
			for j in range(param["T"]-1, -1, -1):
				alea = random.random()
				if (alea <= self.population.payoff[(i*param["T"])+j]):
					cont += 1
					if (random.random() <= param["mu"]):
						mutation = 1
					else:
						mutation = 0
					self.population.patch_du.insert((i+1)*param["T"], self.population.patch_du[(i*param["T"])+j])
					self.population.genotype.insert((i+1)*param["T"], (self.population.genotype[(i*param["T"])+j]+mutation)%2)
					self.population.phenotype.insert((i+1)*param["T"], self.population.genotype[(i+1)*param["T"]])
					self.population.repartition.insert((i+1)*param["T"], 0)
					self.population.payoff.insert(((i+1)*param["T"]), 222)
			nnew.insert(0, cont)

		else:
			for j in range((param["N"]%param["T"])-1, -1, -1):
				alea = random.random()
				if (alea <= self.population.payoff[(i*param["T"])+j]):
					cont += 1
					if (random.random() <= param["mu"]):
						mutation = 1
					else:
						mutation = 0
					self.population.patch_du.append(self.population.patch_du[(i*param["T"])+j])		
					self.population.genotype.append((self.population.genotype[(i*param["T"])+j]+mutation)%2)
					self.population.phenotype.append(self.population.genotype[-1])
					self.population.repartition.append(0)
					self.population.payoff.append(333)
			nnew.insert(0, cont)

	aleaindex = set()
	for i in range(param["NPATCH"]):
		
		if ((i != param["NPATCH"]-1) | ((param["N"]%param["T"]) == 0)):
			while len(aleaindex) < sum(nnew[:i+1]):
				aleaindex.add(random.randint((i*param["T"])+sum(nnew[:i]), ((i+1)*param["T"])-1+sum(nnew[:i+1])))
		else:
			while len(aleaindex) < sum(nnew):
				aleaindex.add(random.randint((i*param["T"])+sum(nnew[:i]), param["N"]+sum(nnew)))

	new_patch_du = [v for i, v in enumerate(self.patch_du) if i not in aleaindex]
	while self.patch_du: self.patch_du.pop()
	self.patch_du[:] = new_patch_du
	while new_patch_du: new_patch_du.pop()

	new_genotype = [v for i, v in enumerate(self.genotype) if i not in aleaindex]
	while self.genotype:	self.genotype.pop()
	self.genotype[:] = new_genotype
	while new_genotype: new_genotype.pop()

	new_phenotype = [v for i, v in enumerate(self.phenotype) if i not in aleaindex]
	while self.phenotype: self.phenotype.pop()
	self.phenotype[:] = new_phenotype
	while new_phenotype: new_phenotype.pop()

	new_repartition = [v for i, v in enumerate(self.repartition) if i not in aleaindex]
	while self.repartition: self.repartition.pop()
	self.repartition[:] = new_repartition
	while new_repartition: new_repartition.pop()

	new_payoff = [v for i, v in enumerate(self.payoff) if i not in aleaindex]
	while self.payoff: self.payoff.pop()
	self.payoff[:] = new_payoff
	while new_payoff: new_payoff.pop()



def disperse(self):

	genotype_shuf = []; phenotype_shuf = [];		#here, if desired, one can shuffle all the attributes of the population class
	index_shuf = range(len(self.population.genotype))
	shuffle(index_shuf)

	for i in index_shuf:
	    genotype_shuf.append(self.population.genotype[i])
	    phenotype_shuf.append(self.population.phenotype[i])

	self.population.genotype[:] = genotype_shuf
	self.population.phenotype[:] = phenotype_shuf
	
