'''
Created on 2 Feb 2010

@author: Mike Thomas

'''

class DecimalOddsDisplay(object):
    '''
    classdocs
    '''


    @classmethod
    def display(cls, prob):
        if prob is None or not isinstance(prob, float) or prob <= 0:
            return "---"
        elif prob > 1:
            return "0.00"
        else:
            return "%0.2f" % ((1 - prob) / prob)

class BetfairOddsDisplay(object):
    @classmethod
    def display(cls, prob):
        if prob is None or not isinstance(prob, float) or prob <= 0:
            return "---"
        elif prob > 1:
            return "0.00"
        else:
            return "%0.2f" % (1 + ((1 - prob) / prob))

class FractionalOddsDisplay(object):
    @classmethod
    def display(cls, prob):
        if prob is None or not isinstance(prob, float) or prob <= 0:
            return "---"
        elif prob > 1:
            return "0.00"
        else:
            return "x/y"



class Round(object):
    def __init__(self, roundVal = 100):
        self.roundVal = float(roundVal)

    def convert(self, prob):
        if prob is None:
            return None
        return prob * self.roundVal / 100
