'''
Created on 2 Feb 2010

@author: Mike Thomas

'''

def numDecimals(odds):
    if odds > 10:
        return 0
    if odds > 5:
        return 1
    return 2

_fractionalOdds = [(10000, 1),
                   (5000, 1),
                   (4000, 1),
                   (2500, 1),
                   (2000, 1),
                   (1500, 1),
                   (1250, 1),
                   (1000, 1),
                   (750, 1),
                   (500, 1),
                   (400, 1),
                   (300, 1),
                   (250, 1),
                   (200, 1),
                   (175, 1),
                   (150, 1),
                   (125, 1),
                   (100, 1),
                   (80, 1),
                   (70, 1),
                   (66, 1),
                   (60, 1),
                   (50, 1),
                   (40, 1),
                   (33, 1),
                   (30, 1),
                   (28, 1),
                   (25, 1),
                   (22, 1),
                   (20, 1),
                   (19, 1),
                   (18, 1),
                   (17, 1),
                   (16, 1),
                   (15, 1),
                   (14, 1),
                   (13, 1),
                   (12, 1),
                   (11, 1),
                   (10, 1),
                   (9, 1),
                   (17, 2),
                   (8, 1),
                   (15, 2),
                   (7, 1),
                   (13, 2),
                   (6, 1),
                   (11, 2),
                   (5, 1),
                   (9, 2),
                   (4, 1),
                   (18, 5),
                   (7, 2),
                   (100, 30),
                   (16, 5),
                   (3, 1),
                   (14, 5),
                   (11, 4),
                   (13, 5),
                   (5, 2),
                   (12, 5),
                   (95, 40),
                   (23, 10),
                   (9, 4),
                   (11, 5),
                   (85, 40),
                   (21, 10),
                   (2, 1),
                   (19, 10),
                   (15, 8),
                   (9, 5),
                   (7, 4),
                   (17, 10),
                   (13, 8),
                   (8, 5),
                   (6, 4),
                   (7, 5),
                   (11, 8),
                   (13, 10),
                   (5, 4),
                   (6, 5),
                   (11, 10),
                   (21, 20),
                   (1, 1),
                   (20, 21),
                   (10, 11),
                   (9, 10),
                   (5, 6),
                   (4, 5),
                   (8, 11),
                   (7, 10),
                   (4, 6),
                   (5, 8),
                   (8, 13),
                   (3, 5),
                   (4, 7),
                   (8, 15),
                   (1, 2),
                   (40, 85),
                   (9, 20),
                   (4, 9),
                   (2, 5),
                   (4, 11),
                   (7, 20),
                   (1, 3),
                   (30, 100),
                   (2, 7),
                   (1, 4),
                   (2, 9),
                   (1, 5),
                   (2, 11),
                   (1, 6),
                   (2, 13),
                   (1, 7),
                   (2, 15),
                   (1, 8),
                   (2, 17),
                   (1, 9),
                   (1, 10),
                   (1, 11),
                   (1, 12),
                   (1, 13),
                   (1, 14),
                   (1, 15),
                   (1, 16),
                   (1, 18),
                   (1, 19),
                   (1, 20),
                   (1, 22),
                   (1, 25),
                   (1, 28),
                   (1, 30),
                   (1, 33),
                   (1, 40),
                   (1, 50),
                   (1, 60),
                   (1, 66),
                   (1, 80),
                   (1, 100),
                   (1, 125),
                   (1, 150),
                   (1, 200),
                   (1, 250),
                   (1, 300),
                   (1, 400),
                   (1, 500),
                   (1, 1000),
                   (1, 1250),
                   (1, 1500),
                   (1, 2000),
                   (1, 2500),
                   (1, 4000),
                   (1, 5000),
                   (1, 10000)]

_fractionalOdds = [(float(o[1]) / (o[0] + o[1]), "%s/%s" % o) for o in _fractionalOdds]
_fractionalOddsDict = dict(_fractionalOdds)
_fractionalOdds = [o[0] for o in _fractionalOdds]

import bisect

class OddsDisplayer(object):
    implemented = False
    @classmethod
    def display(cls, prob_):
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
            numDecimalPlaces = 0
            if odds <= 2:
                mult = 100
                numDecimalPlaces = 2
            elif odds <= 3:
                mult = 50
                numDecimalPlaces = 2
            elif odds <= 4:
                mult = 20
                numDecimalPlaces = 2
            elif odds <= 6:
                mult = 10
                numDecimalPlaces = 1
            elif odds <= 10:
                mult = 5
                numDecimalPlaces = 1
            elif odds <= 20:
                mult = 2
                numDecimalPlaces = 1
            elif odds <= 30:
                mult = 1
                numDecimalPlaces = 0
            elif odds <= 50:
                mult = 0.5
            elif odds <= 100:
                mult = 0.2
            else:
                mult = 0.1
            odds = int((odds * mult) + 0.5) / float(mult)
            return "%0.*f" % (numDecimalPlaces, odds)

class FractionalOddsDisplay(OddsDisplayer):
    implemented = True
    @classmethod
    def display(cls, prob):
        if prob is None or not isinstance(prob, float) or prob <= 0:
            return "---"
        elif prob > 1:
            return "0.00"
        else:
            nearest = bisect.bisect_left(_fractionalOdds, prob)
            return _fractionalOddsDict[_fractionalOdds[nearest]]

if __name__ == "__main__":
    for x in (0.75, 0.5, 0.25):
        print FractionalOddsDisplay.display(x)

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
