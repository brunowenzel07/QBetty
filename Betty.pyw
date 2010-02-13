'''
Created on 13 Feb 2010

@author: Mike Thomas
'''

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    from GUI.BettyGUI import BettyMain, appName
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(appName)
    main = BettyMain()
    main.show()
    app.exec_()
