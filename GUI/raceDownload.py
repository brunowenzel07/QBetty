'''
Created on 27 Mar 2010

@author: Mike Thomas
'''
from optionSelector import optionSelector
import Download
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import Qt
def selectRace():
    QApplication.setOverrideCursor(Qt.WaitCursor)
    dateList = Download.RPDownloader.getAvailableDates()
    dlg = optionSelector("Select meeting date", dateList)
    QApplication.setOverrideCursor(Qt.ArrowCursor)
    if not dlg.exec_():
        return None
    date = dateList[dlg.getOptionIndex()]
    QApplication.setOverrideCursor(Qt.WaitCursor)
    meetingHTML = Download.RPDownloader.getMeetingsHTML(date)
    meetingSet = Download.meetingsParser.parse(meetingHTML)
    meetings = meetingSet.keys()
    dlg = optionSelector("Select meeting", meetings)
    QApplication.setOverrideCursor(Qt.ArrowCursor)
    if not dlg.exec_():
        return None
    meetingName = meetings[dlg.getOptionIndex()]
    meeting = meetingSet[meetingName]
    times = meeting.keys()
    times.sort()
    dlg = optionSelector("Select race time", times)
    if not dlg.exec_():
        return None
    raceInfo = meeting[times[dlg.getOptionIndex()]]
    QApplication.setOverrideCursor(Qt.WaitCursor)
    raceInfo.download()
    QApplication.setOverrideCursor(Qt.ArrowCursor)
    return raceInfo.race

if __name__ == "__main__":
    from PyQt4.QtGui import QApplication
    import sys
    app = QApplication(sys.argv)
    Download.RPDownloader.setTestMode()
    race = selectRace()
    print race

