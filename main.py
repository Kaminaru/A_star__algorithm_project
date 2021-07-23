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

class Window(QMainWindow):
    def __init__(self, HEIGHT, WIDTH):
        super(Window, self).__init__()
        
        self.setWindowTitle("A* algorithm")
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)
        
        # self.labelTest = QLabel("Press it", self)
        # self.labelTest.move(0, 0)
        # self.labelTest.resize(120, 80)

        # self.buttonTest = QPushButton(self)
        # self.buttonTest.setText("PRESS ME!")
        # self.buttonTest.clicked.connect(self.clickAction)


        self.show()

    # def clickAction(self):
    #     self.buttonTest.setText("ouch!")

    def createBoard(self, numberOfRows, numberOfCol, size):
        board = []
        for i in range(numberOfRows):
            rowList = []
            for j in range(numberOfCol):
                newLabel = QLabel("", self)
                newLabel.setStyleSheet("border : 1px solid grey; background : white;")
                newLabel.setGeometry(j*size, i*size, size, size) # setGeometry(left, top, width, height)
                newLabel.show()
                rowList.append(Node(size, newLabel))
            board.append(rowList)
        return board

class Node():
    def __init__(self, size, labelPointer):
        # f(n) = g(n) + h(n)
        # Where g(n) is actual cost from the start node to this node
        # h(n) estimated cost to the target node/end node. In our case we use manhattan distance to find it.
        # The node with the lowest f(n) is the one that we will choose
        self.f = -1
        self.g = -1
        self.h = -1
        self.cameFrom = None # refers to the Node object where we came from (the lowest value came from)
        self.neighbors = []
        self.width = 0
        self.size = size
        self.labelPointer = labelPointer
        self.checked = False # tells if we already checked all neigbors of this Node


def updateBoard():
    pass


if __name__ == "__main__":
    WIDTH = 1000
    numberOfCol = 50
    numberOfRows = 30 
    sizeOfNode = WIDTH/numberOfCol # so here each node will have width and height of 1000/50 = 20
    HEIGHT = sizeOfNode*numberOfRows

    # Will have f(n) value of the Node as key and reference to the Node object as value
    # nextNode = PriorityQueue()
    
    # nextNode.put((5, "Test"))
    # nextNode.put((1, "Test2"))
    # next_item = nextNode.get()

    app = QApplication(sys.argv)
    window = Window(HEIGHT, WIDTH)


    board = window.createBoard(numberOfRows, numberOfCol, sizeOfNode)
    # drawBoard(board)



    sys.exit(app.exec_())
    

