'''
Created on 1 Feb 2010

@author: Mike Thomas

'''
from Horse import Horse

class Race(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.horses = []

    def __len__(self):
        return len(self.horses)

    def __iter__(self):
        for h in self.horses: yield h

    def columnTitles(self):
        return ["Name", "RPR", "TS"]

    @property
    def numColumns(self):
        return len(self.columnTitles())

    def iterHorse(self, horse):
        yield horse.name
        yield horse.rpr
        yield horse.ts

    def addHorse(self, horse = None):
        if horse is None: horse = Horse()
        self.horses.append(horse)
        return horse

    def delHorse(self, horse):
        if isinstance(horse, int):
            hl = [h for h in self.horses if h.id == horse]
            for h in hl: self.delHorse(h)
        elif isinstance(horse, Horse):
            self.horses.remove(horse)

def EmptyRace():
    r = Race()
    r.addHorse()
    r.addHorse()
    return r


