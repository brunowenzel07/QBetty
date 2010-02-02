'''
Created on 1 Feb 2010

@author: Mike Thomas

'''
from Horse import Horse
from Adjustments import Adjustments
from Data.Adjustments import defaultAdjusts

class Race(object):
    '''
    classdocs
    '''

    __sigmoid = (1000, 900, 800, 667, 570, 500, 400, 333, 250, 200,
                 141, 111, 80, 66, 50, 40, 33, 30, 20, 10, 1)
    __siglen = len(__sigmoid) - 1

    def __init__(self):
        '''
        Constructor
        '''
        self.horses = []
        self.adjusts = Adjustments()

    def __len__(self):
        return len(self.horses)

    def __iter__(self):
        for h in self.horses: yield h

    def addHorse(self, horse = None):
        if horse is None: horse = Horse()
        self.horses.append(horse)
        return horse

    def insert(self, position):
        horse = Horse()
        self.horses.insert(position, horse)
        return horse

    def delHorse(self, horse):
        if isinstance(horse, int):
            hl = [h for h in self.horses if h.id == horse]
            for h in hl: self.delHorse(h)
        elif isinstance(horse, Horse):
            self.horses.remove(horse)

    def calculate(self):
        adj = {}
        for horse in self:
            adj[horse] = []
            adj[horse].extend((rating for rname, rating in self.adjusts.iterAdjustedRatings(horse)))
        maxRatings = [max((adj[horse][i] for horse in self)) for i in xrange(0, Horse.numRatings)]
        minTrail = {}
        weight = {}
        totalWeight = 0
        for horse in self:
            minTrail[horse] = min((maxRatings[i] - adj[horse][i] for i in xrange(0, Horse.numRatings)))
            weight[horse] = self.sigmoid(minTrail[horse])
            totalWeight += weight[horse]
        for horse in self:
            try:
                horse.prob = float(weight[horse]) / totalWeight
            except ZeroDivisionError:
                horse.prob = None

    @classmethod
    def sigmoid(cls, trail):
        return cls.__sigmoid[min(cls.__siglen, trail)]

    def __getitem__(self, index):
        return self.horses[index]

def EmptyRace():
    r = Race()
    r.addHorse()
    r.addHorse()
    r.adjusts = defaultAdjusts()
    return r


