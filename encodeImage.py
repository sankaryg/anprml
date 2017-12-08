# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 10:52:22 2017

@author: Ba La
"""

import base64

def encode(fname):
    with open(fname, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string