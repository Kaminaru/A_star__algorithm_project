from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QGridLayout
import sys

from queue import PriorityQueue
import threading
import time

board = [] # global reference to the board (2D list with Node objects)
startPoint = False # tells if we decided the start point/label
endPoint = False # tells if we decided the end point/label

leftClick = False # detects if leftClick is pressed down
rightClick = False # detects if rightClick is pressed down
stopThread = False # to be able to kill thread easy way

trueNodeSize = 0 # size of the node block on the window

class Window(QWidget):
    def __init__(self, HEIGHT, WIDTH):
        super().__init__()
        
        self.setWindowTitle("A* algorithm")
        self.setFixedWidth(WIDTH)
        self.setFixedHeight(HEIGHT)

        self.solvingThread = threading.Thread(target=self.solveBoard, args = ())

        self.show()

    def keyPressEvent(self, e): # called after button on keyboard is pressed
        global stopThread
        if e.key() == Qt.Key_R: # Button "R" is for reset of the board
            stopThread = True # solveBoard() function will stop after that, that will lead to thread beeing killed
            self.resetBoard()
        elif e.key() == Qt.Key_S: # Button "S" is for start: program will find solution
            if not self.solvingThread.is_alive(): # do not let do anything while thread is running
                if startPoint == True and endPoint == True:
                    stopThread = False
                    self.solvingThread = threading.Thread(target=self.solveBoard, args = ())
                    self.solvingThread.start()

    def resetBoard(self):
        # sets every Node to "white stage"
        global startPoint, endPoint
        startPoint = False
        endPoint = False
        for row in board:
            for node in row:
                node.changeColor("white")
                node.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(255, 255, 255);")

    def createBoard(self, numberOfRows, numberOfCol):
        # creates board with QGrid and many clickable QLabels
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.setSpacing(0)
        self.setLayout(grid)
        
        tmpBoard = []
        for i in range(numberOfRows):
            rowList = []
            for j in range(numberOfCol):
                newLabel = clickableQLabel(self)
                newLabel.setStyleSheet("border : 1px solid grey; background : rgb(255, 255, 255);")
                newNode = Node(i, j)
                newNode.setLabel(newLabel)
                newLabel.addNodePointer(newNode)

                rowList.append(newNode)
                grid.addWidget(newLabel,i,j)
            tmpBoard.append(rowList)
        global board
        board = tmpBoard

    def findmanhattanDistance(self, startNode, endNode):
        # Finds and returns Manhattan distance from the start to the end Node object in the 2D board list
        x1 = startNode.getX()
        y1 = startNode.getY()
        x2 = endNode.getX()
        y2 = endNode.getY()
        return abs(x1-x2) + abs(y1-y2)

    def setNeighbours(self):
        # go through each node and finds his neighbours and add those nodes to the list of neigbours for each node
        for i in range(len(board)):
            for j in range(len(board[0])):
                neighbours = []
                if i-1 >= 0 and board[i-1][j].getColor() != "black": # up
                    neighbours.append(board[i-1][j])
                if i+1 < len(board)-1 and board[i+1][j].getColor() != "black": # down
                    neighbours.append(board[i+1][j])
                if j-1 >= 0 and board[i][j-1].getColor() != "black": # left
                    neighbours.append(board[i][j-1])
                if j+1 < len(board[0])-1 and board[i][j+1].getColor() != "black": # right
                    neighbours.append(board[i][j+1])
                board[i][j].changeNeighborList(neighbours)
        
    def reconstruct_path(self, cameFrom, currentNode, startNode):
        # paints the shortest path from start to the end point
        while currentNode in cameFrom:
            currentNode = cameFrom[currentNode]
            if currentNode != startNode:
                currentNode.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(123, 234, 107);")
                currentNode.changeColor("path")
                time.sleep(0.01) # 10 ms

    def solveBoard(self):
        self.setNeighbours() # only sets neighbours after solve S button on keyboard is pressed
        # position in board 2D list
        startNode, endNode = self.findStartAndEnd()  # finds start and end node

        nextNodeQueue = PriorityQueue() # Will have f(n) value of the Node as key and reference to the Node object as value
        # we start from the start node
        count = 0 # so priorityQueue will hold the order of the new added elements with the same f(n) value
        nextNodeQueue.put((0, count, startNode))

        # f(n) = g(n) + h(n)
        # Where g(n) is actual cost from the start node to this node
        # h(n) estimated cost to the target node/end node. In our case we use manhattan distance to find it.
        # The node with the lowest f(n) is the one that we will choose
        cameFrom = {} # refers to the Node object where we came from (the lowest value came from)
        gScore = {node : float('inf') for row in board for node in row}
        gScore[startNode] = 0
        fScore = {node : float('inf') for row in board for node in row}
        fScore[startNode] = self.findmanhattanDistance(startNode, endNode) # no need g, because there is no g(n) for start node 

        while not nextNodeQueue.empty():
            if not stopThread: # in case we want to stop thread by pressing "R" key while it's running
                currentNode = nextNodeQueue.get()[2]
                if currentNode.getColor() == "end":
                    self.reconstruct_path(cameFrom, currentNode, startNode)
                    print("Found solution!")
                    return True
                
                for neighbor in currentNode.getNeighborList():
                    tmpGScore = gScore[currentNode] + 1 # 1 is the weight of the edge from current to neighbor. In our case 1.
                    if tmpGScore < gScore[neighbor]:
                        # This path to neighbor is better than any previous one. Save it.
                        cameFrom[neighbor] = currentNode # so shortes path is from "currentNode"
                        gScore[neighbor] = tmpGScore
                        fScore[neighbor] = tmpGScore + self.findmanhattanDistance(neighbor, endNode)
                        if (fScore[neighbor], count, neighbor) not in nextNodeQueue.queue:
                            count += 1
                            nextNodeQueue.put((fScore[neighbor], count, neighbor))
                            if neighbor != endNode:
                                neighbor.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(245, 130, 130);")
                                neighbor.changeColor("lightRed")
                                time.sleep(0.01) # 10 ms

                if currentNode != startNode:
                    currentNode.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(196, 221, 249);")
                    currentNode.changeColor("lightBlue")
                    time.sleep(0.01) # 10 ms
            else:
                print("Thread is stopped")
                return False
        print("Wasn't able to find a solution")
        return False

    def findStartAndEnd(self):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j].getColor() == "start":
                    startNode = board[i][j]
                elif board[i][j].getColor() == "end":
                    endNode = board[i][j]
        return startNode, endNode

