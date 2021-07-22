# I decided to choose manhattan distance, because it feels more natural for "square" type of the graph/board 
# Add GUI
# Add way to add "walls" to check if algorithm works fine
# Prog must tell if there is no way to come from start position to end position


#(Start[0][1], End[3][7])
#  0123456789
  ############
0 # S        #
1 #          #
2 #          #
3 #       E  #
4 #          #
  ############

class Node():
    def __init__(self):
        # f(n) = g(n) + h(n)
        # Where g(n) is actual cost from the start node to this node
        # h(n) estimated cost to the target node/end node. In our case we use manhattan distance to find it.
        # The node with the lowest f(n) is the one that we will choose
        self.f = -1
        self.g = -1
        self.h = -1
        self.cameFrom = None # refers to the Node object where we came from

def createBoard(rowNum, colNum, nodeList):
    for _ in range(rowNum):
        rowList = []
        for _ in range(colNum):
            rowList.append(Node())
        nodeList.append(rowList)

def main():
    nodeList = []
    createBoard(5,10, nodeList)
