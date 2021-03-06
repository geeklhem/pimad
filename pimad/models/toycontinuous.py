#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Continuous toy model"""

from __future__ import division
import numpy as np
from pimad.model import Model


class ToyContinuous(Model):
    """ A model where the probability of attachment are conditioning both the
    payoff and the social cost.
    """
    EXAMPLE_PARAMETERS =  {"n":100,  # Number of patches
                           "T":1000, # Patch size
                           "ip":0,   # Initial proportions of mutants
                           "m":0.5,  # Mutant trait value
                           "r":0.5,  # Resident trait value
                           "mu":0,   # Mutation rate
                           "b":20,   # Benefits coefficient
                           "c":1,    # Cost coefficient
                           "g":100,   # Number of generations
                       }
    model_name = "Continuous Toy Model [Garcia, Doulcier & De Monte 2015]"

    def __init__(self,param,tracked_values=()):
        """Constructor"""
        super(ToyContinuous,self).__init__(param,tracked_values)


        required_param = [("r","Resident trait value in [0,1]."),
                          ("m","Mutant trait value in [0,1].")]
        for p in required_param:
            if p[0] not in self.p:
                raise ValueError("Missing parameter: {0[0]} ({0[1]})".format(p))

            
    def step(self):
        """Runs one generation of the model
    
        Called by model.play at each generation """
        
        self.dispersion()
        self.aggregation()
        payoffs = self.payoff()
        self.demographic(payoffs)
        

    
    def dispersion(self):
        """ Shuffle individuals and reset aggregation status. 
        
        """ 

        ## Reset of the individuals population arrays
        self.population.aggregated[:] = 0
        self.population.genealogy[:] = -1

        ## Shuffling the individuals ! 
        p = np.random.permutation(self.population.N)
        self.population.phenotype.flat = self.population.phenotype.flat[p] 
        self.population.genotype.flat = self.population.genotype.flat[p]

                   
    def aggregation(self):
        """ One shot aggregation process.
        """


        # Choose a random recruiter by patch:
        recruiter = np.random.randint(self.population.T,size=self.population.n)
        # Get its phenotype 
        recruiter_phenotype = self.population.phenotype[recruiter,range(self.population.n)]
        attch_proba_recruiter = (  self.p["r"] * np.logical_not(recruiter_phenotype)
                                   + self.p["m"] * recruiter_phenotype)

        # The recruiters are always aggregated. 
        self.population.aggregated[recruiter,range(self.population.n)] = 1
        
        
        # Alternative: the recruiter is aggregated only if its social trait is >0. 
        #(self.p["r"] * np.logical_not(recruiter_phenotype) + self.p["m"] * recruiter_phenotype ) >0

        ### One shot attachment process...
        for z,loners in [(self.p["r"],self.population.loner_residents),
                         (self.p["m"],self.population.loner_mutants)]:
            
            number = loners.sum(0)
            proba = np.sqrt(z * attch_proba_recruiter)

            # Number of individual aggregated by patch...
            try:
                attached = np.array([np.random.binomial(n,p) for n,p in zip(number,proba)])
            except ValueError as e:
                print("Error in attachment phase.")
                print(number,proba)
                raise ValueError(e)
            # in each column, attach the n first of this phenotype
            for i,n in enumerate(attached):
                x = np.nonzero(loners[:,i])[0]
                self.population.aggregated[x[:n],i] = 1
      
    def payoff(self):
        """
        Compute the payoff for each patch and each combinaison of repartition and phenotype.
        """
        
        average_z = (self.population.aggregated_residents.sum(0) * self.p["r"]
                     + self.population.aggregated_mutants.sum(0) * self.p["m"])/self.population.aggregated.sum(0)
        group_benefits = self.p["b"] * average_z
        #print group_benefits.shape

        return {"aggregated":{"resident":group_benefits-self.p["c"]*self.p["r"],
                                "mutant":group_benefits-self.p["c"]*self.p["m"]},
                  "loner":{"resident":[-self.p["c"]*self.p["r"]]*self.p["n"],
                           "mutant":[-self.p["c"]*self.p["m"]]*self.p["n"]},
        }
    


    def demographic(self,payoff):
        """Life & Death.
        """     
        
        ## Normalize the payoff to give the fitness.
        #print "Payoff:\n", payoff
        fitness = np.array([payoff["aggregated"]["resident"],
                            payoff["aggregated"]["mutant"],
                            payoff["loner"]["resident"],
                            payoff["loner"]["mutant"]])
        

        if np.min(fitness.flat) != np.max(fitness.flat):
            fitness -= np.min(fitness.flat)
            fitness /= np.max(fitness.flat)
        else:
            fitness.flat[:] = .5 

        ## Count the number of individual in each fitness category.
        number = np.array([self.population.aggregated_residents.sum(0),
                           self.population.aggregated_mutants.sum(0),
                           self.population.loner_residents.sum(0),
                           self.population.loner_mutants.sum(0)])


        ## Each individual is allowed to try to reproduce once.
        try:
            offspring = np.array([np.random.binomial(n,p) for n,p in zip(number.flat,
                                                                         fitness.flat)],
                             ).reshape(number.shape)
        except ValueError as e:
                print("Error in demographic phase: offspring.")
                print("Payoff: {}".format(payoff))
                print("Number \t Fitness \n"+"\n".join(["{}\t{}".format(n,p)
                                                         for n,p in zip(number.flat, fitness.flat)]))
                raise ValueError(e)
        offspring = offspring.sum(1)        
        offspring_residents = offspring[0] + offspring[2] #No of new Aggregated & loners residents.
        offspring = offspring.sum() #total offspring        
        

        # Mutations
        try:
            offspring_residents += (np.random.binomial(offspring - offspring_residents,self.p["mu"]) #reverse mutation
                                    - np.random.binomial(offspring_residents,self.p["mu"])) #forward mutation
        except ValueError as e:
                print("Error in demographic phase: mutation. (mu = {})".format(self.p["mu"]))
                print(offspring,offspring_residents)
                raise ValueError(e)

        
        ## Death process : newborn are inserted in random position
        ## inside the new population, thus killing the one whose place
        ## they take.
        positions = np.random.permutation(self.population.N)[:offspring]
   
        self.population.phenotype.flat[positions[:offspring_residents]] = 0
        self.population.phenotype.flat[positions[offspring_residents:]] = 1 

        
