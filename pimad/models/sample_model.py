#!/usr/bin/env/ python
# -*- coding: utf-8 -*-
"""Sample model - Copy this file and create your own"""

import models.model as model
from toymodel import ToyModel

class SampleModel(ToyContinuous):
    """ Sample Model
    """

    def __init__(self,param,tracked_values=[]):
        """Constructor"""
        model.Model.__init__(self,param,tracked_values)
        self.model_name = """Sample Model"""


# Model's Class (Required for import in main program)
model_class = SampleModel

