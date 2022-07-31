import numpy as np,pygame

CONNECT4_STYLE = 0
TICTACTOE_STYLE = 1
class GameBoard():

    def __init__(self,dimensions,style):

        self.grid = []
        for y in range(dimensions[0]):
            self.grid.append([])
            for x in range(dimensions[1]):
                self.grid[-1].append(0)
        self.style = style
    def draw(self,surface,position,size):

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


                

