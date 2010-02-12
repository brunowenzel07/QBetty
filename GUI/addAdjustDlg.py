'''
Created on 12 Feb 2010

@author: Mike Thomas

'''

from PyQt4.QtGui import QDialog
from ui_addAdjustDlg import Ui_addAdjustDialog

class addAdjustDlg(Ui_addAdjustDialog, QDialog):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(addAdjustDlg, self).__init__(parent)
        self.setupUi(self)
