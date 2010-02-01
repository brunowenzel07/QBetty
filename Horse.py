'''
Created on 1 Feb 2010

@author: Mike Thomas

'''

class Horse(object):
    '''
    classdocs
    '''
    __numHorses = 0

    def __init__(self, name = None):
        '''
        Constructor
        '''
        self.id = Horse.__newId()
        self.name = "Horse %d" % self.id if name is None else name
        self.rpr = 100
        self.ts = 100

    @classmethod
    def __newId(cls):
        Horse.__numHorses += 1
        return Horse.__numHorses
