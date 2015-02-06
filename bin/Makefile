all: pip heatmap threshold altruism pip_GST pip_NLC trajectoires sizedistr.eps
quick: pip_quick heatmap_quick threshold_quick altruism_quick pip_GST_quick pip_NLC_quick trajectoires_quick
all_pip_quick: pip_quick pip_GST_quick pip_NLC_quick 


pip: pip_TOY pip_GST pip_NLC

pip_TOY:
	ipython figures.py pip

heatmap:
	ipython figures.py heatmap r=0.22ANDg=500

threshold:
	ipython figures.py threshold g=500

altruism:
	ipython figures.py altruism


pip_GST:
	ipython figures.py pip mdl=0 GST

pip_NLC:
	ipython figures.py pip mdl=0 NLC


pip_SIG:
	ipython figures.py pip mdl=0 SIG


trajectoires:
	ipython figures.py trajectoires
	ipython figures.py trajectoires dz=-0.1

quick :=n=100ANDT=100ANDreplica=2

pip_SIG_quick:
	ipython figures.py pip precision=0.1AND$(quick) SIG

pip_quick:
	ipython figures.py pip precision=0.1AND$(quick)

heatmap_quick:
	ipython figures.py heatmap precision=0.1AND$(quick)ANDr=0.22ANDT_range=[100,500,1000]ANDg=500

threshold_quick:
	ipython figures.py threshold kmax=5AND$(quick)ANDT_range=[100,500]ANDb_range=[2,10,20]ANDg=500

threshold_100:
	ipython figures.py threshold kmax=10ANDT_range=[100]ANDb_range=[2,4,8,10,20,30,40,50,60,70,80]ANDg=500ANDreplica=10

threshold_new:
	ipython figures.py threshold kmax=10ANDT_range=[20,100]ANDb_range=[2,3,4,5,6,7,8,9,10,15,20,25,30,35,40]ANDg=500ANDreplica=50

threshold_new_quick:
	ipython figures.py threshold kmax=5AND$(quick)ANDT_range=[20,100]ANDb_range=[2,5,10,15,20,25,30,35,40]ANDg=500ANDreplica=10


sizedistr.eps:
	ipython distr.py

pip_GST_quick:
	ipython figures.py pip precision=0.1AND$(quick) GST

pip_NLC_quick:
	ipython figures.py pip $(quick)ANDprecision=0.1 NLC

trajectoires_quick:
	ipython figures.py trajectoires dz=-0.1ANDrange_ip=[0.001,0.01,0.1]ANDrange_g=[10,50]AND$(quick)
	ipython figures.py trajectoires range_ip=[0.001,0.01,0.1]ANDrange_g=[10,50]AND$(quick)
