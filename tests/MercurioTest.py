import unittest
from mercurio.Mercurio import Mercurio

'''
Test for mercurio lister

Created on Jul 21, 2013

@author: Tiberiu
'''

class Test(unittest.TestCase):


    def setUp(self):
        self.mercurio = Mercurio()
        pass


    def tearDown(self):
        pass

    def testDictionareFromReadlineIgnoreWhiteSpaces(self):
        print 'Ignore whitespaces test.'
        res = self.mercurio._dictionareFromReadline("  button  =  on   ")
        self.assertEqual('on', res.get('button'), 'not expected')
        pass
    
    
    def testDictionareFromReadlineValidInput(self):
        value = "target=something"
        result = self.mercurio._dictionareFromReadline(value)
        assert result, {'target': 'something'}
        pass
    
    
    def testDictionareFromReadlineEmptyInput(self):
        value = "\n\r"
        result = self.mercurio._dictionareFromReadline(value)
        assert result == {}
        pass
    
    
    def testDictionareFromReadlineInvalidInput(self):
        value = "somethinginvalid"
        result = self.mercurio._dictionareFromReadline(value)
        assert result == {}
        pass
    
    
    def testPrepareCommand(self):
        command = "fab production deploy"
        result = self.mercurio._prepareCommand(command)
        assert result == ['fab', 'production', 'deploy']
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()