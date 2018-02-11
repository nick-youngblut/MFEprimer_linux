#!/usr/bin/env python
# import
from __future__ import print_function
## batteries
import os
import sys
import pytest
## package
from MFEprimer.chilli import Seq

# data dir
test_dir = os.path.join(os.path.dirname(__file__))
data_dir = os.path.join(test_dir, 'data')

class Test_complement(object):
    def test_simple(self):
        x = 'ATGC'
        y = Seq.complement(x)
        assert y == 'TACG'
    def test_gap(self):
        x = 'AT-GC'
        y = Seq.complement(x)
        assert y == 'TA-CG'
        
class Test_reverse(object):
    def test_simple(self):
        x = 'ATGC'
        y = Seq.reverse(x)
        assert y == 'CGTA'
    def test_gap(self):
        x = 'AT-GC'
        y = Seq.reverse(x)
        assert y == 'CG-TA'

class Test_rev_com(object):
    def test_simple(self):
        x = 'ATGC'
        y = Seq.rev_com(x)
        assert y == 'GCAT'
    def test_gap(self):
        x = 'AT-GC'
        y = Seq.rev_com(x)
        assert y == 'GC-AT'
