from re import S
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

    def constructMoveTree(self):
        
        searchDepth = 5
        self.possibilities = tree.node((copyGrid(self.environment.grid),(-1,-1)),1,None)
        fifo = [self.possibilities]
        while (len(fifo) > 0):
            current = fifo[0]
            #print(current.cost)
            if (current.depth < searchDepth):
                for i in range(0,len(self.environment.grid)):
                    grid = copyGrid(current.value[0])
                    if (self.environment.moveLegal(x=i,grid=grid)):
                        
                        
                        cell = [i,0]

                        for y in range(0,len(grid[0])):
                            if (y+1 == len(grid[0])):
                                cell[1] = y
                                break
                            if (grid[cell[0]][y+1] != 0):
                                cell[1] = y
                                break
                            

                        grid[cell[0]][cell[1]] = self.team

                        current.addChild((grid,cell),self.evaluateConnect4(cell,current.value[0],self.team))
                        fifo.append(current.children[-1])
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

        value += 3**lineLength

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

        value += 3**lineLength

        return value
                
    

    