#!/usr/bin/env python
# import
from __future__ import print_function
## batteries
import os
import sys
import pytest
## package
from MFEprimer.chilli import chilli

# data dir
test_dir = os.path.join(os.path.dirname(__file__))
data_dir = os.path.join(test_dir, 'data')

class Test_DNA2int(object):
    def test_simple(self):
        x = 'ATGC'
        y = chilli.DNA2int(x)
        msg = 'Return value: {}'.format(y)
        assert y == 54
        
class Test_DNAint_2_strand(object):
    def test_simple(self):
        x = 'ATGC'
        y = chilli.DNA2int_2_strand(x)
        msg = 'Return value: {}'.format(y)
        assert y == (54,99)

class Test_baseN(object):
    def test_simple(self):
        x = 10
        y = chilli.baseN(x, 2)
        msg = 'Return value: {}'.format(y)
        assert y == '1010'

# class Test_cal_dimer(object):
#     def test_simple(self):
#         x = 'ATGCGCGATAGAATATACATA'
#         y = 'TAGGCCGAGATAATATACATA'
#         y = chilli.cal_dimer(x, y)
#         msg = 'Return value: {}'.format(y)
#         assert(y, 1, msg=msg)
