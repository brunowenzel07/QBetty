'''
Created on 2 Feb 2010

@author: Mike Thomas

'''

class OddsDisplay(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

class Round(object):
    def __init__(self, roundVal = 100):
        self.roundVal = float(roundVal)

    def convert(self, prob):
        if prob is None:
            return None
        return prob * self.roundVal / 100