class clickableQLabel(QLabel):
    # own class that imports QLabel however it will also have QMouseEvents with left and right clicks
    nodePointer = None
    def mouseReleaseEvent(self, QMouseEvent):
        # If mouse realesed, we won't change any colors for any label we hover over
        global leftClick, rightClick
        if leftClick == True:
            leftClick = False
        if rightClick == True:
            rightClick = False

    def mousePressEvent(self, QMouseEvent):
        # Mouse right click changing one label back to white
        # Mouse left click changing one label to start position, end positon or black (if start and end is chosen)
        global startPoint, endPoint, leftClick, rightClick
        if QMouseEvent.button() == Qt.LeftButton:
            leftClick = True # tells that left button is pressed (will be used in mouseMoveEvent() function)
            if self.nodePointer.getColor() == "white":
                if startPoint == False: # if we don't have start point
                    self.nodePointer.changeColor("start") # or in other words blue
                    self.setStyleSheet("background : blue;")
                    startPoint = True
                elif endPoint == False: # if we don't have end, but we have start point
                    self.nodePointer.changeColor("end") # or in other words green
                    self.setStyleSheet("background : green;")
                    endPoint = True
                else: # if we have start and end point
                    self.nodePointer.changeColor("black")
                    self.setStyleSheet("border : 1px solid grey; background : rgb(0, 0, 0);")
        elif QMouseEvent.button() == Qt.RightButton:
            rightClick = True # tells that right button is pressed (will be used in mouseMoveEvent() function)
            # check if this is a start or end node. We need to reset information about startPoint or endPoint
            if self.nodePointer.getColor() == "start":
                startPoint = False
            elif self.nodePointer.getColor() == "end":
                endPoint = False
            # reset lable to back to white
            self.nodePointer.changeColor("white")
            self.setStyleSheet("border : 1px solid grey; background : rgb(255, 255, 255);")
                
    def mouseMoveEvent(self, event):
        # If right or left mouse button is pressed, and start and end point is chosen, we will change color to black 
        # to whatever other lable we hover over with the mouse pointer
        global startPoint, endPoint
        x = event.windowPos().x() # x position of the mouse pointer on the window
        y = event.windowPos().y() # y position of the mouse pointer on the window
        # changing x,y cordinates to [i][j] position in the 2D board list by using node side size
        i = int(y/trueNodeSize)
        j = int(x/trueNodeSize)
        if i < len(board) and i >= 0 and j < len(board[0]) and j >= 0: # checks if i and j is not out of boundaries
            curNode = board[i][j]
            if leftClick and curNode.getColor() != "start" and curNode.getColor() != "end":
                if startPoint and endPoint:
                    curNode.changeColor("black")
                    curNode.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(0, 0, 0);")
            elif rightClick:
                if curNode.getColor() == "start":
                    startPoint = False
                elif curNode.getColor() == "end":
                    endPoint = False
                curNode.changeColor("white")
                curNode.getLabel().setStyleSheet("border : 1px solid grey; background : rgb(255, 255, 255);")

    def addNodePointer(self, node):
        self.nodePointer = node


class Node():
    def __init__(self, x, y):
        self.neighbors = [] # list of the neighbors to this node
        self.labelPointer = None
        self.color = "white"
        self.x = x # x position in the board list
        self.y = y # y position in the board list

    def changeNeighborList(self, newList):
        self.neighbors = newList
    
    def getNeighborList(self):
        return self.neighbors

    def setLabel(self, labelPointer):
        self.labelPointer = labelPointer

    def getLabel(self):
        return self.labelPointer

    def getColor(self):
        return self.color
    
    def changeColor(self, color):
        self.color = color

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def __lt__(self, other): # needed for priorityQueue
        return False


if __name__ == "__main__":
    WIDTH = 900
    numberOfCol = 35
    numberOfRows = 35
    trueNodeSize = WIDTH/numberOfCol
    sizeOfNode = int(WIDTH/numberOfCol)
    HEIGHT = int(sizeOfNode*numberOfRows)

    app = QApplication(sys.argv)
    window = Window(HEIGHT, WIDTH)

    window.createBoard(numberOfRows, numberOfCol)
    sys.exit(app.exec_())