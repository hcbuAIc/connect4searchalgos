import numpy as np,pygame
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

        if (self.style == 0):
            
            TEAMCOLORS = ((255,255,255),(255,0,0),(255,255,0))

            pygame.draw.rect(surface,(0,17,50),(corner[0],corner[1],size[0],size[1]))
            for x in range(len(self.grid)):
                for y in range(len(self.grid[0])):
                    pygame.draw.circle(surface,TEAMCOLORS[self.grid[x][y]],
                    corner + size*np.array(((x+0.5)/len(self.grid),(y+0.5)/len(self.grid[1]))),
                    int((size[0]/len(self.grid)) * 0.8*0.5) )
    def gameInput(self,team,**kwargs):
        
        if (self.style == 0):
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

        


                

