'''
Created on 5 Mar 2010

@author: Mike Thomas

'''

from BeautifulSoup import BeautifulSoup
import re
import json
from Data import Race

class NoRaceDataError(Exception):
    pass

class RaceParser(object):
    def parse(self, raceHandle):
        race = Race.Race()
        lines = list(raceHandle)
        soup = BeautifulSoup("".join(lines), convertEntities = BeautifulSoup.HTML_ENTITIES)
        # Get race course
        headline = soup.find("h1", {"class":"cardHeadline"})
        if not headline:
            raise NoRaceDataError()
        race.course = headline.find("span", {"class":"placeRace"}).contents[0].strip()
        race.course = race.course.lower().capitalize()
        if re.search(r" \(.*\)", race.course):
            race.course = re.sub(r" \(.*\)", "", race.course)
        # Get race time
        raceDetails = headline.find(attrs = {"class":"navRace"})
        race.time = raceDetails.find(text = re.compile(r"\d+:\d+"))
        race.time = race.time.strip()
        timeMatch = re.search(r"(\d+):(\d+)", race.time)
        if timeMatch:
            hours = int(timeMatch.group(1))
            minutes = int(timeMatch.group(2))
            if hours < 12: hours += 12
            race.time = "%02d:%02d" % (hours, minutes)
        # Get race name
        raceDetails = soup.find("div", {"class":"raceInfo clearfix"})
        details = raceDetails.findAll("strong")
        for element in details:
            if element.contents:
                race.name = element.contents[0].strip()
                break
        # Get race distance
        distanceNode = raceDetails.find(text = re.compile(r"(\d+m(\d+f)?)|(\d+f)"))
        if distanceNode:
            distanceMatch = re.search(r"(\d+)m", distanceNode)
            if distanceMatch:
                race.distance = 8 * int(distanceMatch.group(1))
            distanceMatch = re.search(r"(\d+)f", distanceNode)
            if distanceMatch:
                race.distance += int(distanceMatch.group(1))
        # Get race class
        classText = raceDetails.find(text = re.compile(r"Class", re.I))
        if classText:
            classMatch = re.search(r"(Class \d+)", classText, re.I)
            if classMatch:
                race.raceClass = classMatch.group(1).lower().capitalize()
            # Get race prize
        winnerText = raceDetails.find(text = re.compile(r"Winner", re.I))
        if winnerText:
            winnerMatch = re.search(u"Winner \xa3([0-9,]+)", winnerText, re.I)
            if winnerMatch:
                prize = winnerMatch.group(1)
                prize = re.sub(",", "", prize)
                race.prize = int(prize)
        # Get horse data and date
        cardInit = re.compile(r'www\.horses\.card\.init\((.*)\);\}\);')
        horseData = None
        for line in lines:
            if cardInit.search(line):
                match = cardInit.search(line)
                data = match.group(1)
                data = json.loads(data)
                horseData = data['horsesData']
                race.date = data['raceDate']
                race.date = re.search(r"(\d{4})-(\d{2})-(\d{2})", race.date)
                race.date = "%s/%s/%s" % (race.date.group(3), race.date.group(2),
                                          race.date.group(1))
                break
        horseData = dict([(int(h[1:]), horseData[h]) for h in horseData])
        horseNumbers = horseData.keys()
        horseNumbers.sort()
        for horseId in horseNumbers:
            horseHash = horseData[horseId]
            horse = race.addHorse(horseId = horseId)
            horse.name = BeautifulSoup(horseHash["horse"],
                                       convertEntities = BeautifulSoup.HTML_ENTITIES).contents[0]
            horse.name = horse.name.title()
            try:
                horse.ts = int(horseHash["topspeed"])
                if horse.ts == -1:
                    horse.ts = 0
            except ValueError:
                horse.ts = 0
            try:
                horse.rpr = int(horseHash["rprating"])
                if horse.rpr == -1:
                    horse.rpr = 0
            except ValueError:
                horse.rpr = 0
        return race

parser = RaceParser()

def parse(raceHandle):
    return parser.parse(raceHandle)


def testmain():
    import glob
    for raceFile in glob.glob("testdata/race_57*.html"):
        print raceFile
        handle = open(raceFile)
        try:
            race = parser.parse(handle)
            for horse in race:
                print horse
        except NoRaceDataError:
            print "No valid Race Data"
            continue
        finally:
            handle.close()
        print race
        #for raceHorse in race:
        #    print raceHorse


if __name__ == "__main__":
    testmain()
