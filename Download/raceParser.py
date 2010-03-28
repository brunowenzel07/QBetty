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
        race.course = headline.contents[-1].strip()
        race.course = race.course.lower().capitalize()
        if re.search(" \(.*\)", race.course):
            race.course = re.sub(" \(.*\)", "", race.course)
        # Get race time
        raceDetails = headline.find(attrs = {"class":"navRace"})
        race.time = raceDetails.find(text = re.compile(r"\d+:\d+"))
        race.time = race.time.strip()
        timeMatch = re.search("(\d+):(\d+)", race.time)
        if timeMatch:
            hours = int(timeMatch.group(1))
            minutes = int(timeMatch.group(2))
            if hours < 12: hours += 12
            race.time = "%02d:%02d" % (hours, minutes)
        # Get race name
        raceDetails = soup.find("p", {"class":"raceInfo"})
        details = raceDetails.find("strong").contents[0]
        race.name = details.strip()
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
        horseDataFinder = re.compile(r"^\s*horsesData\s*=")
        dateFinder = re.compile(r'var jsRaceDate="(\d{4}-\d{2}-\d{2})"')
        horseData = "{}"
        for line in lines:
            if horseDataFinder.search(line):
                horseData = re.sub(".*?({.*}).*", r"\1", line)
            elif dateFinder.search(line):
                race.date = dateFinder.search(line).group(1)
                race.date = re.search("(\d{4})-(\d{2})-(\d{2})", race.date)
                race.date = "%s/%s/%s" % (race.date.group(3), race.date.group(2),
                                          race.date.group(1))
        horseData = json.loads(horseData)
        horseData = dict([(int(horseData[h]["no"]), horseData[h]) for h in horseData])
        horseNumbers = horseData.keys()
        horseNumbers.sort()
        for horseId in horseNumbers:
            horseHash = horseData[horseId]
            horse = race.addHorse()
            horse.name = horseHash["horseFull"]
            horse.name = horse.name.replace(r"\'", "'")
            try:
                horse.ts = int(horseHash["ts"])
            except ValueError:
                horse.ts = 0
            try:
                horse.rpr = int(horseHash["rpr"])
            except ValueError:
                horse.rpr = 0
        return race

parser = RaceParser()

def parse(raceHandle):
    return parser.parse(raceHandle)

if __name__ == "__main__":
    import glob
    for raceFile in glob.glob("testdata/race_*.html"):
        print raceFile
        handle = open(raceFile)
        try:
            race = parser.parse(handle)
        except NoRaceDataError:
            print "No valid Race Data"
            continue
        finally:
            handle.close()
        print race
        #for raceHorse in race:
        #    print raceHorse
