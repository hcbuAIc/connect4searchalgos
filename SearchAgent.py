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
        
        searchDepth = 2
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

                        #child's value is a grid and the column the last move was made at
                        #sign(turn-0.5) makes the costs positive or negative based on whose turn it is
                        cost = self.evaluateConnect4(cell,current.value[0],turn+1) * sign(turn-0.5)
                        current.addChild((grid,i),cost)

                    
                for child in current.children:
                    fifo.append(child)

            fifo.pop(0)
       
        

    def evaluateConnect4(self,cell,grid,team):

        value = 0

        


        #checking for verical lines

        lineLength = 1
        for y in range(cell[1],len(grid[cell[0]])):
            if (y+1 >= len(grid[0])):
                break
            if (grid[cell[0]][y] != team):
                break
            else:
                lineLength += 1

        value += lineLength

        lineLength = 1
        for x in range(cell[0]+1,len(grid)):
            if (x+1 >= len(grid)):
                break
            if (grid[x][cell[1]] != team):
                break
            else:
                lineLength += 1
        
        for x in range(cell[0]-1,0,1):
            if (x-1 < 0):
                break
            if (grid[x][cell[1]] != team):
                break
            else:
                lineLength += 1

        value += lineLength

        return value
                
    

    