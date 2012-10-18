#!/usr/bin/python

import csv
import unittest
import sys
from itertools import izip
from StringIO import StringIO

from repeater import learn, main, repeat_files, repeat_tables

simple = (
    ('a', 'A'),
)

longer = (
    ('a', 'A'),
    ('b', 'B'),
    ('b', 'B'),
    ('a', 'A'),
)

class TestLearnKnowledgeMap(unittest.TestCase):

    def testSimple(self):
    	kmap = learn(simple, {
    		# column 0 depends on column 1
    		0 : 1,
    	})
    	self.assertEqual(kmap[0]['A'], 'a')

    def testLonger(self):
    	kmap = learn(longer, {
    		# column 0 depends on column 1
    		0 : 1,
    	})
    	self.assertEqual(dict(kmap), {
    		0: {
    			'A': 'a',
    			'B': 'b',
    		}
    	})

class TestRepeaterCLI(unittest.TestCase):

    def testSampleData(self):
        resultIO = StringIO()
    	repeat_files(open('last_month.csv', 'rb'), open('next_month_input.csv', 'rb'), resultIO)
        resultData = csv.reader(resultIO.getvalue())
        with open('next_month_complete.csv', 'rb') as expectedFile:
            expectedData = csv.reader(expectedFile)
            for expected, actual in izip(expectedData, resultData):
                self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

