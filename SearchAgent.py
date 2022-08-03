from re import S

from numpy import sign
import gameboard,tree

#necesary because python decides that any list being copied will always be a pointer
def copyGrid(A):

    out = []
    for x in range(len(A)):
        out.append([])
        for y in range(len(A[0])):
            out[-1].append(A[x][y])
    return out



class searchAgent():

    def __init__(self,gameboard):

        self.environment = gameboard
        self.game = gameboard.style
        #tree representing possible actions
        self.possibilities = None
        self.team = 2


    def constructMinimaxMoveTree(self):
        
        searchDepth = 3
        self.possibilities = tree.node((copyGrid(self.environment.grid),(-1,-1)),1,None)
        fifo = [self.possibilities]
       
        #tree construction
        while (len(fifo) > 0):
            current = fifo[0]
            #print(current.cost)
            if (current.depth < searchDepth):
                
                #0 means the agent choses
                #1 means the player choses
                turn = current.depth % 2
                
                for i in range(0,len(self.environment.grid)):
                    grid = copyGrid(current.value[0])
                    if (self.environment.moveLegal(x=i,grid=grid)):
                        
                        cell = [i,0]

                        for i in range(len(grid[0])):
                            cell[1] = i
                            if (grid[0][i] != 0):
                                cell[1]-=1
                                break

                        cost = self.evaluateConnect4(current.value[0]) * sign(turn-0.5)
                        current.addChild((grid,i),cost)

                    
                for child in current.children:
                    fifo.append(child)

            fifo.pop(0)
       
    def evaluateCell(self,cell,grid,team):
        
        score = 0
        
        gridSizeX = len(grid)
        gridSizeY = len(grid[0])
        slopes = ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1))

        for slope in slopes:
            lineLength = 1
            pieceLine = 1
            x = cell[0]
            y = cell[1]
            for i in range(0,4):
                x += slope[0]
                y += slope[1]
                if (x<gridSizeX and y < gridSizeY and x >= 0 and y >= 0):
                    if (grid[x][y] != 0 and grid[x][y] != team):
                        break
                    if (grid[x][y] == team):
                        pieceLine += 1
                    lineLength += 1
                else:
                    break
            if (lineLength >= 4):
                score+=1
            if (pieceLine >= 4):
                return 65536
                

        return score

        

    def evaluateConnect4(self,grid):

        value = 0

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                team = grid[x][y]
                if (team == 1):
                    #player's piece
                    value -= self.evaluateCell((x,y),grid,team)
                if (team == 2):
                    #agent's piece
                    value += self.evaluateCell((x,y),grid,team)

        return value
                
    

    