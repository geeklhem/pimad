#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""The toy model as defined by Garcia & De Monte 2012."""

import numpy
import random

import model
import math

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Toy model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ToyModel(model.Model):
    """A toy model of group formation by differential attachment. [Garcia & De Monte 2012]


    Needs the following parameters in *model.param* dict : 
    
    =====  =====================================================================
    Name   Parameter
    =====  =====================================================================
    b      Benefits in the pgg (int)
    c      Linear cost of altruism (int)
    ps     Attachment probability of two social individuals  (float).
    pa     Attachment probability of two asocial individuals (float).
    pas    Attachment probability of an social and an asocial individual (float).
    mu     Mutation rate (float).
    =====  =====================================================================

    
    """

    def __init__(self,param,tracked_values=[]):
        """Constructeur"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "Toymodel [Garcia & De Monte 2012]"

    def step(self):
        """Runs one generation of the model
    
        Called by :class:`Population`.play at each generation """
        
        self.dispersion()
        self.aggregation()
        self.payoff()
        self.demographic()
        
        

    def aggregation(self):
        """ Define the aggregation process.
        
        =========  ============================
        **Read**   self.population.phenotype.
        **Write**  self.population.repartition, 
                   self.population.proportions.
        =========  ============================

        .. note ::
           By line in self.population.proportions:
        
           0. Social individual in the group.
           1. Individuals in the group.
           2. Social individuals alone.
           3. Individuals alone.
  
        """
        
        ## For each patch
        for patch in range(self.population.Npatch):
            # Here patch size is assumed to always be T.
            patch_begin = patch * self.population.T
            patch_end = patch_begin + self.population.T 

            ## Choose a random recruiter and compute the probabilities to attach.
            recruiter_index = random.randint(patch_begin,patch_end-1)
            
            if self.population.phenotype[recruiter_index]:
                # The recruiter is social.
                proba = (self.param["pas"],self.param["ps"])
            else: 
                # The recruiter is asocial.
                proba = (self.param["pa"],self.param["pas"])

            ## Loop on patch individuals and give them a chance to attach to the group.
            for n,i in enumerate(self.population.phenotype[patch_begin:patch_end]):
                if random.random() < proba[i]:
                    self.population.repartition[n+patch_begin] = 1
                    self.population.proportions[patch,0] += i #= 1 if social
                    self.population.proportions[patch,1] += 1
                else:
                    self.population.proportions[patch,2] += i #= 1 if social
                    self.population.proportions[patch,3] += 1
                       
            # The recruiter is always in the group. 
            if not self.population.repartition[recruiter_index]:
                self.population.repartition[recruiter_index] = True
                self.population.proportions[patch,0] += i #= 1 if social
                self.population.proportions[patch,1] += 1
                self.population.proportions[patch,2] -= i #= 1 if social
                self.population.proportions[patch,3] -= 1

    def payoff(self):
        """
        Compute the payoff for each patch and each combinaison of repartition and phenotype.
        
        =========  ============================
        **Read**   self.population.phenotype.
                   self.population.repartition, 
        **Write**  self.population.payoff.
        =========  ============================
        
        .. note ::
           By line in self.population.payoff:
        
           0. Payoff of social individual in a group
           1. Payoff of asocial individual in a group
           2. Payoff of social individual alone
           3. Payoff of asocial individual alone
        
        """
        ## For each patch
        for patch in range(self.population.Npatch):
            group_benefit = (self.b*self.population.proportions[patch,0])
            group_benefit /= self.population.proportions[patch,1]  
            
            # Payoff of social individual in a group
            self.population.payoff[patch,0] = group_benefit - self.c 
            # Payoff of asocial individual in a group
            self.population.payoff[patch,1] = group_benefit
            # Payoff of social individual alone
            self.population.payoff[patch,2] = - self.c # and not b-c 
            # Payoff of asocial individual alone
            self.population.payoff[patch,3] = 0 

            

    def demographic(self):
        """Global life, Death, Mutation, Heredity and genealogy processes
        
        =========  ============================
        **Read**   self.population.phenotype,
                   self.population.genotype,
                   self.population.repartition,
                   self.population.payoff.
        **Write**  self.population.phenotype,
                   self.population.genotype,
                   self.population.genealogy.
        =========  ============================
        """     
        
        newborn_genotype = []
        newborn_phenotype = []
        newborn_genealogy = []

        ## Normalize the payoff to give the fitness
        fitness = numpy.array(self.population.payoff, dtype=numpy.float)
        fitness -= numpy.min(fitness)
        fitness /= numpy.max(fitness)
        
        #fitness index for the couples of (phenotype, repartition).
        fitness_index = {(1,1):0, #social in group.
                         (0,1):1, #asocial in group.
                         (1,0):2, #social alone.
                         (0,0):3} #asocial alone.

        ## Each individual has a chance to reproduce once.
        for n,g in enumerate(self.population.genotype):
            p = self.population.phenotype[n] 
            r = self.population.repartition[n]
            patch = n/self.population.T
            if random.random()<fitness[patch,fitness_index[(p,r)]]:
                #The genotype is inherited or flipped if mutated.
                if random.random()<self.param["mu"]:
                    # Mutated : if g = 1, not g = 0 and if g = 0, not g = 1 
                    newborn_genotype.append(not g)
                else:
                    newborn_genotype.append(g)
                
                # Phenotype is inherited according to the rules of phenotype_heredity().
                newborn_phenotype.append(self.phenotype_heredity(p,g))
                
                # Genealogy is the index of the parent in the previous generation.
                newborn_genealogy.append(n)

        ## Death process : newborn are inserted in random position inside the new population, thus killing the one whose place they take.
        for i in range(len(newborn_genotype)):
            n = random.randint(0,self.population.N-1)
            self.population.phenotype[n] = newborn_phenotype[i]
            self.population.genotype[n]  = newborn_genotype[i]
            self.population.genealogy[n] = newborn_genealogy[i]
                                         
    def dispersion(self):
        """Global shuffling and reset population.arrays
        
        =========  ============================
        **Write**  self.population.phenotype,
                   self.population.genotype,
                   self.population.repartition,
                   self.population.genealogy,
                   self.population.payoff.
                   self.population.proportions.
        =========  ============================
        """ 

        ## Reset of the individuals population arrays
        self.population.repartition[:] = 0
        self.population.genealogy[:] = -1

        ## Flush the arrays patches.
        self.population.flush_patch_arrays()

        ## Shuffling the individuals ! 
        p = numpy.random.permutation(self.population.N)
        self.population.phenotype = self.population.phenotype[p] 
        self.population.genotype = self.population.genotype[p]

                   
    def phenotype_heredity(self,phenotype,genotype):
        """Return the phenotype of the child cell given the one of the parent.
        
        :param phenotype: Phenotype of the parent. 
        :type phenotype: bool
        :param genotype: genotype of the parent. 
        :type genotype: bool
        :return: (bool) - Phenotype of the child. 
        .. note ::
          Here it's an identity, this method should be overrided in a inherited model.
        """
        return genotype

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Epigenetic  toy model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ToyEpigenetic(ToyModel):
    """ [Orso 2013]
    
    A model with epigenetic heredity. 

    Needs the following supplementary parameters in *model.param* dict : 
    
    =====  =====================================================================
    Name   Parameter
    =====  =====================================================================
    alpha  Probability of direct phenotipic inheritance.
    q0     Probability for a genotype 0 individual to have a 1 phenotype*
    q1     Probability for a genotype 1 individual to have a 1 phenotype*
    =====  =====================================================================

    * If there is no direct phenotypic inheritance.


    .. note ::
           If alpha is not set in input, it's set to 0. (No direct phenotypical
       inheritance) 
           If only q0 or q1 is set in input, q1=q0
           If neither q0 nor q1 is set in input,  Q = [0,1] (direct genotypic
       inheritance without switch).

    Exemple:
    python experiment.py test -m ToyEpigenetic -p alpha=0.1,q0=0.5,q1=0.1
    """

    def __init__(self,param,tracked_values=[]):
        """Constructeur"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "ToyEpigenetic [Modified Toymodel]"
        
        # If parameters are not defined, set default values...
        if not "alpha" in self.param:
            self.param["alpha"] = 0
            print("[!] Warning : alpha not precised, set to 0.")

        if not "q1" in self.param:
            if "q0" in self.param:
                self.param["Q"]= [self.param["q0"],self.param["q0"]]
                print("[!] Warning : q1 not precised, setting it to q0.")
            else:
                self.param["Q"]= [0,1]
                print("[!] Warning : q0 and q1 not precised, setting them to (O,1).")
        else:
            if "q0" in self.param:
                self.param["Q"]= [self.param["q0"],self.param["q1"]]
            else:
                self.param["Q"]= [self.param["q1"],self.param["q1"]]
                print("[!] Warning : q0 not precised, setting it to q1.")


    def step(self):
        self.global_proportions = [sum(self.population.genotype)/float(self.population.N),
                                   sum(self.population.phenotype)/float(self.population.N)]
        ToyModel.step(self)

    def phenotype_heredity(self,phenotype,genotype):
        """Return the phenotype of the child cell given the one of the parent.
        
        :param phenotype: Phenotype of the parent. 
        :type phenotype: bool
        :param genotype: genotype of the parent. 
        :type genotype: bool
        :return: (bool) - Phenotype of the child. 
        """
        # Phenotipic heridity
        if random.random() < self.param["alpha"]:
            return phenotype
        # Switch probability
        else: 
            if random.random() < self.param["Q"][genotype]:
                return 1 
            else: 
                return 0


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Dictyo toy model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ToyDictyo(ToyModel):
    """ Based on the toy model but a part of the group don't reproduce. (spore/stem).

    .. note::
    - Only 80% of the group (cheaters first) get a chance to reproduce.
    - Alone individuals reproduce only if the parmeter alone_repro = True (Does not change the fitness normalization fonction. [Default = TRUE] 
    """

    def __init__(self,param,tracked_values=[]):
        """Constructeur"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "ToyDictyo [Modified Toymodel]"
        if not "alone_repro" in self.param:
            self.param["alone_repro"]=True
        if self.param["alone_repro"]:
            self.model_name += "Loners can reproduce"
        else:
            self.model_name += "Loners can't reproduce"

    def demographic(self):
            """Global life, Death, Mutation, Heredity and genealogy processes

            Only 80% of the group get a chance to reproduce. Asocial first.

            =========  ============================
            **Read**   self.population.phenotype,
                       self.population.genotype,
                       self.population.repartition,
                       self.population.payoff.
            **Write**  self.population.phenotype,
                       self.population.genotype,
                       self.population.genealogy.
            =========  ============================
            """     

            newborn_genotype = []
            newborn_phenotype = []
            newborn_genealogy = []

            ## Normalize the payoff to give the fitness
            fitness = numpy.array(self.population.payoff, dtype=numpy.float)
            fitness -= numpy.min(fitness)
            fitness /= numpy.max(fitness)

            #fitness index for the couples of (phenotype, repartition).
            fitness_index = {(1,1):0, #social in group.
                             (0,1):1, #asocial in group.
                             (1,0):2, #social alone.
                             (0,0):3} #asocial alone.

            ########### MODIFIED PART ##########################################
            ## Each alone individual has a chance to reproduce once           ##
            ## 80% of the grouped individuals (asocial first) has a chance to ##
            ## reproduce once.                                                ##
            ####################################################################
            
            ## Keep a track of the number of allowed potential reproducer in each
            ## patch's group.
            nb_repro_group = numpy.zeros((self.population.Npatch,1))
            nb_repro_group_p = numpy.zeros((self.population.Npatch,2))

            for np,patch in enumerate(self.population.proportions):
                nb_repro_group[np] = int(patch[1]*0.8)
                nb_repro_group_p[np,0] = patch[1]-patch[0]
                if nb_repro_group_p[np,0] > nb_repro_group[np]:
                    nb_repro_group_p[np,0] = nb_repro_group[np]
                    nb_repro_group_p[np,1] = 0
                else:
                    nb_repro_group_p[np,1] = nb_repro_group[np] - nb_repro_group_p[np,0]
            
            # Each individual is maybe allowed to reproduce once.
            for n,g in enumerate(self.population.genotype):
                p = self.population.phenotype[n] 
                r = self.population.repartition[n]
                patch = n/self.population.T
                
                allowed = 1

                # Only 80% of the group is allowed to try !
                if r: #If attached.
                    if nb_repro_group_p[patch,p]:
                        nb_repro_group_p[patch,p] -= 1
                    else:
                        allowed = 0
                else:
                    allowed = self.param["alone_repro"]
                
                
                if allowed and random.random()<fitness[patch,fitness_index[(p,r)]]:
                
                    ######### END OF MODIFIED PART #####################################"
                    #The genotype is inherited or flipped if mutated.
                    if random.random()<self.param["mu"]:
                        # Mutated : if g = 1, not g = 0 and if g = 0, not g = 1 
                        newborn_genotype.append(not g)
                    else:
                        newborn_genotype.append(g)

                    # Phenotype is inherited according to the rules of phenotype_heredity().
                    newborn_phenotype.append(self.phenotype_heredity(p,g))

                     # Genealogy is the index of the parent in the previous generation.
                    newborn_genealogy.append(n)

            ## Death process : newborn are inserted in random position inside the new population, thus killing the one whose place they take.
            for i in range(len(newborn_genotype)):
                n = random.randint(0,self.population.N-1)
                self.population.phenotype[n] = newborn_phenotype[i]
                self.population.genotype[n]  = newborn_genotype[i]
                self.population.genealogy[n] = newborn_genealogy[i]



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Continuous model
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ToyContinuous(ToyModel):
    """ A model where the probability of attachment are conditioning both the
    payoff and the social cost.

    In this model there's still only two phenotypes at a time a resident 
    (the asocial of the toymodel) and a mutant (the social of the toymodel)

    **Modification from the toymodel :** 

    - In the aggregation phase the probaility of aggregation of two individuals 
    is the geometric mean of the phenotypes.
    - The social cost of an individual is -c*z
    - The group benefit of an individual is b*\overline{z} (mean of the social
    trait).

    """

    def __init__(self,param,tracked_values=[]):
        """Constructor"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = "Continuous Toy Model"

        # The probability of attachment between a za and a zs individual is:
        self.param["pas"] = math.sqrt(self.param["pa"]*self.param["ps"])

    def payoff(self):
        """
        Compute the payoff for each patch and each combinaison of repartition and phenotype.
        
        =========  ============================
        **Read**   self.population.phenotype.
                   self.population.repartition, 
        **Write**  self.population.payoff.
        =========  ============================
        
        .. note ::
           By line in self.population.payoff:
        
           0. Payoff of zs individual in a group
           1. Payoff of za individual in a group
           2. Payoff of zs individual alone
           3. Payoff of za individual alone
        
        """
        ## For each patch
        for patch in range(self.population.Npatch):

            gb = self.group_benefits(patch)
            cost_s = self.cost(self.param["ps"])
            cost_a = self.cost(self.param["pa"])

            # Payoff of zs individual in a group
            
            self.population.payoff[patch,0] = gb - cost_s
            # Payoff of za individual in a group
            self.population.payoff[patch,1] = gb - cost_a
            
            # Payoff of zs individual alone
            self.population.payoff[patch,2] = -cost_s
            # Payoff of za individual alone
            self.population.payoff[patch,3] = -cost_a

    def group_benefits(self,p):
        """ Return the individual group-benefits in the p patch """
        # The group benefit is b * \overline{z} the mean social trait.
        meanZ = self.population.proportions[p,0]*self.param["ps"] 
        meanZ += ((self.population.proportions[p,1] -
                  self.population.proportions[p,0])*self.param["pa"]) 
        meanZ /= self.population.proportions[p,1]  

        return meanZ * self.b

    def cost(self,z):
        """ Return the individual cost of a z-social individual"""
        return self.c * z

