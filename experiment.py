import model
import component.functionso as m

fcts = {"attach": "functions-o.attachO",
            "birthanddeath":"functions-o.localbirthdeathO",
            "fpayoff":"functions-o.fpayO",
            "dispersion":"functions-o.disperseO",
            "initialisation":"functions-o.initializeO"}

param = {"N":100,
         "T":10,
         "b":3,
         "c":1,
         "ps":0.3,
         "pa":0.1,
         "mu":0.1}
param["NPATCH"] = param["N"]/param["T"]

a = m.ModelO(param)		#qui istanziare un oggetto della classe ModelO
print("\n Model:")
print(a)
print("\n Population:")
print(a.population)
print("\n Run:")
a.play(5)


