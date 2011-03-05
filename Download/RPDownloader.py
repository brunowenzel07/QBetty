'''
Created on 28 Mar 2010

@author: Mike Thomas
'''
import os
from BeautifulSoup import BeautifulSoup
import re
from urllib import urlopen
import raceParser

testDataDir = os.path.join(os.path.dirname(__file__), "testdata")

def parseRaceDates(handle):
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
#        print "Getting dates from", address
        return parseRaceDates(urlopen(address))

    def getMeetingsHTML(self, date):
        address = "%s/horses2/cards/home.sd?r_date=%s" % (RPDownloader.BASE_ADDRESS, date)
#        print "Getting meetings from", address
        return urlopen(address)

    def getRaceHTML(self, info):
#        address = "%s%s" % (RPDownloader.BASE_ADDRESS, info.address)
#        print "Getting race HTML from", info.address
        return urlopen(info.address)

class MockRPDownloader(object):
    def getAvailableDates(self):
        print "Getting test dates"
        address = os.path.join(testDataDir, "meetings.html")
        return parseRaceDates(open(address))

    def getMeetingsHTML(self, date_):
        print "Getting test meetings"
        return open(os.path.join(testDataDir, "meetings.html"))

    def getRaceHTML(self, info):
        print "Getting test race"
        return open(os.path.join(testDataDir, "race_%s.html" % info.raceid))

class RaceDownloader(object):
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
        if self._downloaded:
            return
        html = rpdownloader.getRaceHTML(self)
        self.race = raceParser.parse(html)
        self._downloaded = True

def getAvailableDates():
    return rpdownloader.getAvailableDates()

def getMeetingsHTML(date):
    return rpdownloader.getMeetingsHTML(date)

def setTestMode():
    global rpdownloader
    rpdownloader = MockRPDownloader()

rpdownloader = RPDownloader()
