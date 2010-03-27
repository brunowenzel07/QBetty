'''
Created on 27 Mar 2010

@author: Mike Thomas

'''

from BeautifulSoup import BeautifulSoup
from Download import raceParser
import re
from urllib import urlopen

def parseRaceDates(handle):
    raceDates = []
    lines = list(handle)
    soup = BeautifulSoup("".join(lines), convertEntities = BeautifulSoup.HTML_ENTITIES)
    dateFinder = re.compile("cards/home.sd\?r_date=(\d+-\d+-\d+)$")
    raceDates = set([dateFinder.search(x['href']).group(1) for x in soup.findAll("a", href = dateFinder)])
    raceDates = list(raceDates)
    raceDates.sort()
    return raceDates

class RPDownloader(object):
    BASE_ADDRESS = "http://www.racingpost.com"

    def getAvailableDates(self):
        address = "%s/horses2/cards/home.sd" % (RPDownloader.BASE_ADDRESS)
        return parseRaceDates(urlopen(address))

    def getMeetingsHTML(self, date):
        address = "%s/horses2/cards/home.sd?r_date=%s" % (RPDownloader.BASE_ADDRESS, date)
        return urlopen(address)

    def getRaceHTML(self, info):
        address = "%s%s" % (RPDownloader.BASE_ADDRESS, info.address)
        return urlopen(address)

rpDownloader = RPDownloader()

class MockRPDownloader(object):
    def getAvailableDates(self):
        print "Getting test dates"
        address = "testdata/meetings.html"
        return parseRaceDates(open(address))

    def getMeetingsHTML(self, date):
        print "Getting test meetings"
        return open("testdata/meetings.html")

    def getRaceHTML(self, info):
        print "Getting test race"
        return open("testdata/race_%s.html" % info.raceid)

class RaceDownloader():

    def __init__(self, course, date, time, title, address, raceid):
        self.race = None
        self.course = course
        self.date = date
        self.time = time
        self.title = title
        self.raceid = raceid
        self.address = address
        self._downloaded = False

    def download(self):
        html = rpDownloader.getRaceHTML(self)
        self.race = raceParser.parser.parse(html)
        self._downloaded = True

class Meeting(dict):
    def __init__(self, course, date):
        super(Meeting, self).__init__()
        self.course = course
        self.date = date

    def addRace(self, time, title, address, raceid):
        self[time] = RaceDownloader(self.course, self.date,
                                          time, title, address, raceid)
        return self[time]

class MeetingSet(dict):
    def __init__(self, date = None):
        super(MeetingSet, self).__init__()
        self.date = date

    def addMeeting(self, course):
        if course in self:
            raise IndexError("Meeting already exists")
        self[course] = Meeting(course, self.date)
        return self[course]

class MeetingsParser(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass

    def parse(self, handle):
        meetings = MeetingSet()
        lines = list(handle)
        soup = BeautifulSoup("".join(lines), convertEntities = BeautifulSoup.HTML_ENTITIES)
        dateNode = soup.find("input", {"type":"hidden", "name":"r_date"})
        meetings.date = dateNode['value']
        idFinder = re.compile(r"race_id=(\d+)")
        bracketFinder = re.compile(r"\((.*)\)")
        for meetingHead in soup.findAll("div", {"class":"crBlock"}):
            meetingNode = meetingHead.find("td", {"class":"meeting"})
            try: courseName = meetingNode.find("a").contents[0].strip()
            except AttributeError: continue
            bracketMatch = bracketFinder.search(courseName)
            if bracketMatch:
                if bracketMatch.group(1) != "AW":
                    continue
                else:
                    courseName = re.sub(" \(.*\)", "", courseName)
            thisMeeting = meetings.addMeeting(courseName.capitalize())
            for raceTableNode in meetingHead.findAll("table", {"class":"cardsGrid"}):
                for tableRow in raceTableNode.findAll("tr"):
                    address = tableRow.find("a")["href"]
                    raceId = idFinder.search(address).group(1)
                    timeNode = tableRow.find("th", {"class":"rTime"}).find("a")
                    time = timeNode.contents[0].strip()
                    nameNode = tableRow.find("td", {"class":None}).find("a")
                    name = nameNode.contents[0].strip()
                    thisMeeting.addRace(time, name, address, raceId)
        return meetings

def setTestMode():
    global rpDownloader
    rpDownloader = MockRPDownloader()

if __name__ == "__main__":
    setTestMode()
    parser = MeetingsParser()
    print rpDownloader.getAvailableDates()
    mset = parser.parse(rpDownloader.getMeetingsHTML(""))
    print mset.date
    for course, meeting in mset.iteritems():
        print course
        for time, race in meeting.iteritems():
            print time, race.raceid, race.title
            try: race.download()
            except raceParser.NoRaceDataError:
                continue
            print race.race
