'''
Created on 1 Feb 2010

@author: Mike Thomas

'''

class Adjustments(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.__order = []
        self.__adjusts = {}

    def __len__(self):
        return len(self.__order)

    def __getitem__(self, index):
        return self.__order[index]

    def __iter__(self):
        for adjust in self.__order:
            yield adjust

    def setAdjust(self, adjust, horse, value):
        if isinstance(adjust, int):
            self.setAdjust(self[adjust], horse, value)
            return
        self.__adjusts.setdefault(adjust, {})[horse] = value

    def getAdjust(self, adjust, horse):
        if adjust in self.__adjusts:
            return self.__adjusts[adjust].get(horse, 0)
        return 0

    def iterAdjustedRatings(self, horse):
        total = sum((self.getAdjust(adjust, horse) for adjust in self.__adjusts))
        for rname, rating in horse.ratings():
            yield (rname, rating + total)

    def getAdjustedRating(self, horse, rating):
        total = sum((self.getAdjust(adjust, horse) for adjust in self.__adjusts))
        return total + horse[rating]

    def adjustments(self):
        for adjust in self.__order: yield adjust

    def addAdjustment(self, adjust):
        if adjust not in self.__adjusts:
            self.__adjusts[adjust] = {}
            self.__order.append(adjust)

    def delAdjustment(self, adjust):
        if adjust in self.__adjusts:
            del self.__adjusts[adjust]
            self.__order.remove(adjust)

    def moveUp(self, adjust):
        if adjust in self.__adjusts:
            index = self.__order.index(adjust)
            if index == 0: return
            self.__order.remove(adjust)
            self.__order.insert(index - 1, adjust)

    def moveDown(self, adjust):
        if adjust in self.__adjusts:
            index = self.__order.index(adjust)
            if index == len(self.__order) - 1: return
            self.__order.remove(adjust)
            self.__order.insert(index + 1, adjust)

    def __str__(self):
        return ",".join(self.__order)

    def getXMLTree(self, doc):
        top = doc.createElement("adjustList")
        for adjust in self.__order:
            node = doc.createElement("adjust")
            top.appendChild(node)
            text = doc.createTextNode(adjust)
            node.appendChild(text)
        return top

    def readXMLTree(self, listnode):
        for node in listnode.getElementsByTagName("adjust"):
            if node.parentNode != listnode: continue
            try: name = unicode(node.firstChild.nodeValue)
            except: continue
            self.addAdjustment(name)

    def getHorseXMLTree(self, doc, horse):
        top = doc.createElement("adjustList")
        for adjust in self.__order:
            value = self.getAdjust(adjust, horse)
            if value == 0:
                continue
            node = doc.createElement("adjust")
            node.setAttribute("name", adjust)
            top.appendChild(node)
            text = doc.createTextNode(str(value))
            node.appendChild(text)
        return top

    def readHorseXMLTree(self, horse, horsenode):
        for listnode in horsenode.getElementsByTagName("adjustList"):
            for node in listnode.getElementsByTagName("adjust"):
                try: value = int(node.firstChild.nodeValue)
                except: continue
                adjust = unicode(node.getAttribute("name"))
                self.setAdjust(adjust, horse, value)



def defaultAdjusts():
    ads = Adjustments()
    ads.addAdjustment("Form")
    ads.addAdjustment("Course")
    ads.addAdjustment("Distance")
    return ads

if __name__ == "__main__":
    ads = Adjustments()
    ads.addAdjustment("a")
    print ads
    ads.addAdjustment("b")
    print ads
    ads.addAdjustment("a")
    print ads
    ads.addAdjustment("c")
    ads.addAdjustment("d")
    print ads
    ads.moveUp("b")
    print ads
    ads.moveUp("b")
    print ads
    print ads
    ads.moveDown("c")
    print ads
    ads.moveDown("c")
    print ads
    ads.moveUp("x")
    print ads
    from Horse import Horse
    h = Horse()
    for rname, rating in ads.iterAdjustedRatings(h):
        print rname, rating
    ads.setAdjust("a", h, 3)
    for rname, rating in ads.iterAdjustedRatings(h):
        print rname, rating
    ads.setAdjust("b", h, -2)
    for rname, rating in ads.iterAdjustedRatings(h):
        print rname, rating
