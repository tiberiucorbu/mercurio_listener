'''
Created on Jul 21, 2013

@author: Tiberiu
'''
import unittest
from mercurio.NumberRange import NumberRange


class Test(unittest.TestCase):

    def testRangeExactMatch(self):
        print 'test range - exact match.'
        res = NumberRange('100, 80, 82');
        self.assertTrue(res.contains(100), 'not expected')

        self.assertTrue(res.contains(100), 'not expected')
        self.assertTrue(res.contains(80), 'not expected')
        self.assertFalse(res.contains(83), 'not expected')
        pass
    
    def testRangeBetweenMatch(self):
        print 'test interval ends defined, '
        res = NumberRange('100-80, 200-300');
        self.assertTrue(res.contains(100), 'not expected')
        self.assertFalse(res.contains(79), 'not expected')
        self.assertTrue(res.contains(250), 'not expected')
        self.assertTrue(res.contains(300), 'not expected')
        pass
    
    def testLeftRightExclusiveMatch(self):
        print 'test left and right match.'
        res = NumberRange('80>, >100');
        self.assertTrue(res.contains(101), 'not expected')
        self.assertTrue(res.contains(70), 'not expected')
        self.assertFalse(res.contains(90), 'not expected')
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()