all: pip heatmap threshold altruism pip_GST pip_NLC trajectoires sizedistr.eps
quick: pip_quick heatmap_quick threshold_quick altruism_quick pip_GST_quick pip_NLC_quick trajectoires_quick
all_pip_quick: pip_quick pip_GST_quick pip_NLC_quick 


pip: pip_TOY pip_GST pip_NLC

pip_TOY:
	python figures.py pip

heatmap:
	python figures.py heatmap

threshold:
	python figures.py threshold

altruism:
	python figures.py altruism


pip_GST:
	python figures.py pip mdl=0 GST

pip_NLC:
	python figures.py pip mdl=0 NLC

trajectoires:
	python figures.py trajectoires
	python figures.py trajectoires dz=-0.1

quick :=n=100ANDT=100ANDreplica=2

pip_quick:
	python figures.py pip precision=0.1AND$(quick)

heatmap_quick:
	python figures.py heatmap precision=0.1AND$(quick)

threshold_quick:
	python figures.py threshold kmax=3AND$(quick)

sizedistr.eps:
	python distr.py

pip_GST_quick:
	python figures.py pip precision=0.1AND$(quick) GST

pip_NLC_quick:
	python figures.py pip $(quick)ANDprecision=0.1 NLC

trajectoires_quick:
	python figures.py trajectoires dz=-0.1ANDrange_ip=[0.001,0.01,0.1]ANDrange_g=[10,50]AND$(quick)
	python figures.py trajectoires range_ip=[0.001,0.01,0.1]ANDrange_g=[10,50]AND$(quick)
