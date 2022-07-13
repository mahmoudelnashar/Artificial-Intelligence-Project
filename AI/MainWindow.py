from PyQt5 import QtCore, QtGui, QtWidgets
from MainWindow2 import Ui_GraphSearch

class Ui_MainWindow(object):
    def undirectedGraph(self):
        MainWindow.close()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_GraphSearch('u')
        self.ui.setupUi(self.window)
        self.window.show()


    def directedGraph(self):
        MainWindow.close()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_GraphSearch('d')
        self.ui.setupUi(self.window)
        self.window.show()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 200, 641, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.directedButton = QtWidgets.QPushButton(self.horizontalLayoutWidget, clicked = lambda: self.directedGraph())
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.directedButton.setFont(font)
        self.directedButton.setObjectName("directedButton")
        self.horizontalLayout.addWidget(self.directedButton)
        self.undirectedButton = QtWidgets.QPushButton(self.horizontalLayoutWidget, clicked = lambda: self.undirectedGraph())
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        self.undirectedButton.setFont(font)
        self.undirectedButton.setAutoDefault(False)
        self.undirectedButton.setFlat(False)
        self.undirectedButton.setObjectName("undirectedButton")
        self.horizontalLayout.addWidget(self.undirectedButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "StartupWindow"))
        self.directedButton.setText(_translate("MainWindow", "Directed Graph"))
        self.undirectedButton.setText(_translate("MainWindow", "Undirected Graph"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
