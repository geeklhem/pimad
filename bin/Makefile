all: pip heatmap threshold altruism pip_GST pip_NLC trajectoires sizedistr.eps
quick: pip_quick heatmap_quick threshold_quick altruism_quick pip_GST_quick pip_NLC_quick trajectoires_quick
all_pip_quick: pip_quick pip_GST_quick pip_NLC_quick 


pip: pip_TOY pip_GST pip_NLC

pip_TOY:
	ipython figures.py pip

heatmap:
	ipython figures.py heatmap r=0.22ANDg=500

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
	ipython figures.py pip precision=0.1AND$(quick)ANDlk_R=100

threshold:
	ipython figures.py threshold 

threshold_small:
	ipython figures.py threshold b_range=[3,10,20,40]ANDreplica=30

threshold_quick:
	ipython figures.py threshold kmax=5AND$(quick)ANDb_range=[3,10,20]

sizedistr.eps:
	ipython distr.py

pip_GST_quick:
	ipython figures.py pip precision=0.1AND$(quick) GST

pip_NLC_quick:
	ipython figures.py pip $(quick)ANDprecision=0.1 NLC

trajectoires_quick:
	ipython figures.py trajectoires dz=-0.1ANDrange_ip=[0.001,0.01,0.1]ANDrange_g=[10,50]AND$(quick)
	ipython figures.py trajectoires range_ip=[0.001,0.01,0.1]ANDrange_g=[10,50]AND$(quick)
