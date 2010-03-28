'''
Created on 27 Mar 2010

@author: Mike Thomas

'''

from BeautifulSoup import BeautifulSoup
import re
import RPDownloader

class Meeting(dict):
    def __init__(self, course, date):
        super(Meeting, self).__init__()
        self.course = course
        self.date = date

    def addRace(self, time, title, address, raceid):
        self[time] = RPDownloader.RaceDownloader(self.course, self.date,
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

__parser = MeetingsParser()
def parse(handle):
    return __parser.parse(handle)