# Name of the model's Class (Required for import in main program)
model_class = ToyContinuous

class ToyContinuousGST(ToyContinuous):
    """Toy continuous with a group size threshold"""
    model_name = "Continuous Toy Model with group-size threshold [Garcia, Doulcier & De Monte 2015]"
    EXAMPLE_PARAMETERS = ToyContinuous.EXAMPLE_PARAMETERS
    EXAMPLE_PARAMETERS["alpha"] = 0.75
        
    def __init__(self,param,tracked_values=()):
        """Constructor"""
        super(ToyContinuousGST,self).__init__(param,tracked_values)
        

        required_param = [("alpha","Group size threshold (as a proportion of T) in [0,1]."),]


        for p in required_param:
            if p[0] not in self.p:
                raise ValueError("Missing parameter: {0[0]} ({0[1]})".format(p))
    def payoff(self):
        """
        Compute the payoff for each patch and each combinaison of repartition and phenotype.
        """
        
        average_z = (self.population.aggregated_residents.sum(0) * self.p["r"]
                     + self.population.aggregated_mutants.sum(0) * self.p["m"])/self.population.aggregated.sum(0)
        group_benefits = self.p["b"] * average_z * (self.population.aggregated.sum(0)<= [self.p["alpha"]*self.p["T"]]*self.p["n"])
        #print group_benefits.shape

        return {"aggregated":{"resident":group_benefits-self.p["c"]*self.p["r"],
                                "mutant":group_benefits-self.p["c"]*self.p["m"]},
                  "loner":{"resident":[-self.p["c"]*self.p["r"]]*self.p["n"],
                           "mutant":[-self.p["c"]*self.p["m"]]*self.p["n"]},
        }

