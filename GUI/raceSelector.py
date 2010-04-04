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

details = CachedDetails()

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
        if details.dateList is None:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            details.dateList = Download.RPDownloader.getAvailableDates()
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.setupUi(self)
        self.populateDates()
        if details.selectedDate is not None:
            try:
                index = details.dateList.index(details.selectedDate)
            except ValueError:
                return
            self.dateList.setCurrentRow(index)
            if details.selectedMeeting is not None:
                try:
                    index = details.meetings.index(details.selectedMeeting)
                except ValueError:
                    return
                self.courseList.setCurrentRow(index)
        self.connect(self, SIGNAL("accepted()"), self.on_raceSelector_accepted)

    def populateDates(self):
        populateList(self.dateList, details.dateList)

    def populateCourses(self):
        if details.meetingSet.get(details.selectedDate) is None:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            meetingHTML = Download.RPDownloader.getMeetingsHTML(details.selectedDate)
            details.meetingSet[details.selectedDate] = Download.meetingsParser.parse(meetingHTML)
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        details.meetings = details.meetingSet[details.selectedDate].keys()
        details.meetings.sort()
        populateList(self.courseList, details.meetings)

    def populateRaces(self):
        details.thisMeeting = details.meetingSet[details.selectedDate][details.selectedMeeting]
        details.times = details.thisMeeting.keys()
        details.times.sort()
        populateList(self.timeList, details.times)

    @pyqtSignature("")
    def on_dateList_itemSelectionChanged(self):
        details.selectedDate = details.dateList[self.dateList.currentRow()]
        self.populateCourses()

    @pyqtSignature("")
    def on_courseList_itemSelectionChanged(self):
        details.selectedMeeting = details.meetings[self.courseList.currentRow()]
        self.populateRaces()

    def on_raceSelector_accepted(self):
        details.selectedRace = details.times[self.timeList.currentRow()]
        raceInfo = details.thisMeeting[details.selectedRace]
        QApplication.setOverrideCursor(Qt.WaitCursor)
        raceInfo.download()
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        self.race = raceInfo.race

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Download.RPDownloader.setTestMode()
    dlg = raceSelector()
    dlg.exec_()
