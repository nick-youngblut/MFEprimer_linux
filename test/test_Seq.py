#!/usr/bin/env python
# import
from __future__ import print_function
## batteries
import os
import sys
import unittest
## package
from MFEprimer.chilli import Seq

# data dir
test_dir = os.path.join(os.path.dirname(__file__))
data_dir = os.path.join(test_dir, 'data')

class Test_complement(unittest.TestCase):
    def test_simple(self):
        x = 'ATGC'
        y = Seq.complement(x)
        self.assertEqual(y, 'TACG')
    def test_gap(self):
        x = 'AT-GC'
        y = Seq.complement(x)
        self.assertEqual(y, 'TA-CG')
        
class Test_reverse(unittest.TestCase):
    def test_simple(self):
        x = 'ATGC'
        y = Seq.reverse(x)
        self.assertEqual(y, 'CGTA')
    def test_gap(self):
        x = 'AT-GC'
        y = Seq.reverse(x)
        self.assertEqual(y, 'CG-TA')

class Test_rev_com(unittest.TestCase):
    def test_simple(self):
        x = 'ATGC'
        y = Seq.rev_com(x)
        self.assertEqual(y, 'GCAT')
    def test_gap(self):
        x = 'AT-GC'
        y = Seq.rev_com(x)
        self.assertEqual(y, 'GC-AT')
