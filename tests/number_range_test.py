'''
Created on Jul 21, 2013

@author: Tiberiu
'''
import unittest
from mercurio import number_range


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    def testRangeExactMatch(self):
        print 'test Range - Exact Match.'
        res = number_range.NumberRange('100, 80, 82');
        self.assertTrue(res.contains(100), 'not expected')

        self.assertTrue(res.contains(100), 'not expected')
        self.assertTrue(res.contains(80), 'not expected')
        self.assertFalse(res.contains(83), 'not expected')
        pass
    
    def testRangeBetweenMatch(self):
        print 'testRangeBetweenMatch.'
        res = number_range.NumberRange('100-80, 200-300');
        self.assertTrue(res.contains(100), 'not expected')
        self.assertFalse(res.contains(79), 'not expected')
        self.assertTrue(res.contains(250), 'not expected')
        self.assertTrue(res.contains(300), 'not expected')
        pass
    
    def testLeftRightExclusiveMatch(self):
        print 'testLeftRightExclusiveMatch.'
        res = number_range.NumberRange('80>, >100');
        self.assertTrue(res.contains(101), 'not expected')
        self.assertTrue(res.contains(70), 'not expected')
        self.assertFalse(res.contains(90), 'not expected')
        pass
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()