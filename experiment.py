import model
import component.omodel as om

fcts = {}
fcts["attach"] = "ofunctions.attach"
fcts["birthanddeath"] = "ofunctions.localbirthdeath"
fcts["fpayoff"] = "ofunctions.fpay"
fcts["dispersion"] = "ofunctions.disperse"
fcts["initialisation"] = "ofunctions.initialize"

param = {}
param["N"] = 1000
param["T"] = 50
param["b"] = 3
param["c"] = 1
param["ps"] = 0.5
param["pa"] = 0.2
param["mu"] = 0.01
param["NPATCH"] = param["N"]/param["T"]

a = om.ModelO(param)
print("\n Model:")
print(a)
print("\n Population:")
print(a.population)
print("\n Run:")
a.play(5)


