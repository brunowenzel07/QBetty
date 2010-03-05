'''
Created on 5 Mar 2010

@author: Mike Thomas

'''

from BeautifulSoup import BeautifulSoup
import re
from Data import Race

def parseRaceHTML(raceHandle):
    race = Race.Race()
    lines = list(raceHandle)
    soup = BeautifulSoup("".join(lines), convertEntities = BeautifulSoup.HTML_ENTITIES)
    # Get race course
    headline = soup.find("h1", {"class":"cardHeadline"})
    race.course = headline.contents[-1].strip()
    # Get race time
    raceDetails = headline.find(attrs = {"class":"navRace"})
    race.time = raceDetails.find(text = re.compile(r"\d+:\d+"))
    race.time = race.time.strip()
    # Get race name
    raceDetails = soup.find("p", {"class":"raceInfo"})
    details = raceDetails.find("strong").contents[0]
    race.name = details.strip()
    # Get race distance
    distanceNode = raceDetails.find(text = re.compile(r"\d+m(\d+f)?"))
    distanceMatch = re.search(r"(\d+)m(\d+f)?", distanceNode)
    if distanceMatch:
        race.distance = 8 * int(distanceMatch.group(1))
        if distanceMatch.group(2) != None:
            furlongs = distanceMatch.group(2)
            race.distance += int(furlongs[0:-1])
    # Get race class
    classText = raceDetails.find(text = re.compile(r"Class", re.I))
    classMatch = re.search(r"(Class \d+)", classText, re.I)
    if classMatch:
        race.raceClass = classMatch.group(1)
    # Get race prize
    winnerText = raceDetails.find(text = re.compile(r"Winner", re.I))
    winnerMatch = re.search(u"Winner \xa3([0-9,]+)", winnerText, re.I)
    if winnerMatch:
        prize = winnerMatch.group(1)
        prize = re.sub(",", "", prize)
        race.prize = int(prize)
    # Get horse data and date
    horseDataFinder = re.compile(r"^\s*horsesData\s*=")
    dateFinder = re.compile(r'^\s*var jsRaceDate="(\d{4}-\d{2}-\d{2})"')
    horseData = "{}"
    for line in lines:
        if horseDataFinder.search(line):
            horseData = re.sub(".*?({.*}).*", r"\1", line)
        elif dateFinder.search(line):
            race.date = dateFinder.search(line).group(1)
    horseData = eval(horseData)
    horseData = dict([(int(horseData[h]["no"]), horseData[h]) for h in horseData])
    horseNumbers = horseData.keys()
    horseNumbers.sort()
    for horseId in horseNumbers:
        horseHash = horseData[horseId]
        horse = race.addHorse()
        horse.name = horseHash["horseFull"]
        try:
            horse.ts = int(horseHash["ts"])
        except ValueError:
            horse.ts = 0
        try:
            horse.rpr = int(horseHash["rpr"])
        except ValueError:
            horse.rpr = 0
    return race

if __name__ == "__main__":
    race = parseRaceHTML(open("testdata/race2.html"))
    print race
    for raceHorse in race:
        print raceHorse
