from tracemalloc import start
import pygame,numpy as np

def clamp(a,b,c):
    if (a < b):
        return b
    if (a > c):
        return c
    return a
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
    maxNodes = 1000
    numNodes = 0
    pygame.draw.circle(surface,(0,0,0),position + np.array((0,0)),nodeRadius,1)

    while len(fifo) > 0 and numNodes < maxNodes:
        current = fifo[0][0]
        count = 0
        numNodes+=1


        for child in current.children:
            offset = 0
            
            if (len(current.children) > 1):
                offset = ((count/(len(current.children)-1)) - 0.5) * nodeRadius * 3
                offset += np.sign(((count/(len(current.children)-1)) - 0.5)) * (current.numTotalOffspring+child.numTotalOffspring) * 2 * nodeRadius * abs((count/(len(current.children)-1)) - 0.5)
                #offset += np.sign(fifo[0][1][0]-position[0]) * child.numTotalOffspring/2 * nodeRadius * 3

            pos = fifo[0][1] + np.array((offset,edgeLength))
            direction = (fifo[0][1]-pos)/np.linalg.norm(pos-fifo[0][1])
            pygame.draw.line(surface,(0,0,0),pos+direction*nodeRadius,fifo[0][1]-direction*nodeRadius,1)
            if (child.cost == None):
                pygame.draw.circle(surface,(0,0,0),pos,nodeRadius+2,1)
            else:
                
                color = np.array((255,255,0))*clamp(child.cost/25,0,1) + np.array((255,0,0))*clamp(-child.cost/25,0,1)
                #color = np.array((255,255,0))*clamp(child.depth%2,0,1) + np.array((255,0,0))*clamp((child.depth+1)%2,0,1)
                pygame.draw.circle(surface,(0,0,0),pos,nodeRadius+2,1)
                pygame.draw.circle(surface,color,pos,nodeRadius+1)
                

            fifo.append([child,pos])
            count += 1
        fifo.pop(0)
    

