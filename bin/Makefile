all: pip heatmap threshold altruism pip_GST pip_NLC trajectoires sizedistr.eps
quick: pip_quick heatmap_quick threshold_quick altruism_quick pip_GST_quick pip_NLC_quick trajectoires_quick
all_pip_quick: pip_quick pip_GST_quick pip_NLC_quick 

pip:
	python figures.py pip

heatmap:
	python figures.py heatmap

threshold:
	python figures.py threshold

altruism:
	python figures.py altruism

pip_GST:
	python figures.py pip

pip_NLC:
	python figures.py pip mdl=0 NLC

trajectoires:
	python figures.py trajectoires

quick := n=100&T=100&replica=2 

pip_quick:
	python figures.py pip precision=0.1&$(quick)

heatmap_quick:
	python figures.py heatmap precision=0.1&$(quick)

threshold_quick:
	python figures.py threshold kmax=3&$(quick)

sizedistr.eps:
	python distr.py

pip_GST_quick:
	python figures.py pip precision=0.1&$(quick) GST

pip_NLC_quick:
	python figures.py pip precision=0.1&$(quick) NLC

trajectoires_quick:
	python figures.py trajectoires range_ip=[0.001,0.01,0.1]&range_g=[10,50]&$(quick)


