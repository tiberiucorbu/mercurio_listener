#!/usr/bin/python
import re

'''
Created on Jul 27, 2013

@author: Tiberiu
'''  

class RangeStatement:
        
    '''
    RegEx used to extract an exact comparison. Matches any number
    ''' 
    NUM_RANGE_EXACT_COMPARE = r'(\d+)'
    '''
    RegEx used to extract between comparison. Matches: 100-200
    '''
    NUM_RANGE_BETWEEN_COMPARE = r'(\d+)[-]{1}(\d+)'
    '''
    RegEx used to extract a  left side compare. Matches: 100>, 100>=, 100<, 100<=
    '''
    NUM_RANGE_LEFT_COMPARE = r'(\d+)([=]?[<>]{1})'
    '''
    RegEx used to extract right side compare. Matches: >100, >=100, <100, <=100
    '''
    NUM_RANGE_RIGHT_COMPARE = r'([<>]{1}[=]?)(\d+)'  
    '''
    Mapping between the regex matcher and the meaning of it's groups.
    Answers to which group represents the operator and
    where to place the value to be matched, on the left or right side.
    
    Relyes on the index of each mapping array: index 0 is left value group num.,
    index 1 is the operator group num. and index 2 is the right value group num.
    
    '-1' means no group 
    '''
    MAPPING = {
               NUM_RANGE_EXACT_COMPARE: [1, -1, -1],
               NUM_RANGE_BETWEEN_COMPARE: [1, -1, 2],
               NUM_RANGE_LEFT_COMPARE: [1, 2, -1],
               NUM_RANGE_RIGHT_COMPARE: [-1, 1, 2]
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

    @param rangeString - any match of the constants patterns defined as a range : NUM_RANGE_EXACT_COMPARE,  
    NUM_RANGE_BETWEEN_COMPARE, etc.
    @param debug - should this object print out debug infos ?
    '''
    def __init__(self, rangeString, debug=False):
        self.debug = debug
        self.parseRange(rangeString)
        
    
    def parseRange(self, rangeString):
        for x in [self.NUM_RANGE_BETWEEN_COMPARE, self.NUM_RANGE_LEFT_COMPARE, self.NUM_RANGE_RIGHT_COMPARE, self.NUM_RANGE_EXACT_COMPARE]:
            y = self.match(x, rangeString) 
            if y:
                m = self.MAPPING[x]
                left = self.getRangeValue(y, m[0]);
                operator = self.getRangeValue(y, m[1])
                right = self.getRangeValue(y, m[2])
                if self.debug:
                    print 'Matched rangeString: ', rangeString , ';  left value: ', left, ', operator: ', operator, ', right value: ', right
                self.setRangeValues(left, operator, right)
                break
            if self.debug:
                print 'Not matched: ', rangeString

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
            if self.debug:
                print 'Exact Comparison - compare value is :', x , ', matcher value is ', self.left
            return x == self.left
        else :
            if self.debug:
                print 'Between Comparison - compare value is :', x , ', matcher value on the right side is ', self.right, ' and on left side is ', self.left
            return self.COMPARATIONS['between'](self.left, self.right, x) or self.COMPARATIONS['between'](self.right, self.left, x)


class NumberRange:
    
    def __init__(self, rangeString, debug=False):
        self.rangeString = rangeString
        self.ranges = set()
        self.debug = debug
        self.initRange()

        
    def initRange(self):
        if self.debug:
            print 'initialising range'
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
        