class ContinuousNLCost(ToyContinuous):
    """ Continuous Toy model with a non linear cost function

    **Modification from the toycontinuous :**
    
    - Cost of the social trait is not linear (-cz) but tends toward infinty 
    as z tends toward 1.

    Take a new parameter cl (cost linearity). Higher cl means that the cost is
    linear like for greater z before rocketing to infinty.
"""

    def __init__(self,param,tracked_values=[]):
        """Constructor"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = """ContinuousNLCost, 
        Continuous Toy Model with a group size threshold """

        # The probability of attachment between a za and a zs individual is:
        self.param["pas"] = math.sqrt(self.param["pa"]*self.param["ps"])

        # Default value for cl is 4.
        if not "cl" in self.param:
            self.param["cl"] = 4


    def cost(self,z):
        """ Return the individual cost of a z-social individual"""
        return self.c * z * math.exp(1/(1-z)**(1/self.param["cl"])


class ContinuousSizeThreshold(ToyContinuous):
    """ Continuous Toy Model with a group size threshold

    **Modification from the toycontinuous :**
    
    - if groupsize is greater than param["t"]/param["T"] group benefits are null.
    Default value for t is 0.75.

    """

    def __init__(self,param,tracked_values=[]):
        """Constructor"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = """ContinuousSizeThreshold, 
        Continuous Toy Model with a group size threshold """

        # The probability of attachment between a za and a zs individual is:
        self.param["pas"] = math.sqrt(self.param["pa"]*self.param["ps"])

        # Default value for t is 0.75.
        if not "t" in self.param:
            self.param["t"] = 0.75

    def group_benefits(self,p):
        """ Return the individual group-benefits in the p patch """
        # The group benefit is b * \overline{z} the mean social trait. if the 
        # group is small enough.
        if self.population.proportions[p,1] < self.param["t"]/self.param["T"]:

            meanZ = self.population.proportions[p,0]*self.param["ps"] 
            meanZ += ((self.population.proportions[p,1] -
                      self.population.proportions[p,0])*self.param["pa"]) 
            meanZ /= self.population.proportions[p,1]  

            return meanZ * self.b

        # Or it's null.
        else:
            return 0

if __name__ == "__main__":
    param = {"N":100,
             "T":10,
             "ip":0.5,
             "b":20,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.3*0.1),
             "mu":0.9,
             "Q":[0.5,0.5],
             "alpha":0.9}

    tracked_values = ["population.proportions"]

    a = ToyEpigenetic(param, tracked_values)
    #a = ContinuousSizeThreshold(param, tracked_values)

    print("\n Model:")
    print(a)
    print("\n Population:")
    print(a.population)
    print("\n Run:")
    #a.play(10)
    a.equilibrium(1000)



