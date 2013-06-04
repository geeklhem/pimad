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
