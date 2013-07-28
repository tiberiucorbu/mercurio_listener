'''
Created on Jul 21, 2013

@author: Tiberiu
'''
import unittest
from mercurio.engine import Mercurio


class Test(unittest.TestCase):


    def setUp(self):
        self.mercurio = Mercurio()
        pass


    def tearDown(self):
        pass

    def testIgnoreWhiteSpaces(self):
        print 'Ignore whitespaces test.'
        res = self.mercurio._dict_from_readline("  button  =  on   ")
        self.assertEqual('on', res.get('button'), 'not expected')
        pass
    
    
    def test_dict_from_readline_with_valid_input(self):
        value = "target=something"
        result = self.mercurio._dict_from_readline(value)
        assert result, {'target': 'something'}
        pass
    
    
    def test_dict_from_readline_with_empty_input(self):
        value = "\n\r"
        result = self.mercurio._dict_from_readline(value)
        assert result == {}
        pass
    
    
    def test_dict_from_readline_with_invalid_input(self):
        value = "somethinginvalid"
        result = self.mercurio._dict_from_readline(value)
        assert result == {}
        pass
    
    
    def test_prepare_command(self):
        command = "fab production deploy"
        result = self.mercurio._prepare_command(command)
        assert result == ['fab', 'production', 'deploy']
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()