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
		self.population.genotype.append(randint(0,1))
		self.population.phenotype.append(genotype[i])
		self.population.repartition.append(0)
		self.population.payoff.append(0)



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



def fpay(patch, patch_du, repartition, phenotype, index, benefit, cost):
	if patch[patch_du[index]][1] == 0:
		return round(benefit*(1.0*patch[patch_du[index]][0])*repartition[index]-(1.0*cost*phenotype[index]), 3)
	else:
		return round(benefit*(1.0*patch[patch_du[index]][0]/patch[patch_du[index]][1])*repartition[index]-(1.0*cost*phenotype[index]), 3)



def evaluator(N, T, NPATCH, patch_du, phenotype, repartition):
	patch = []
	subpatch = []
	phenaux = []
	phenrepaux = []
	repaux = []
	for j in range(N):
		for i in range(NPATCH):
			if patch_du[j] == i:
				if ((i != NPATCH-1) | ((N%T) == 0)):
					for l in range(T):
						phenaux.append(phenotype[(i*T)+l])
						phenrepaux.append(phenotype[(i*T)+l]*repartition[(i*T)+l])
						repaux.append(repartition[(i*T)+l])
				else:
					for l in range(N%T):
						phenaux.append(phenotype[(i*T)+l])
						phenrepaux.append(phenotype[(i*T)+l]*repartition[(i*T)+l])
						repaux.append(repartition[(i*T)+l])
		if ((j%T) == 0):
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



def normalize(N, T, payoff):
	minimum = min(payoff)
	maximum = max(payoff)
	for i in range(N):
		payoff[i] -= minimum
		if ((minimum==0) & (maximum==0)):
			payoff[i] = 0
		else:
			payoff[i] = payoff[i]/(maximum-minimum)



def normalizelocal(N, T, NPATCH, payoff):
	payoffaux = []
	for i in range(NPATCH):
		if ((i != NPATCH-1) | ((N%T) == 0)):
			payoffaux = [payoff[s] for s in range((i*T), (i*T)+T)]
			for j in range(T):
				payoff[(i*T)+j] -= min(payoffaux)
				if ((min(payoffaux)==0) & (max(payoffaux)==0)):
					payoff[(i*T)+j] = 0
				else:
					payoff[(i*T)+j] = payoff[(i*T)+j]/(max(payoffaux)-min(payoffaux))
		else:
			payoffaux = [payoff[s] for s in range((i*T), (i*T)+(N%T))]
			for j in range(N%T):
				payoff[(i*T)+j] -= min(payoffaux)
				if ((min(payoffaux)==0) & (max(payoffaux)==0)):
					payoff[(i*T)+j] = 0
				else:
					payoff[(i*T)+j] = payoff[(i*T)+j]/(max(payoffaux)-min(payoffaux))
	while payoffaux: payoffaux.pop()



def birth(N, MU, patch_du, genotype, phenotype, repartition, payoff):
	NNEW=0
	for i in range(N):
		alea = random.random()
		if (alea <= payoff[i]):
			NNEW += 1
			if (random.random() <= MU):
				mutation = 1
			else:
				mutation = 0
			patch_du.append(patch_du[i])
			genotype.append((genotype[i]+mutation)%2)
			phenotype.append(genotype[-1])
			repartition.append(0)
			payoff.append(0)
	return NNEW



def death(N, D, patch_du, genotype, phenotype, repartition, payoff):
	NDEAD=0
	for i in range(N-1, -1, -1):
		if (random.random() <= D):
			del patch_du[i]
			del genotype[i]
			del phenotype[i]
			del repartition[i]
			del payoff[i]
			NDEAD += 1
	return NDEAD;



def localbirthdeath(N, T, NPATCH, MU, patch_du, genotype, phenotype, repartition, payoff):

	nnew = []
	for i in range(NPATCH-1, -1, -1):

		cont = 0

		if ((i != NPATCH-1) | ((N%T) == 0)):
			for j in range(T-1, -1, -1):
				alea = random.random()
				if (alea <= payoff[(i*T)+j]):
					cont += 1
					if (random.random() <= MU):
						mutation = 1
					else:
						mutation = 0
					patch_du.insert((i+1)*T, patch_du[(i*T)+j])
					genotype.insert((i+1)*T, (genotype[(i*T)+j]+mutation)%2)
					phenotype.insert((i+1)*T, genotype[(i+1)*T])
					repartition.insert((i+1)*T, 0)
					payoff.insert(((i+1)*T), 222)
			nnew.insert(0, cont)

		else:
			for j in range((N%T)-1, -1, -1):
				alea = random.random()
				if (alea <= payoff[(i*T)+j]):
					cont += 1
					if (random.random() <= MU):
						mutation = 1
					else:
						mutation = 0
					patch_du.append(patch_du[(i*T)+j])		
					genotype.append((genotype[(i*T)+j]+mutation)%2)
					phenotype.append(genotype[-1])
					repartition.append(0)
					payoff.append(333)
			nnew.insert(0, cont)

	aleaindex = set()
	for i in range(NPATCH):
		
		if ((i != NPATCH-1) | ((N%T) == 0)):
			while len(aleaindex) < sum(nnew[:i+1]):
				aleaindex.add(random.randint((i*T)+sum(nnew[:i]), ((i+1)*T)-1+sum(nnew[:i+1])))
		else:
			while len(aleaindex) < sum(nnew):
				aleaindex.add(random.randint((i*T)+sum(nnew[:i]), N+sum(nnew)))

	new_patch_du = [v for i, v in enumerate(patch_du) if i not in aleaindex]
	while patch_du:	patch_du.pop()
	patch_du[:] = new_patch_du
	while new_patch_du: new_patch_du.pop()

	new_genotype = [v for i, v in enumerate(genotype) if i not in aleaindex]
	while genotype:	genotype.pop()
	genotype[:] = new_genotype
	while new_genotype: new_genotype.pop()

	new_phenotype = [v for i, v in enumerate(phenotype) if i not in aleaindex]
	while phenotype: phenotype.pop()
	phenotype[:] = new_phenotype
	while new_phenotype: new_phenotype.pop()

	new_repartition = [v for i, v in enumerate(repartition) if i not in aleaindex]
	while repartition: repartition.pop()
	repartition[:] = new_repartition
	while new_repartition: new_repartition.pop()

	new_payoff = [v for i, v in enumerate(payoff) if i not in aleaindex]
	while payoff: payoff.pop()
	payoff[:] = new_payoff
	while new_payoff: new_payoff.pop()



def disperse(genotype, phenotype):

	genotype_shuf = []; phenotype_shuf = [];
	index_shuf = range(len(genotype))
	shuffle(index_shuf)

	for i in index_shuf:
	    genotype_shuf.append(genotype[i])
	    phenotype_shuf.append(phenotype[i])

	genotype[:] = genotype_shuf
	phenotype[:] = phenotype_shuf
	
