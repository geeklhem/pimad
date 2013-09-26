#!/bin/sh
python experiment.py epi_i04_a01.data -m ToyEpigenetic -p alpha=0,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.4
python experiment.py epi_i04_a06.data -m ToyEpigenetic -p alpha=0.6,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.4
python experiment.py epi_i04_a08.data -m ToyEpigenetic -p alpha=0.8,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.4
python experiment.py epi_i04_a1.data -m ToyEpigenetic -p alpha=1,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.4

python experiment.py epi_i005_a01.data -m ToyEpigenetic -p alpha=0,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.05
python experiment.py epi_i005_a06.data -m ToyEpigenetic -p alpha=0.6,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.05
python experiment.py epi_i005_a08.data -m ToyEpigenetic -p alpha=0.8,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.05
python experiment.py epi_i005_a1.data -m ToyEpigenetic -p alpha=1,q0=0.2,q1=0.8,N=1000000,mu=0,ip=0.05





