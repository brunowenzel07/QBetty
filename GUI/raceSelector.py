'''
Created on 4 Apr 2010

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog, QApplication
from PyQt4.QtCore import Qt, pyqtSignature, QString, SIGNAL
from ui_raceSelector import Ui_raceSelector
import Download

class CachedDetails(object):
    dateList = None
    meetingSet = {}
    meetings = None
    times = None
    selectedDate = None
    selectedMeeting = None
    thisMeeting = None
    selectedRace = None

_DETAILS = CachedDetails()

def populateList(listWidget, contents):
    listWidget.clear()
    listWidget.setSortingEnabled(False)
    for item in contents:
        listWidget.addItem(QString(item))

class raceSelector(Ui_raceSelector, QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(raceSelector, self).__init__(parent)
        if _DETAILS.dateList is None:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            _DETAILS.dateList = Download.RPDownloader.getAvailableDates()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.setupUi(self)
        self.populateDates()
        if _DETAILS.selectedDate is not None:
            try:
                index = _DETAILS.dateList.index(_DETAILS.selectedDate)
            except ValueError:
                return
            self.dateList.setCurrentRow(index)
            if _DETAILS.selectedMeeting is not None:
                try:
                    index = _DETAILS.meetings.index(_DETAILS.selectedMeeting)
                except ValueError:
                    return
                self.courseList.setCurrentRow(index)
        self.race = None
        self.connect(self, SIGNAL("accepted()"), self.on_raceSelector_accepted)

    def populateDates(self):
        populateList(self.dateList, _DETAILS.dateList)

    def populateCourses(self):
        if _DETAILS.meetingSet.get(_DETAILS.selectedDate) is None:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            meetingHTML = Download.RPDownloader.getMeetingsHTML(_DETAILS.selectedDate)
            _DETAILS.meetingSet[_DETAILS.selectedDate] = Download.meetingsParser.parse(meetingHTML)
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        _DETAILS.meetings = _DETAILS.meetingSet[_DETAILS.selectedDate].keys()
        _DETAILS.meetings.sort()
        populateList(self.courseList, _DETAILS.meetings)

    def populateRaces(self):
        _DETAILS.thisMeeting = _DETAILS.meetingSet[_DETAILS.selectedDate][_DETAILS.selectedMeeting]
        _DETAILS.times = _DETAILS.thisMeeting.keys()
        _DETAILS.times.sort()
        populateList(self.timeList, _DETAILS.times)

    @pyqtSignature("")
    def on_dateList_itemSelectionChanged(self):
        _DETAILS.selectedDate = _DETAILS.dateList[self.dateList.currentRow()]
        self.populateCourses()

    @pyqtSignature("")
    def on_courseList_itemSelectionChanged(self):
        _DETAILS.selectedMeeting = _DETAILS.meetings[self.courseList.currentRow()]
        self.populateRaces()

    def on_raceSelector_accepted(self):
        _DETAILS.selectedRace = _DETAILS.times[self.timeList.currentRow()]
        raceInfo = _DETAILS.thisMeeting[_DETAILS.selectedRace]
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            raceInfo.download()
            self.race = raceInfo.race
        finally:
            QApplication.setOverrideCursor(Qt.ArrowCursor)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Download.RPDownloader.setTestMode()
    dlg = raceSelector()
    dlg.exec_()
