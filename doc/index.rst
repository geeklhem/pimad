.. Pimad documentation master file, created by
   sphinx-quickstart on Mon Jun  3 12:23:08 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PIMAD documentation
===================

 Pimad (Pimad is modeling adaptive dynamics) is a modeling tool for studying adaptive evolution of grouping by adhesion.

.. toctree::
   :maxdepth: 3


Quick how-to
------------

How to run a simulation:
........................

.. code-block:: bash

  experiment.py <file> [-g=<number>] [-p=<parameters>] [-m=<modelName>]
  experiment.py (-h | --help)
  experiment.py --version
  experiment.py --license

Pimad will try to load any trace data found in <file>. If it's unsuccessfull it 
will create one using the model defined in this file. It will play it until it reach an equilibrium unless the "-g" option is provided.

You should use this file with interactive python :
`ipython -i exepriment.py test.data`.
You will then be able to apply output function to the loaded or generated data
using the `data` object.

**Options:**

.. code-block:: bash

  -g=<number>              Number of generations to run
  -p=<parameters>          Model parmeters in the format "p1=value,p2=value,p3=v"
  -m=<modelName>           Model name (ToyModel or ToyDictyo)
  -h --help                Show this screen.
  --version                Show version.
  --license                Show license information.

How to generate an experimental report ?
.........................................

.. code-block:: bash

  exreport.py
  exreport.py <file>

Pimad will load the specified file (or all the *.data files in the current folder), run the analysis, make the plots and create a html report file in the `reports/` directory with the same name than the input file.

It will also actualize the `reports/index.html` page. 


Structure
----------

Pimad is composed of :

- The Population class : contains the population current characteristics. 
- The Model class : a generic model class from witch inherits all models.
- The Trace class : contains the data (successive states of tracked Population attributes) and perform the numerical analysis.
- The output methods : generate the output (e.g. matplotlib plots) from a Trace object. 

Complete documentation of all the modules can be found here : :ref:`modindex`

Dependencies
------------
Pimad is written in Python 2.7.3 and needs the following libraries :

- Numpy
- Matplotlib
- Docpopt (included)

Licence
-------
Copyright (C) 2013 Guilhem DOULCIER

This program comes with ABSOLUTELY NO WARRANTY.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by 
the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

