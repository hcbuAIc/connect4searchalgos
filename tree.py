from tracemalloc import start
import pygame,numpy as np
class node():

    def __init__(self,value,cost,parent):

        self.value = value
        self.cost = cost
        self.parent = parent
        self.children = []
        self.numTotalOffspring = 0
        if (self.parent == None):
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

    def addChild(self,value,cost):

        self.children.append(node(value,cost,self))
        self.addOffspring()

    def addOffspring(self):
        self.numTotalOffspring += 1
        if (self.parent != None):
            self.parent.addOffspring()

def drawTree(surface,root,position,nodeRadius,edgeLength,offset):

    tree = []
    fifo = [[root,position]]

    pygame.draw.circle(surface,(0,0,0),position + np.array((0,0)),nodeRadius,1)

    while len(fifo) > 0:
        current = fifo[0][0]
        count = 0

        for child in current.children:
            offset = 0
            if (len(current.children) > 1):
                offset = ((count/(len(current.children)-1)) - 0.5) * nodeRadius * 3
                offset += np.sign(((count/(len(current.children)-1)) - 0.5)) * (current.numTotalOffspring+child.numTotalOffspring) * 2 * nodeRadius * abs((count/(len(current.children)-1)) - 0.5)
                #offset += np.sign(fifo[0][1][0]-position[0]) * child.numTotalOffspring/2 * nodeRadius * 3

            pos = fifo[0][1] + np.array((offset,edgeLength))
            direction = (fifo[0][1]-pos)/np.linalg.norm(pos-fifo[0][1])
            pygame.draw.line(surface,(0,0,0),pos+direction*nodeRadius,fifo[0][1]-direction*nodeRadius,1)
            pygame.draw.circle(surface,(0,0,0),pos,nodeRadius,1)
            fifo.append([child,pos])
            count += 1
        fifo.pop(0)
    

