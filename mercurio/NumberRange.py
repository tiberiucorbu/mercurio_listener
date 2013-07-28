#!/usr/bin/python
import re
from mercurio.LoggerFactory import LoggerFactory
'''
Created on Jul 27, 2013

@author: Tiberiu
'''  

class RangeStatement:
        
    '''
    RegEx used to extract an exact comparison. Matches any number
    ''' 
    EXACT_COMPARE = r'(\d+)'
    '''
    RegEx used to extract between comparison. Matches: 100-200
    '''
    BETWEEN_COMPARE = r'(\d+)[-]{1}(\d+)'
    '''
    RegEx used to extract a  left side compare. Matches: 100>, 100>=, 100<, 100<=
    '''
    LEFT_COMPARE = r'(\d+)([=]?[<>]{1})'
    '''
    RegEx used to extract right side compare. Matches: >100, >=100, <100, <=100
    '''
    RIGHT_COMPARE = r'([<>]{1}[=]?)(\d+)'  
    '''
    Mapping between the regex matcher and the meaning of it's groups.
    Answers to which group represents the operator and
    where to place the value to be matched, on the left or right side.
    
    Relyes on the index of each mapping array: index 0 is left value group num.,
    index 1 is the operator group num. and index 2 is the right value group num.
    
    '-1' means no group 
    '''
    MAPPING = {
               EXACT_COMPARE: [1, -1, -1],
               BETWEEN_COMPARE: [1, -1, 2],
               LEFT_COMPARE: [1, 2, -1],
               RIGHT_COMPARE: [-1, 1, 2]
               }  
    '''
    A mapping between the literal operator and it's algoritmic meaning, the keys are kept in a technical educated form 
    but could be changed to some 'business' values like: 'greater than' instead of '>'
    '''
    COMPARATIONS = {
                    'between':(lambda x, y, value: value >= x and value <= y), 
                    '>': (lambda x, y: x > y), 
                    '<': (lambda x, y: x < y), 
                    '>=': (lambda x, y: x >= y), 
                    '<=': (lambda x, y: x <= y)
                    }

    '''
    RangeStatement - Creates a range statement useful to check if a number is in a defined range, 
    like an check of the following form: is 100 bigger than 1000 ? 

    @param rangeString - any match of the constants patterns defined as a range : EXACT_COMPARE,  
    BETWEEN_COMPARE, etc.
    @param debug - should this object print out debug infos ?
    '''
    def __init__(self, rangeString):
        self.log = LoggerFactory().get()
        self.parseRange(rangeString)
        
    
    def parseRange(self, rangeString):
        '''
        Tries to find a mattching 
        '''
        for x in [self.BETWEEN_COMPARE, self.LEFT_COMPARE, self.RIGHT_COMPARE, self.EXACT_COMPARE]:
            y = self.match(x, rangeString) 
            if y:
                m = self.MAPPING[x]
                left = self.getRangeValue(y, m[0]);
                operator = self.getRangeValue(y, m[1])
                right = self.getRangeValue(y, m[2])
                self.log.debug('Matched rangeString: %s;  left value: %s operator: %s right value: %s' %  (rangeString, left, operator, right) )
                self.setRangeValues(left, operator, right)
                break
            self.log.debug('Not matched: %s' % rangeString)

    def getRangeValue(self, matcher, group):
        if group > -1: 
            return matcher.group(group)
        else: 
            return None
        
    def match(self, matcher, stmt):
        m = re.match(matcher, stmt)
        return m 
    
    def setRangeValues(self, left, operator, right):
        self.left = None if left is None else float(left)
        self.right = None if right is None else float(right)
        self.operator = operator
    
    def contains(self, val):
        x = float(val)
        retVal = False
        if self.operator is None :
            retVal = self.isBetweenOrExact(x)
        else :     
            retVal = self.rightOrLeftCompare(x)
        return retVal
    
    def rightOrLeftCompare(self, x):
        if self.COMPARATIONS[self.operator]:
            func = self.COMPARATIONS[self.operator]
            if self.right is None :
                return func(self.left, x)
            else :
                return func(x, self.right) 
    
    def isBetweenOrExact(self, x):
        if self.right is None :
            self.log.debug('Exact Comparison - compare value is : %s, matcher value is %s' %  (x, self.left)  )
            return x == self.left
        else :
            self.log.debug('Between Comparison - compare value is : %s, matcher value on the right side is %s and on left side is %s' % (x, self.right , self.left))
            return self.COMPARATIONS['between'](self.left, self.right, x) or self.COMPARATIONS['between'](self.right, self.left, x)


class NumberRange:
    
    def __init__(self, rangeString):
        self.rangeString = rangeString
        self.ranges = set()
        self.initRange()

        
    def initRange(self):
     
        for x in self.rangeString.split(','):       
            rangeStatement = RangeStatement(x.strip())
            if rangeStatement is not None:
                self.ranges.add(rangeStatement)
        
        
    def contains(self, x):
        for aRange in self.ranges:
            if aRange.contains(x):
                return True

        
if __name__ == "__main__":
    print "Done..."
        
