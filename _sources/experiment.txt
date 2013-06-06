experiment Module
=================

Usage
------

::

   experiment.py <file> [-g <number>]
   experiment.py (-h | --help)
   experiment.py --version
   experiment.py --license

Pimad will try to load any trace data found in <file>. If it's unsuccessfull it 
will create one using the model defined in this file. It will play it for ten
generations unless the "-g" option is provided.

You should use this file with interactive python :
`ipython -i exepriment.py test.data`.
You will then be able to apply output function to the loaded or generated data
using the `data` object.

Options
--------
The options are : ::

   -g                       Number of generations to run
   -h --help                Show this screen.
   --version                Show version.
   --license                Show license information.

