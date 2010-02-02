'''
Created on 1 Feb 2010

@author: Mike Thomas

'''

class Horse(object):
    '''
    classdocs
    '''
    __numHorses = 0
    numRatings = 2
    __ratingMap = ["rpr", "ts"]
    ratingTitles = ["RPR", "Topspeed"]

    def __init__(self, name = None, **kws):
        '''
        Constructor
        '''
        self.id = Horse.__newId()
        self.name = "Horse %d" % self.id if name is None else name
        for rname in self.__ratingMap:
            if rname in kws:
                self.__setattr__(rname, kws[rname])
            else:
                self.__setattr__(rname, 100)
        self.prob = None

    @classmethod
    def __newId(cls):
        Horse.__numHorses += 1
        return Horse.__numHorses

    def ratings(self):
        for rname in self.__ratingMap:
            yield (rname, self.__getattribute__(rname))

    def __hash__(self):
        return self.id

    def __getitem__(self, index):
        return self.__getattribute__(self.__ratingMap[index])

    def __setitem__(self, index, value):
        self.__setattr__(self.__ratingMap[index], value)
