#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pull enviroment varables as configuration and applies DB initualization if needed
"""

import json
import os

'''
from env, were are the DB files located?
DB_DATA_DIR

DB_LOAD_* per class
* = class name, list of objects that define the class

pyyaml or json should load file defined by var

objects should push directly into model...how?


'''

INSTANCE_ID = os.environ.get("INSTANCE_ID", None)


