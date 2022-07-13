from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import Algorithms as alg
from pyvisCode import pyvisGraphGenerator, legend_creator

class Ui_GraphSearch(object):
    def __init__(self, mode):
        self.mode = mode
        self.nodes = []
        self.edges = []
        self.adjacencyList = []
        self.start = None
        self.goals = None
        self.visited = None
        self.path = None

    def legend_creator(self):
        legend_creator('Graph.html')
        with open('Graph.html', 'r')as f:
            htmlFile = f.read()
            self.webEngineView3.setHtml(htmlFile)

    def generateAdjList(self):
        self.adjacencyList = []
        for x in self.nodes:
            adj = []
            for e in self.edges:
                if x[0] == e[0]:
                    adj.append((e[1], e[2]))
                if self.mode == 'u' and x[0] == e[1]:
                    adj.append((e[0], e[2]))
            self.adjacencyList.append((x[0], adj))

    def redrawGraph(self):
        pyvisGraphGenerator('Graph.html', self.nodes, self.edges, self.mode, self.goals, self.visited, self.path)
        # open the html file in the webengine widget
        with open('Graph.html', 'r')as f:
            htmlFile = f.read()
            self.webEngineView.setHtml(htmlFile)


    def insertNodeClicked(self):
        nodes = [e[0] for e in self.nodes]
        node = self.nodeNameIN.text()
        heuristic = self.nodeHeuristicIN.text()
        if node == '' or heuristic == '':
            return
        if not heuristic.isdigit():
            self.showWarrningMsg('Heuristic invalid, heuristic must be non-negative number')
            self.nodeHeuristicIN.clear()
            return
        heuristic = float(heuristic)
        # validate the nodes and heuristic
        if node in nodes:
            self.showWarrningMsg("Node already in graph can't add node")
            self.nodeNameIN.clear()
            return
        if heuristic < 0:
            self.showWarrningMsg('Heuristic invalid, heuristic must be non-negative number')
            self.nodeHeuristicIN.clear()
            return
        self.nodes.append((node, heuristic))
        self.nodeNameIN.clear()
        self.nodeHeuristicIN.clear()
        self.redrawGraph()


    def deleteNodeClicked(self):
        nodes = [e[0] for e in self.nodes]
        node = self.nodeNameDelete.text()
        if node == '':
            return
        self.nodeNameDelete.clear()
        if node not in nodes:
            self.showWarrningMsg('Node already not in graph.')
            return
        # node in graph we need to remove node and all edges connected to it
        for n in nodes:
            if node == n:
                index = nodes.index(n)
                del self.nodes[index]
        for e in self.edges:
            if node == e[0] or node == e[1]:
                self.edges.remove(e)
            if node == e[1]:
                self.edges.remove(e)
        self.redrawGraph()


    def insertEdgeClicked(self):
        start = self.edgeStartNodeIN.text()
        end = self.edgeEndNodeIN.text()
        weight = self.edgeWeightIN.text()
        if start == '' or end == '' or weight == '':
            return
        if not weight.isdigit():
            self.showWarrningMsg('Weight invalid, weight must be positive number')
            self.nodeHeuristicIN.clear()
            return
        weight = float(weight)
        nodes = [e[0] for e in self.nodes]
        if start not in nodes:
            self.showWarrningMsg('Start node not in graph, enter start node first')
            self.edgeStartNodeIN.clear()
            return
        if end not in nodes:
            self.showWarrningMsg('End node not in graph, enter end node first')
            self.edgeEndNodeIN.clear()
            return
        if weight <= 0:
            self.showWarrningMsg('Weight invalid, weight must be positive number')
            self.edgeWeightIN.clear()
            return
        for e in self.edges:
            if start == e[0] and end == e[1]:
                self.showWarrningMsg('Edge already in graph')
                self.edgeStartNodeIN.clear()
                self.edgeEndNodeIN.clear()
                return
            if self.mode == 'u' and start == e[1] and end == e[0]:
                self.showWarrningMsg('Edge already in graph')
                self.edgeStartNodeIN.clear()
                self.edgeEndNodeIN.clear()
                return
        self.edges.append((start, end, weight))
        self.edgeStartNodeIN.clear()
        self.edgeEndNodeIN.clear()
        self.edgeWeightIN.clear()
        self.redrawGraph()


    def deleteEdgeClicked(self):
        start = self.edgeStartNodeDelete.text()
        end = self.edgeEndNodeDelete.text()
        if start == '' or end == '':
            return
        for e in self.edges:
            if start == e[0] and end == e[1]:
                self.edges.remove(e)
                self.edgeStartNodeDelete.clear()
                self.edgeEndNodeDelete.clear()
                self.redrawGraph()
                print('deleteEdge')
                print(self.edges)
                return
            if self.mode == 'u' and start == e[1] and end == e[0]:
                self.edges.remove(e)
                self.edgeStartNodeDelete.clear()
                self.edgeEndNodeDelete.clear()
                self.redrawGraph()
                print('deleteEdge')
                print(self.edges)
                return
        self.showWarrningMsg('Edge not found')



    def showWarrningMsg(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec_()

    def finishDataEntryClicked(self):
        nodes = [e[0] for e in self.nodes]
        # taking the start
        start = self.startIN.text()
        # validate the start
        if start not in nodes:
            self.showWarrningMsg("Start not in graph")
            self.startIN.clear()
            return
        # taking the goals
        goals = [e for e in self.goalsIN.text().split(',')]
        for e in goals:
            if e == " ":
                goals.remove(e)
        #  validate goals
        for x in goals:
            if x not in nodes:
                self.showWarrningMsg("Node(s) in goal list are not in graph")
                self.goalsIN.clear()
                return
        # start and goals are validated
        self.start = start
        self.goals = goals
        self.startLabel.setText('Start: '+str(start))
        self.goalsLabel.setText('Goals: '+str(goals))
        self.startIN.clear()
        self.goalsIN.clear()
        #redraw the graph
        self.redrawGraph()
        #generate the adjacency list
        self.generateAdjList()
        # reconfiguring the buttons and text boxes
        # textboxes
        self.nodeNameIN.setEnabled(False)
        self.nodeHeuristicIN.setEnabled(False)
        self.nodeNameDelete.setEnabled(False)
        self.edgeStartNodeIN.setEnabled(False)
        self.edgeEndNodeIN.setEnabled(False)
        self.edgeWeightIN.setEnabled(False)
        self.edgeStartNodeDelete.setEnabled(False)
        self.edgeEndNodeDelete.setEnabled(False)
        self.startIN.setEnabled(False)
        self.goalsIN.setEnabled(False)
        # buttons
        self.insertNodeButton.setEnabled(False)
        self.deleteNodeButton.setEnabled(False)
        self.insertEdgeButton.setEnabled(False)
        self.deleteEgeButton.setEnabled(False)
        self.finishDataEntryButton.setEnabled(False)
        self.BFSButton.setEnabled(True)
        self.DFSButton.setEnabled(True)
        self.IDSButton.setEnabled(True)
        self.UCSButton.setEnabled(True)
        self.GreedyButton.setEnabled(True)
        self.astarButton.setEnabled(True)
        self.searchAgainButton.setEnabled(False)
        self.modifyDataButton.setEnabled(True)
        self.legend_creator()

    # ------------------------------------------------ Search Functions-------------------------------------------------
    def BFSClicked(self):
        self.path, self.visited = alg.BFS(self.adjacencyList,self.start,self.goals)
        self.redrawGraph()
        self.searchIsExecuted()
        self.visited_lab.setText('Visited Nodes: ' + str(self.visited))
        self.path_lab.setText('Solution Path: ' + str(self.path))

    def DFSClicked(self):
        self.path, self.visited = alg.DFS(self.adjacencyList,self.start,self.goals)
        self.redrawGraph()
        self.searchIsExecuted()
        self.visited_lab.setText('Visited Nodes: ' + str(self.visited))
        self.path_lab.setText('Solution Path: ' + str(self.path))

    def IDSClicked(self):
        self.path, trash, self.visited = alg.IDS(self.adjacencyList,self.start,self.goals)
        self.redrawGraph()
        self.searchIsExecuted()
        self.visited_lab.setText('Visited Nodes: ' + str(self.visited))
        self.path_lab.setText('Solution Path: ' + str(self.path))

    def UCSClicked(self):
        self.path, self.visited = alg.UCS(self.adjacencyList,self.start,self.goals)
        self.redrawGraph()
        self.searchIsExecuted()
        self.visited_lab.setText('Visited Nodes: ' + str(self.visited))
        self.path_lab.setText('Solution Path: ' + str(self.path))

    def GreedyClicked(self):
        self.path, self.visited = alg.GreedySearch(self.nodes, self.adjacencyList, self.start, self.goals)
        self.redrawGraph()
        self.searchIsExecuted()
        self.visited_lab.setText('Visited Nodes: ' + str(self.visited))
        self.path_lab.setText('Solution Path: ' + str(self.path))

    def AstarClicked(self):
        self.path, self.visited = alg.AstarSearch(self.nodes, self.adjacencyList, self.start, self.goals)
        self.redrawGraph()
        self.searchIsExecuted()
        self.visited_lab.setText('Visited Nodes: ' + str(self.visited))
        self.path_lab.setText('Solution Path: ' + str(self.path))

    def searchIsExecuted(self):
        self.BFSButton.setEnabled(False)
        self.DFSButton.setEnabled(False)
        self.IDSButton.setEnabled(False)
        self.UCSButton.setEnabled(False)
        self.GreedyButton.setEnabled(False)
        self.astarButton.setEnabled(False)
        self.searchAgainButton.setEnabled(True)
        self.modifyDataButton.setEnabled(True)

    def modifyDataPressed(self):
        # textboxes
        self.nodeNameIN.setEnabled(True)
        self.nodeHeuristicIN.setEnabled(True)
        self.nodeNameDelete.setEnabled(True)
        self.edgeStartNodeIN.setEnabled(True)
        self.edgeEndNodeIN.setEnabled(True)
        self.edgeWeightIN.setEnabled(True)
        self.edgeStartNodeDelete.setEnabled(True)
        self.edgeEndNodeDelete.setEnabled(True)
        self.startIN.setEnabled(True)
        self.goalsIN.setEnabled(True)
        # buttons
        self.insertNodeButton.setEnabled(True)
        self.deleteNodeButton.setEnabled(True)
        self.insertEdgeButton.setEnabled(True)
        self.deleteEgeButton.setEnabled(True)
        self.finishDataEntryButton.setEnabled(True)
        self.BFSButton.setEnabled(False)
        self.DFSButton.setEnabled(False)
        self.IDSButton.setEnabled(False)
        self.UCSButton.setEnabled(False)
        self.GreedyButton.setEnabled(False)
        self.astarButton.setEnabled(False)
        self.searchAgainButton.setEnabled(False)
        self.modifyDataButton.setEnabled(False)

    def searchAgainPressed(self):
        self.BFSButton.setEnabled(True)
        self.DFSButton.setEnabled(True)
        self.IDSButton.setEnabled(True)
        self.UCSButton.setEnabled(True)
        self.GreedyButton.setEnabled(True)
        self.astarButton.setEnabled(True)
        self.searchAgainButton.setEnabled(False)
        self.modifyDataButton.setEnabled(True)
        self.path = None
        self.visited = None
        self.redrawGraph()

    def setupUi(self, GraphSearch):
        GraphSearch.setObjectName("GraphSearch")
        GraphSearch.resize(1550, 900)
        self.centralwidget = QtWidgets.QWidget(GraphSearch)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 20, 391, 761))
        self.groupBox_3.setObjectName("groupBox_3")
        self.frame = QtWidgets.QFrame(self.groupBox_3)
        self.frame.setGeometry(QtCore.QRect(-10, 20, 391, 741))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(80, 310, 211, 211))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 30, 166, 161))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.BFSButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2, clicked=lambda: self.BFSClicked())
        self.BFSButton.setEnabled(False)
        self.BFSButton.setObjectName("BFSButton")
        self.verticalLayout_2.addWidget(self.BFSButton)
        self.DFSButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2, clicked=lambda: self.DFSClicked())
        self.DFSButton.setEnabled(False)
        self.DFSButton.setObjectName("DFSButton")
        self.verticalLayout_2.addWidget(self.DFSButton)
        self.IDSButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2, clicked=lambda: self.IDSClicked())
        self.IDSButton.setEnabled(False)
        self.IDSButton.setObjectName("IDSButton")
        self.verticalLayout_2.addWidget(self.IDSButton)
        self.UCSButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2, clicked=lambda: self.UCSClicked())
        self.UCSButton.setEnabled(False)
        self.UCSButton.setObjectName("UCSButton")
        self.verticalLayout_2.addWidget(self.UCSButton)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setGeometry(QtCore.QRect(80, 530, 211, 121))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(30, 30, 161, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.GreedyButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3, clicked=lambda: self.GreedyClicked())
        self.GreedyButton.setEnabled(False)
        self.GreedyButton.setObjectName("GreedyButton")
        self.verticalLayout_3.addWidget(self.GreedyButton)
        self.astarButton = QtWidgets.QPushButton(self.verticalLayoutWidget_3, clicked=lambda: self.AstarClicked())
        self.astarButton.setEnabled(False)
        self.astarButton.setObjectName("astarButton")
        self.verticalLayout_3.addWidget(self.astarButton)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(120, 660, 131, 65))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.searchAgainButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4,
                                                       clicked=lambda: self.searchAgainPressed())
        self.searchAgainButton.setEnabled(False)
        self.searchAgainButton.setObjectName("searchAgainButton")
        self.verticalLayout_4.addWidget(self.searchAgainButton)
        self.modifyDataButton = QtWidgets.QPushButton(self.verticalLayoutWidget_4,
                                                      clicked=lambda: self.modifyDataPressed())
        self.modifyDataButton.setEnabled(False)
        self.modifyDataButton.setObjectName("modifyDataButton")
        self.verticalLayout_4.addWidget(self.modifyDataButton)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(20, 230, 351, 61))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.startLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.startLabel.setObjectName("startLabel")
        self.verticalLayout_5.addWidget(self.startLabel)
        self.goalsLabel = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.goalsLabel.setObjectName("goalsLabel")
        self.verticalLayout_5.addWidget(self.goalsLabel)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 351, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.nodeNameIN = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Node name")
        self.nodeNameIN.setObjectName("nodeNameIN")
        self.horizontalLayout_5.addWidget(self.nodeNameIN)
        self.nodeHeuristicIN = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Node heuristic")
        self.nodeHeuristicIN.setObjectName("nodeHeuristicIN")
        self.horizontalLayout_5.addWidget(self.nodeHeuristicIN)
        self.insertNodeButton = QtWidgets.QPushButton(self.verticalLayoutWidget,
                                                      clicked=lambda: self.insertNodeClicked())
        self.insertNodeButton.setObjectName("insertNodeButton")
        self.horizontalLayout_5.addWidget(self.insertNodeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.nodeNameDelete = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Node name")
        self.nodeNameDelete.setObjectName("nodeNameDelete")
        self.horizontalLayout_2.addWidget(self.nodeNameDelete)
        self.deleteNodeButton = QtWidgets.QPushButton(self.verticalLayoutWidget,
                                                      clicked=lambda: self.deleteNodeClicked())
        self.deleteNodeButton.setObjectName("deleteNodeButton")
        self.horizontalLayout_2.addWidget(self.deleteNodeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.edgeStartNodeIN = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Start Node")
        self.edgeStartNodeIN.setObjectName("edgeStartNodeIN")
        self.horizontalLayout_3.addWidget(self.edgeStartNodeIN)
        self.edgeEndNodeIN = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="End Node")
        self.edgeEndNodeIN.setObjectName("edgeEndNodeIN")
        self.horizontalLayout_3.addWidget(self.edgeEndNodeIN)
        self.edgeWeightIN = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Edge weight")
        self.edgeWeightIN.setObjectName("edgeWeightIN")
        self.horizontalLayout_3.addWidget(self.edgeWeightIN)
        self.insertEdgeButton = QtWidgets.QPushButton(self.verticalLayoutWidget,
                                                      clicked=lambda: self.insertEdgeClicked())
        self.insertEdgeButton.setObjectName("insertEdgeButton")
        self.horizontalLayout_3.addWidget(self.insertEdgeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.edgeStartNodeDelete = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Start Node name")
        self.edgeStartNodeDelete.setObjectName("edgeStartNodeDelete")
        self.horizontalLayout_4.addWidget(self.edgeStartNodeDelete)
        self.edgeEndNodeDelete = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="End Node name")
        self.edgeEndNodeDelete.setObjectName("edgeEndNodeDelete")
        self.horizontalLayout_4.addWidget(self.edgeEndNodeDelete)
        self.deleteEgeButton = QtWidgets.QPushButton(self.verticalLayoutWidget,
                                                     clicked=lambda: self.deleteEdgeClicked())
        self.deleteEgeButton.setObjectName("deleteEgeButton")
        self.horizontalLayout_4.addWidget(self.deleteEgeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startIN = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Start Node")
        self.startIN.setObjectName("startIN")
        self.horizontalLayout.addWidget(self.startIN)
        self.goalsIN = QtWidgets.QLineEdit(self.verticalLayoutWidget, placeholderText="Goal Nodes")
        self.goalsIN.setObjectName("goalsIN")
        self.horizontalLayout.addWidget(self.goalsIN)
        self.finishDataEntryButton = QtWidgets.QPushButton(self.verticalLayoutWidget,
                                                           clicked=lambda: self.finishDataEntryClicked())
        self.finishDataEntryButton.setObjectName("finishDataEntryButton")
        self.horizontalLayout.addWidget(self.finishDataEntryButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        GraphSearch.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GraphSearch)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1379, 26))
        self.menubar.setObjectName("menubar")
        GraphSearch.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GraphSearch)
        self.statusbar.setObjectName("statusbar")
        GraphSearch.setStatusBar(self.statusbar)

        self.visited_path_layout = QtWidgets.QWidget(self.centralwidget)
        self.visited_path_layout.setGeometry(QtCore.QRect(20, 800, 1520, 60))
        self.visited_path_layout.setObjectName("visited_path_layout")
        self.visited_path = QtWidgets.QVBoxLayout(self.visited_path_layout)
        self.visited_path.setContentsMargins(0, 0, 0, 0)
        self.visited_path.setObjectName("visited_path")
        self.visited_lab = QtWidgets.QLabel(self.visited_path_layout)
        self.visited_lab.setObjectName("visited")
        self.visited_path.addWidget(self.visited_lab)
        self.path_lab = QtWidgets.QLabel(self.visited_path_layout)
        self.path_lab.setObjectName("path")
        self.visited_path.addWidget(self.path_lab)


        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webEngineView.setGeometry(410, 28, 900, 750)

        #self.webEngineView2 = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        #self.webEngineView2.setGeometry(420, 38, 200, 200)
        self.webEngineView3 = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webEngineView3.setGeometry(1320, 28, 200, 200)

        self.retranslateUi(GraphSearch)
        QtCore.QMetaObject.connectSlotsByName(GraphSearch)

    def retranslateUi(self, GraphSearch):
        _translate = QtCore.QCoreApplication.translate
        GraphSearch.setWindowTitle(_translate("GraphSearch", "MainWindow"))
        self.groupBox_3.setTitle(_translate("GraphSearch", "Control"))
        self.groupBox.setTitle(_translate("GraphSearch", "Uninformed Search"))
        self.BFSButton.setText(_translate("GraphSearch", "Breadth First Search"))
        self.DFSButton.setText(_translate("GraphSearch", "Depth First Search"))
        self.IDSButton.setText(_translate("GraphSearch", "Iterative Deepening Search"))
        self.UCSButton.setText(_translate("GraphSearch", "Uniform Cost Search"))
        self.groupBox_2.setTitle(_translate("GraphSearch", "Informed Search"))
        self.GreedyButton.setText(_translate("GraphSearch", "Greedy Search"))
        self.astarButton.setText(_translate("GraphSearch", "A star Search"))
        self.searchAgainButton.setText(_translate("GraphSearch", "Search Again"))
        self.modifyDataButton.setText(_translate("GraphSearch", "Modify Data"))
        self.startLabel.setText(_translate("GraphSearch", "Start Node: "))
        self.goalsLabel.setText(_translate("GraphSearch", "Goal Nodes:"))
        self.insertNodeButton.setText(_translate("GraphSearch", "Insert Node"))
        self.deleteNodeButton.setText(_translate("GraphSearch", "Delete Node"))
        self.insertEdgeButton.setText(_translate("GraphSearch", "Insert Edge"))
        self.deleteEgeButton.setText(_translate("GraphSearch", "Delete Edge"))
        self.finishDataEntryButton.setText(_translate("GraphSearch", "Finish Data Entry"))

        self.visited_lab.setText(_translate("GraphSearch", "Visited Nodes: "))
        self.path_lab.setText(_translate("GraphSearch", "Solution Path:"))
        self.legend_creator()
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    GraphSearch = QtWidgets.QMainWindow()
    ui = Ui_GraphSearch()
    ui.setupUi(GraphSearch)
    GraphSearch.show()
    sys.exit(app.exec_())
