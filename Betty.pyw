'''
Created on 13 Feb 2010

@author: Mike Thomas
'''

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication, QIcon, QPixmap
    import GUI.BettyGUI
    import ctypes
    myappid = 'Whatang.Betty'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(GUI.BettyGUI.APPNAME)
    icon = QIcon()
    icon.addPixmap(QPixmap(":/Icons/Horse"), QIcon.Normal, QIcon.Off)
    app.setWindowIcon(icon)
    main = GUI.BettyGUI.BettyMain()
    main.show()
    app.exec_()
