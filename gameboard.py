from math import ceil
from matplotlib.pyplot import grid
import numpy as np,pygame

CONNECT4_STYLE = 0
TICTACTOE_STYLE = 1
class GameBoard():

    def __init__(self,dimensions,style):

        self.grid = []
        self.lastDrawPos = None
        self.lastDrawSurface = None
        self.lastDrawSize = None
        for y in range(dimensions[0]):
            self.grid.append([])
            for x in range(dimensions[1]):
                self.grid[-1].append(0)
        self.style = style
    def draw(self,surface,position,size):

        self.lastDrawPos = position
        self.lastDrawSurface = surface
        self.lastDrawSize = np.array((size,size * (len(self.grid[0])/len(self.grid[1]))) )

        size = np.array((size,size * (len(self.grid[0])/len(self.grid[1]))) )
        
        corner = position - size/2

        if (self.style == CONNECT4_STYLE):
            
            TEAMCOLORS = ((255,255,255),(255,0,0),(255,255,0))
            #TEAMCOLORS references the three colors a "node" can have in connect 4
            #0 being empty or white
            #1 being team1 represented red
            #2 being team2 represented by yellow
            pygame.draw.rect(surface,(0,17,50),(corner[0],corner[1],size[0],size[1]))
            #drawing each cell is a pain because cell dimensions are relative to the boardsize
            #0.5 is added to x and y because pygame draws circles centered on the coordinates while x and y here map to the corners of each cell
            #so effectively x = 0 y = 0 is the corner of cell(0,0) and x = 0.5 y = 0.5 is the center of cell(0,0)
            for x in range(len(self.grid)):
                for y in range(len(self.grid[0])):
                    pygame.draw.circle(surface,TEAMCOLORS[self.grid[x][y]],
                    corner + size*np.array(((x+0.5)/len(self.grid),(y+0.5)/len(self.grid[1]))),
                    int((size[0]/len(self.grid)) * 0.4) )

        if (self.style == TICTACTOE_STYLE):
            
            
            pygame.draw.rect(surface,(255,255,255),(corner[0],corner[1],size[0],size[1]))
            
            for x in range(len(self.grid)):
                for y in range(len(self.grid[0])):
                    #drawing the gridCell's bounds
                    pos = corner + size*np.array(((x)/len(self.grid),(y)/len(self.grid[1])))
                    bounds = size*np.array(((1)/len(self.grid),(1)/len(self.grid[1])))
                    pygame.draw.rect(surface,(0,0,0),(pos[0],pos[1],bounds[0],bounds[1]),int(size[0]/len(self.grid[0])*0.05))

                    #team 1 is Xs
                    if (self.grid[x][y] == 1):
                        
                        #the X consists of two lines and it is easy to draw them from the corners of a square
                        #this square is of size xBounds, centered in the cell
                        xBounds = np.array(size[0]/len(self.grid[0]),size[1]/len(self.grid[1])) * 0.4
                        xCenter = corner + (size*np.array(((x+0.5)/len(self.grid),(y+0.5)/len(self.grid[1]))))

                        pygame.draw.line(surface,(255,0,0),xCenter+(xBounds*np.array((-1,-1))),xCenter+(xBounds*np.array((1,1))),int(size[0]/len(self.grid[0])*0.1))
                        pygame.draw.line(surface,(255,0,0),xCenter+(xBounds*np.array((-1,1))),xCenter+(xBounds*np.array((1,-1))),int(size[0]/len(self.grid[0])*0.1))

                    #team 2 is Os
                    if (self.grid[x][y] == 2):
                        pygame.draw.circle(surface,(0,0,255),
                        corner + size*np.array(((x+0.5)/len(self.grid),(y+0.5)/len(self.grid[1]))),
                        int((size[0]/len(self.grid)) * 0.4),int(size[0]/len(self.grid[0])*0.1))
    def gamePlayerInput(self,mousePos,mouseClick):
        
        if (self.lastDrawSurface != None):
            
            if (self.style == CONNECT4_STYLE):

                pieceRadius = int((self.lastDrawSize[0]/len(self.grid[0])) * 0.4)
                targetColumn = -1

                size = np.array((self.lastDrawSize,self.lastDrawSize * (len(self.grid[0])/len(self.grid[1]))) )
                corner = self.lastDrawPos - self.lastDrawSize/2
                #check if and which column is the player's cursor is selecting
                #this is determined by checkin if the player's cursor is within a circle above the board
                for x in range(0,len(self.grid)):
                    cellPos = corner + size[0]*np.array(((x+0.5)/len(self.grid),(-1+0.5)/len(self.grid[1])))
                    if (np.linalg.norm(mousePos-cellPos) < pieceRadius and self.moveLegal(x=x)):
                        pygame.draw.circle(self.lastDrawSurface,(255,0,0),cellPos,pieceRadius)
                        targetColumn = x
                        break

                if (targetColumn == -1):
                    pass
                    #pygame.draw.circle(self.lastDrawSurface,(0,0,0),mousePos,pieceRadius,ceil(pieceRadius*0.05))
                else:
                    if (mouseClick[0]==1 and self.moveLegal(x=targetColumn)):
                        self.gameInput(1,x=targetColumn)
                        return True
            if (self.style == TICTACTOE_STYLE):

                
                targetCell = (-1,-1)

                size = np.array((self.lastDrawSize[0],self.lastDrawSize[1] * (len(self.grid[0])/len(self.grid[1]))) )
                corner = self.lastDrawPos - self.lastDrawSize/2
                #check if and which column is the player's cursor is selecting
                #this is determined by checkin if the player's cursor is inside a gridCell
                for x in range(0,len(self.grid)):
                    for y in range(0,len(self.grid[x])):
                        cellPos = corner + size[0]*np.array(((x)/len(self.grid),(y)/len(self.grid[1])))
                        #basic AABB check
                        localCursorPos = (mousePos-cellPos)
                        if (
                            localCursorPos[0] > 0 and 
                            localCursorPos[1] > 0 and 
                            localCursorPos[0] < size[0]/len(self.grid) and 
                            localCursorPos[1] < size[1]/len(self.grid[0]) and 
                            self.moveLegal(x=x,y=y)):
                            pygame.draw.circle(self.lastDrawSurface,(124,124,255),
                            corner + size*np.array(((x+0.5)/len(self.grid),(y+0.5)/len(self.grid[1]))),
                            int((size[0]/len(self.grid)) * 0.4),int(size[0]/len(self.grid[0])*0.1))
                            targetCell = (x,y)
                            break

                if (targetCell == (-1,-1)):
                    pass
                    #pygame.draw.circle(self.lastDrawSurface,(0,0,0),mousePos,
                    #int((size[0]/len(self.grid)) * 0.4),
                    #ceil(size[0]/len(self.grid)* 0.1))
                else:
                    if (mouseClick[0]==1 and self.moveLegal(x=targetCell[0],y=targetCell[1])):
                        self.gameInput(2,x=targetCell[0],y=targetCell[1])
                        return True

        #return weather the gamestate has advanced
        return False
    def moveLegal(self,**kwargs):
        if (self.style == CONNECT4_STYLE):
            x = None
            for arg,value in kwargs.items():
                if (arg == "x"):
                    x = value
            if (x == None or self.grid[x][0] != 0):
                return False

            return True
            
        if (self.style == TICTACTOE_STYLE):
            x = None
            y = None
            for arg,value in kwargs.items():

                if (arg == "x"):
                    x = value
                if (arg == "y"):
                    y = value

            if (x == None or y == None or self.grid[x][y] != 0):
                return False
            
            return True
            
        return False
    def gameInput(self,team,**kwargs):
        
        if (self.style == CONNECT4_STYLE):
            x = None
            for arg,value in kwargs.items():
                if (arg == "x"):
                    x = value
            if (x == None or self.grid[x][0] != 0):
                return 
            
            for y in range(len(self.grid[x])):
                if (len(self.grid[x]) == y+1):
                    self.grid[x][y] = team
                    return
                if (self.grid[x][y+1] != 0):
                    self.grid[x][y] = team
                    return
        if (self.style == TICTACTOE_STYLE):
            x = None
            y = None
            for arg,value in kwargs.items():

                if (arg == "x"):
                    x = value
                if (arg == "y"):
                    y = value

            if (x == None or y == None):
                return
            self.grid[x][y] = team
            return


                

