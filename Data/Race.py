'''
Created on 1 Feb 2010

@author: Mike Thomas

'''
from Horse import Horse
from Adjustments import Adjustments, defaultAdjusts

class Race(object):
    '''
    classdocs
    '''

    __sigmoid = (1000, 900, 800, 667, 570, 500, 400, 333, 250, 200,
                 141, 111, 80, 66, 50, 40, 33, 30, 20, 10, 1)
    __siglen = len(__sigmoid) - 1
    __tags = (("name", unicode), ("raceClass", unicode), ("course", unicode),
              ("distance", int), ("date", unicode), ("time", unicode), ("prize", int))

    def __init__(self):
        '''
        Constructor
        '''
        self.horses = []
        self.adjusts = Adjustments()
        self.name = "Unknown"
        self.raceClass = "Unknown"
        self.course = "Unknown"
        self.distance = 0
        self.date = None
        self.time = None
        self.prize = 0

    def __len__(self):
        return len(self.horses)

    def __iter__(self):
        for h in self.horses: yield h

    def addHorse(self, horse = None):
        if horse is None: horse = Horse()
        self.horses.append(horse)
        return horse

    def insert(self, position, horse = None):
        if horse is None: horse = Horse()
        self.horses.insert(position, horse)
        return horse

    def delHorse(self, horse):
        if isinstance(horse, int):
            hl = [h for h in self.horses if h.id == horse]
            for h in hl: self.delHorse(h)
        elif isinstance(horse, Horse):
            self.horses.remove(horse)

    def calculate(self):
        if len(self) == 0: return
        if len(self) == 1:
            self[0].prob = None
            return
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

    def save(self, target):
        if isinstance(target, basestring):
            try: target = open(target, "w")
            except:
                return False
        if not isinstance(target, file):
            return False
        doc = self.getXML()
        target.write(doc.toxml())
        return True

    def load(self, target):
        if isinstance(target, basestring):
            try: target = open(target, "r")
            except:
                return False
        if not isinstance(target, file):
            return False
        #return False
        import xml.dom.minidom
        doc = xml.dom.minidom.parse(target)
        top = doc.documentElement
        for tag, tagType in self.__tags:
            for node in doc.getElementsByTagName(tag):
                if node.parentNode != top: continue
                textNode = node.firstChild
                if textNode is None: continue
                self.__setattr__(tag, tagType(textNode.nodeValue))
        for node in doc.getElementsByTagName("adjustList"):
            if node.parentNode != top: continue
            self.adjusts.readXMLTree(node)
        for node in doc.getElementsByTagName("horseList"):
            for horseNode in doc.getElementsByTagName("horse"):
                try: horseId = int(horseNode.getElementsByTagName("id").firstChild.nodeValue)
                except: horseId = None
                try: name = unicode(horseNode.getElementsByTagName("id").firstChild.nodeValue)
                except: name = None
                horse = self.addHorse(Horse(horseId, name))
                horse.readXMLTree(horseNode)
                self.adjusts.readHorseXMLTree(horse, horseNode)
        return True


    def getXML(self):
        import xml.dom.minidom
        impl = xml.dom.minidom.getDOMImplementation()
        doc = impl.createDocument(None, "race", None)
        top = doc.documentElement
        for tag, tagType in self.__tags:
            node = doc.createElement(tag)
            top.appendChild(node)
            value = self.__getattribute__(tag)
            if value is None: continue
            text = doc.createTextNode(str(value))
            node.appendChild(text)
        top.appendChild(self.adjusts.getXMLTree(doc))
        horseList = doc.createElement("horseList")
        top.appendChild(horseList)
        for horse in self:
            horseNode = horse.getXMLTree(doc)
            horseNode.appendChild(self.adjusts.getHorseXMLTree(doc, horse))
            horseList.appendChild(horseNode)
        return doc


def EmptyRace():
    emptyRace = Race()
    emptyRace.addHorse()
    emptyRace.addHorse()
    emptyRace.adjusts = defaultAdjusts()
    return emptyRace

if __name__ == "__main__":
    race = EmptyRace()
    race.adjusts.setAdjust(0, race[0], 3)
    d = race.getXML()
    print d.toprettyxml()
    race = Race()
    print race.load(r"..\GUI\test.bty")
    print race.name
    print race.raceClass
    print race.course
    print race.distance


