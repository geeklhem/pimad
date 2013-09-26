#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
""" Pimad configuration file"""

import math

# Default Model
default_model = "toymodel" 

# Models Default values
p_default = {"N":100,
             "T":100,
             "ip":0.1,
             "b":20,
             "c":1,
             "ps":0.8,
             "pa":0.3,
             "pas":math.sqrt(0.8*0.3),
             "mu":0.01}
