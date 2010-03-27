'''
Created on 27 Mar 2010

@author: Mike Thomas
'''
from Download.meetingsParser import MeetingsParser
import Download.meetingsParser
from optionSelector import optionSelector

def selectRace():
    dateList = Download.meetingsParser.rpDownloader.getAvailableDates()
    dlg = optionSelector("Select meeting date", dateList)
    if not dlg.exec_():
        return None
    date = dateList[dlg.getOptionIndex()]
    print date
    mp = MeetingsParser()
    mset = mp.parse(Download.meetingsParser.rpDownloader.getMeetingsHTML(date))
    meetings = mset.keys()
    dlg = optionSelector("Select meeting", meetings)
    if not dlg.exec_():
        return None
    meetingName = meetings[dlg.getOptionIndex()]
    print meetingName
    meeting = mset[meetingName]
    times = meeting.keys()
    dlg = optionSelector("Select race time", times)
    if not dlg.exec_():
        return None
    raceInfo = meeting[times[dlg.getOptionIndex()]]
    print raceInfo.address
    raceInfo.download()
    return raceInfo.race

if __name__ == "__main__":
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    Download.meetingsParser.setTestMode()
    import os
    os.chdir("../Download")
    race = selectRace()
    print race

