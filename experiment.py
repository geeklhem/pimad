import model

fcts = {"attach": 'test.attach',
            "birthanddeath":"test.bad",
            "fpayoff":"test.payoff",
            "dispersion":"test.dispersion",
            "initialisation":"test.init"}

param = {"N":100000,
         "T":1000,
         "b":3,
         "c":1,
         "ps":0.3,
         "pa":0.1,
         "mu":0.001}
param["NPATCH"] = param["N"]/param["T"]

a = model.Model(fcts,param)
print("\n Model:")
print(a)
print("\n Population:")
print(a.population)
print("\n Run:")
a.play(5)

##########
#for t in range(NGEN):
#	if (t == 0):
#		initialize(N, T, patch_du, genotype, phenotype, repartition, payoff)
#	else:
#		disperse(genotype, phenotype)
#	attach(N, T, NPATCH, PS, PA, phenotype, repartition)
#	mypatch = evaluator(N, T, NPATCH, patch_du, phenotype, repartition)
#	for i in range(N):
#		payoff[i]=fpay(mypatch, patch_du, repartition, phenotype, i, B, C)
#	normalize(N, T, payoff)	
#	localbirthdeath(N, T, NPATCH, MU, patch_du, genotype, phenotype, repartition, payoff)
##########
