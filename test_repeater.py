import unittest
import sys
from StringIO import StringIO

from repeater import learn, main, repeat

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

	def setUp(self):
		self.out = StringIO()
		sys.stdout = self.out

	def testSampleData(self):
		main(['last_month.csv', 'next_month_input.csv'])
		print self.out.getvalue()
