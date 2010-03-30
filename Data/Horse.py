'''
Created on 1 Feb 2010

@author: Mike Thomas

'''

def cmpHorseByInsertion(horseA, horseB):
    return (horseA.id - horseB.id)

def cmpHorseByName(horseA, horseB):
    na = horseA.name.lower()
    nb = horseB.name.lower()
    if na < nb:
        return - 1
    elif na == nb:
        return 1
    else:
        return 0

def cmpHorseByOdds(horseA, horseB):
    if horseA.prob > horseB.prob:
        return - 1
    elif horseA.prob == horseB.prob:
        return 0
    else:
        return 1

horseSortMap = [("insertion", cmpHorseByInsertion),
                ("name", cmpHorseByName),
                ("odds", cmpHorseByOdds)]
horseSortList = [s[0] for s in horseSortMap]
horseSortMap = dict(horseSortMap)


class Horse(object):
    '''
    classdocs
    '''
    __numHorses = 0
    numRatings = 2
    __tags = (("id", int), ("name", unicode))
    __ratingMap = ["rpr", "ts"]
    ratingTitles = ["RPR", "Topspeed"]

    def __init__(self, horseId = None, name = None, **kws):
        '''
        Constructor
        '''
        self.id = Horse.__newId(horseId)
        self.name = "Horse %d" % self.id if name is None else name
        for rname in self.__ratingMap:
            if rname in kws:
                self.__setattr__(rname, kws[rname])
            else:
                self.__setattr__(rname, 100)
        self.prob = None

    def __str__(self):
        ret = str(self.name)
        for rname in self.__ratingMap:
            ret += ",%d" % self.__getattribute__(rname)
        return ret

    @classmethod
    def __newId(cls, horseId):
        if horseId is None:
            horseId = Horse.__numHorses + 1
        if horseId > Horse.__numHorses:
            Horse.__numHorses = horseId
        return horseId

    def ratings(self):
        for rname in self.__ratingMap:
            yield (rname, self.__getattribute__(rname))

    def __hash__(self):
        return self.id

    def __getitem__(self, index):
        return self.__getattribute__(self.__ratingMap[index])

    def __setitem__(self, index, value):
        self.__setattr__(self.__ratingMap[index], value)

    def getXMLTree(self, doc):
        top = doc.createElement("horse")
        for tag in (t[0] for t in self.__tags):
            node = doc.createElement(tag)
            top.appendChild(node)
            value = self.__getattribute__(tag)
            if value is not None:
                text = doc.createTextNode(str(value))
                node.appendChild(text)
        for tag in self.__ratingMap:
            node = doc.createElement(tag)
            top.appendChild(node)
            value = self.__getattribute__(tag)
            if value is not None:
                text = doc.createTextNode(str(value))
                node.appendChild(text)
        return top

    def readXMLTree(self, horseNode):
        for tag, tagType in self.__tags:
            for node in horseNode.getElementsByTagName(tag):
                if node.parentNode != horseNode: continue
                textNode = node.firstChild
                if textNode is None: continue
                self.__setattr__(tag, tagType(textNode.nodeValue))
        for tag in self.__ratingMap:
            for node in horseNode.getElementsByTagName(tag):
                if node.parentNode != horseNode: continue
                textNode = node.firstChild
                if textNode is None: continue
                self.__setattr__(tag, int(textNode.nodeValue))
