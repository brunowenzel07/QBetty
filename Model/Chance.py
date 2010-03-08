'''
Created on 2 Feb 2010

@author: Mike Thomas

'''

def numDecimals(x):
    if x > 10:
        return 0
    if x > 5: return 1
    return 2

class OddsDisplayer(object):
    implemented = False
    @classmethod
    def display(cls, prob):
        return "---"

class DecimalOddsDisplay(OddsDisplayer):
    '''
    classdocs
    '''

    implemented = True

    @classmethod
    def display(cls, prob):
        if prob is None or not isinstance(prob, float) or prob <= 0:
            return "---"
        elif prob > 1:
            return "0.00"
        else:
            odds = (1 - prob) / prob
            return "%0.*f" % (numDecimals(odds), odds)

class BetfairOddsDisplay(OddsDisplayer):
    implemented = True
    @classmethod
    def display(cls, prob):
        if prob is None or not isinstance(prob, float) or prob <= 0:
            return "---"
        elif prob > 1:
            return "0.00"
        else:
            odds = (1 + ((1 - prob) / prob))
            numDecimals = 0
            if odds <= 2:
                mult = 100
                numDecimals = 2
            elif odds <= 3:
                mult = 50
                numDecimals = 2
            elif odds <= 4:
                mult = 20
                numDecimals = 2
            elif odds <= 6:
                mult = 10
                numDecimals = 1
            elif odds <= 10:
                mult = 5
                numDecimals = 1
            elif odds <= 20:
                mult = 2
                numDecimals = 1
            elif odds <= 30:
                mult = 1
                numDecimals = 0
            elif odds <= 50:
                mult = 0.5
            elif odds <= 100:
                mult = 0.2
            else:
                mult = 0.1
            odds = int((odds * mult) + 0.5) / float(mult)
            return "%0.*f" % (numDecimals, odds)

class FractionalOddsDisplay(OddsDisplayer):
    @classmethod
    def display(cls, prob):
        if prob is None or not isinstance(prob, float) or prob <= 0:
            return "---"
        elif prob > 1:
            return "0.00"
        else:
            return "---/---"

oddsList = ("decimal", "betfair", "fractional")
oddsMap = {"decimal":DecimalOddsDisplay,
           "betfair":BetfairOddsDisplay,
           "fractional":FractionalOddsDisplay}


class Round(object):
    def __init__(self, roundVal = 100):
        self.roundVal = float(roundVal)

    def convert(self, prob):
        if prob is None:
            return None
        return prob * self.roundVal / 100
