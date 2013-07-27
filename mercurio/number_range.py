#!/usr/bin/python
import re

'''
Created on Jul 27, 2013

@author: Tiberiu
'''  
    
EXACT = r'(\d+)'
BETWEEN = r'(\d+)[-]{1}(\d+)'
LEFT_COMPARE = r'(\d+)([=]?[<>]{1})'
RIGHT_COMPARE = r'([<>]{1}[=]?)(\d+)'  
MAPPING = {EXACT: [1, -1, -1], BETWEEN: [1, -1, 2], LEFT_COMPARE: [1, 2, -1], RIGHT_COMPARE: [-1, 1, 2]}  

COMPARATIONS = {'between':(lambda x, y, value: value >= x and value <= y), '>': (lambda x, y: x > y), '<': (lambda x, y: x < y), '>=': (lambda x, y: x >= y), '<=': (lambda x, y: x <= y)}

class RangeStatement:
    
    def __init__(self, rangeString, debug=False):
        self.debug = debug
        self.parseRange(rangeString)
        
    
    def parseRange(self, rangeString):
        for x in [BETWEEN, LEFT_COMPARE, RIGHT_COMPARE, EXACT]:
            y = self.match(x, rangeString) 
            if y:
                m = MAPPING[x]
                left = self.getRangeValue(y, m[0]);
                operator = self.getRangeValue(y, m[1])
                right = self.getRangeValue(y, m[2])
                if self.debug:
                    print 'Matched rangeString: ', rangeString , ';  left value: ', left, ', operator: ', operator, ', right value: ', right
                self.setRangeVals(left, operator, right)
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
    
    def setRangeVals(self, left, operator, right):
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
        if COMPARATIONS[self.operator]:
            func = COMPARATIONS[self.operator]
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
            return COMPARATIONS['between'](self.left, self.right, x) or COMPARATIONS['between'](self.right, self.left, x)


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
        
