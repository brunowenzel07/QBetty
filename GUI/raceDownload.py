'''
Created on 27 Mar 2010

@author: Mike Thomas
'''
from optionSelector import optionSelector
import Download
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt

class CachedDetails(object):
    dateList = None
    meetingSet = {}

details = CachedDetails()

def selectRace():
    if details.dateList is None:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        details.dateList = Download.RPDownloader.getAvailableDates()
        QApplication.setOverrideCursor(Qt.ArrowCursor)
    dlg = optionSelector("Select race date", details.dateList)
    if not dlg.exec_():
        return None
    date = details.dateList[dlg.getOptionIndex()]
    if details.meetingSet.get(date) is None:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        meetingHTML = Download.RPDownloader.getMeetingsHTML(date)
        details.meetingSet[date] = Download.meetingsParser.parse(meetingHTML)
        QApplication.setOverrideCursor(Qt.ArrowCursor)
    meetings = details.meetingSet[date].keys()
    dlg = optionSelector("Select race course", meetings)
    if not dlg.exec_():
        return None
    meetingName = meetings[dlg.getOptionIndex()]
    thisMeeting = details.meetingSet[date][meetingName]
    times = thisMeeting.keys()
    times.sort()
    dlg = optionSelector("Select race time", times)
    if not dlg.exec_():
        return None
    raceInfo = thisMeeting[times[dlg.getOptionIndex()]]
    QApplication.setOverrideCursor(Qt.WaitCursor)
    raceInfo.download()
    QApplication.setOverrideCursor(Qt.ArrowCursor)
    return raceInfo.race

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Download.RPDownloader.setTestMode()
    race = selectRace()
    print race
