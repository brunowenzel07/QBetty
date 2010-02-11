'''
Created on 12 Feb 2010

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog
from ui_addRoundDlg import Ui_addRoundDialog

class addRoundDlg(QDialog, Ui_addRoundDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(addRoundDlg, self).__init__(parent)
        self.setupUi(self)
