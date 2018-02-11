#!/usr/bin/env python
# import
from __future__ import print_function
## batteries
import os
import sys
import unittest
## package
from MFEprimer.chilli import chilli

# data dir
test_dir = os.path.join(os.path.dirname(__file__))
data_dir = os.path.join(test_dir, 'data')

class Test_DNA2int(unittest.TestCase):
    def test_simple(self):
        x = 'ATGC'
        y = chilli.DNA2int(x)
        msg = 'Return value: {}'.format(y)
        self.assertEqual(y, 54, msg=msg)
        
class Test_DNAint_2_strand(unittest.TestCase):
    def test_simple(self):
        x = 'ATGC'
        y = chilli.DNA2int_2_strand(x)
        msg = 'Return value: {}'.format(y)
        self.assertEqual(y, (54,99), msg=msg)

class Test_baseN(unittest.TestCase):
    def test_simple(self):
        x = 10
        y = chilli.baseN(x, 2)
        msg = 'Return value: {}'.format(y)
        self.assertEqual(y, '1010', msg=msg)

# class Test_cal_dimer(unittest.TestCase):
#     def test_simple(self):
#         x = 'ATGCGCGATAGAATATACATA'
#         y = 'TAGGCCGAGATAATATACATA'
#         y = chilli.cal_dimer(x, y)
#         msg = 'Return value: {}'.format(y)
#         self.assertEqual(y, 1, msg=msg)
