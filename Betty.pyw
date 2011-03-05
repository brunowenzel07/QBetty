'''
Created on 13 Feb 2010

@author: Mike Thomas
'''

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
    import GUI.BettyGUI
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(GUI.BettyGUI.APPNAME)
    main = GUI.BettyGUI.BettyMain()
    main.show()
    app.exec_()