class ToyContinuousNLC(ToyContinuous):
    """Toy continuous with a non linear cost function"""
    model_name = "Continuous Toy Model with a non linear cost function [Garcia, Doulcier & De Monte 2015]"
    EXAMPLE_PARAMETERS = ToyContinuous.EXAMPLE_PARAMETERS
    EXAMPLE_PARAMETERS["chi"] = 2

    def __init__(self,param,tracked_values=()):
        """Constructor"""
        super(ToyContinuousNLC,self).__init__(param,tracked_values)

        required_param = [("chi","Linearity parameter, >0"),]
        
        for p in required_param:
            if p[0] not in self.p:
                raise ValueError("Missing parameter: {0[0]} ({0[1]}), Example value = {}".format(p,EXAMPLE_PARAMETERS[p[0]]))
    def payoff(self):
        """
        Compute the payoff for each patch and each combinaison of repartition and phenotype.
        """
        
        average_z = (self.population.aggregated_residents.sum(0) * self.p["r"]
                     + self.population.aggregated_mutants.sum(0) * self.p["m"])/self.population.aggregated.sum(0)
        group_benefits = self.p["b"] * average_z 

        def cost(z):
            """ Non linear cost """
            return - self.p["c"]* z * np.exp( (1-z)**(-1.0/self.p["chi"]) - 1 ) 
                                 
        return {"aggregated":{"resident":group_benefits+cost(self.p["r"]),
                              "mutant":group_benefits+cost(self.p["m"])},
                  "loner":{"resident":[cost(self.p["r"])]*self.p["n"],
                           "mutant":[cost(self.p["m"])]*self.p["n"]},
        }

    
class ToyContinuousSigB(ToyContinuous):
    """Toy continuous with group benefits are following a sigmoïd cruve as
      defined in [Archetti et al 2011, Ecology Letters].
    """
    model_name = "Continuous Toy Model with a  sigmoïd benefits function"
    EXAMPLE_PARAMETERS = ToyContinuous.EXAMPLE_PARAMETERS
    EXAMPLE_PARAMETERS["s"] = 1
    EXAMPLE_PARAMETERS["k"] = .6

    def __init__(self,param,tracked_values=()):
        """Constructor"""
        super(ToyContinuousSigB,self).__init__(param,tracked_values)

        required_param = [("s","steepness at the inflection point."),
                          ("k","inflection point as a proportion of T, in ]0,1[."),]
        
        for p in required_param:
            if p[0] not in self.p:
                raise ValueError("Missing parameter: {0[0]} ({0[1]}), Example value = {}".format(p,EXAMPLE_PARAMETERS[p[0]]))

    def payoff(self):
        """
        Compute the payoff for each patch and each combinaison of repartition and phenotype.
        """
        
        average_z = (self.population.aggregated_residents.sum(0) * self.p["r"]
                     + self.population.aggregated_mutants.sum(0) * self.p["m"])/self.population.aggregated.sum(0)


        # i is the number of cooperators. 
        i = self.population.aggregated.sum(0)
        alpha = lambda x: (1 + np.exp(self.p["s"]*self.p["k"]*self.p["T"]-x))**(-1)
        zero = np.zeros(self.p["n"])
        #print "alpha(0)={}".format(alpha(zero))
        #print "alpha(T)={}".format(alpha(zero+self.p["T"]))
        group_benefits = self.p["b"] * average_z * (alpha(i) - alpha(zero)) / (alpha(zero + self.p["T"]) - alpha(zero))
        group_benefits /= i

        
        return {"aggregated":{"resident":group_benefits-self.p["c"]*self.p["r"],
                                "mutant":group_benefits-self.p["c"]*self.p["m"]},
                  "loner":{"resident":[-self.p["c"]*self.p["r"]]*self.p["n"],
                           "mutant":[-self.p["c"]*self.p["m"]]*self.p["n"]},
        }
