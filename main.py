from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys
from queue import PriorityQueue
# I decided to choose manhattan distance, because it feels more natural for "square" type of the graph/board 
# Add way to add "walls" to check if algorithm works fine
# Prog must tell if there is no way to come from start position to end position

# WIDTH = 0
# HEIGHT = 0

# I could use those in Window class, but I would need extra code for that. So it is fine to have it globally
startPoint = False # tells if we decided the start point/label
endPoint = False # tells if we decided the end point/label

class Window(QWidget):
    def __init__(self, HEIGHT, WIDTH):
        super().__init__()
        
        self.setWindowTitle("A* algorithm")
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)

        # self.startPoint = False # tells if we decided the start point/label
        # self.endPoint = False # tells if we decided the end point/label
        self.board = [] # board will all rows where each row is own list with each Node object on the board

        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_R: # Button "R" is for reset of the board
            self.resetBoard()
        elif e.key() == Qt.Key_S: # Button "S" is for start: program will find solution
            self.solveBoard()

    def resetBoard(self):
        global startPoint
        global endPoint
        startPoint = False
        endPoint = False
        for row in self.board:
            for node in row:
                if node.getColor() != "white":
                    node.changeColor("white")
                    node.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(255, 255, 255);")

    def createBoard(self, numberOfRows, numberOfCol, size):
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.setSpacing(0)
        self.setLayout(grid)

        for i in range(numberOfRows):
            rowList = []
            for j in range(numberOfCol):
                newLabel = clickableQLabel(self)
                newLabel.setStyleSheet("border : 1px solid grey; background : rgb(255, 255, 255);")
                newNode = Node(size)
                newNode.setLabel(newLabel)
                newLabel.addNodePointer(newNode)
                # newLabel.installEventFilter(self) # CHECK if works CONNECTS TO eventFilter function
                rowList.append(newNode)
                grid.addWidget(newLabel,i,j)
            self.board.append(rowList)
        return self.board


    def solveBoard(self):
        self.setNeighbours()

    def setNeighbours(self):
        # go through each node and finds his neihnours and add those nodes to the list of neigbours for each node
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                pass

    # def eventFilter(self, object, event):
    #     # if event.type() == QEvent.Enter:
    #     #     print("OK")
    #     #     print(object)
    #     #     return True
    #     if event.type() == QEvent.MouseButtonPress:
    #         print("OK")
    #         print(object)
    #         return True
    #     return False


class clickableQLabel(QLabel):
    nodePointer = None
    left_clicked = pyqtSignal()
    right_clicked = pyqtSignal()

    # def mouseMoveEvent(self, event):
    #     print(event.type())
    #     print(QEvent.LayoutRequest)
    #     x=event.globalX()
    #     y=event.globalY()
    #     print(x,y)

    def mousePressEvent(self, QMouseEvent):
        global startPoint
        global endPoint
        if QMouseEvent.button() == Qt.LeftButton:
            if startPoint == False: # if we don't have start
                self.nodePointer.changeColor("start") # or in other words blue
                self.nodePointer.getLabel().setStyleSheet("border : 1px solid grey; background : blue;")
                startPoint = True
            elif endPoint == False: # if we don't have end
                self.nodePointer.changeColor("end") # or in other words yellow
                self.nodePointer.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(223, 231, 61);")
                endPoint = True
            if self.nodePointer.getColor() == "white":
                self.nodePointer.changeColor("black")
                self.nodePointer.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(0, 0, 0);")

            #self.left_clicked.emit()
        elif QMouseEvent.button() == Qt.RightButton:
            # check if this is a start or end node
            if self.nodePointer.getColor() == "start":
                startPoint = False
            elif self.nodePointer.getColor() == "end":
                endPoint = False
            # reset lable to back to white
            self.nodePointer.changeColor("white")
            self.nodePointer.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(255, 255, 255);")
                
            self.right_clicked.emit()

    def addNodePointer(self, node):
        self.nodePointer = node


class Node():
    def __init__(self, size):
        # f(n) = g(n) + h(n)
        # Where g(n) is actual cost from the start node to this node
        # h(n) estimated cost to the target node/end node. In our case we use manhattan distance to find it.
        # The node with the lowest f(n) is the one that we will choose
        self.f = -1
        self.g = -1
        self.h = -1
        self.cameFrom = None # refers to the Node object where we came from (the lowest value came from)
        self.neighbors = []
        self.size = size
        self.labelPointer = None
        self.checked = False # tells if we already checked all neigbors of this Node
        self.color = "white"

    def setLabel(self, labelPointer):
        self.labelPointer = labelPointer

    def getLabel(self):
        return self.labelPointer

    def getColor(self):
        return self.color
    
    def changeColor(self, color):
        self.color = color
    

def updateBoard():
    pass

if __name__ == "__main__":
    WIDTH = 1000
    numberOfCol = 50
    numberOfRows = 30 
    sizeOfNode = int(WIDTH/numberOfCol) # so here each node will have width and height of 1000/50 = 20
    HEIGHT = int(sizeOfNode*numberOfRows)

    # Will have f(n) value of the Node as key and reference to the Node object as value
    nextNode = PriorityQueue()
    
    # nextNode.put((5, "Test"))
    # nextNode.put((1, "Test2"))
    # next_item = nextNode.get()

    app = QApplication(sys.argv)
    window = Window(HEIGHT, WIDTH)

    board = window.createBoard(numberOfRows, numberOfCol, sizeOfNode)

    sys.exit(app.exec_())
    

