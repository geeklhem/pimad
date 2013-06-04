"""Modeling methods package

This package contains all modeling methods that can be imported by the :class:`Model` class.
"""

import os
for module in os.listdir(os.path.dirname(__file__)):
    if module == '__init__.py' or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module
