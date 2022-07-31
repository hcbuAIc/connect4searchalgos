import pygame,random,numpy as np,gameboard

#change this if you want to increase the screen's resolution
SIZE = np.array((800,880))
screen = pygame.display.set_mode(SIZE)

connect4 = gameboard.GameBoard(np.array((7,6)),0)
connect4.gameInput(1,x=0)
connect4.gameInput(2,x=0)
connect4.gameInput(1,x=1)
connect4.gameInput(2,x=1)

run = True
while run:

    screen.fill((255,255,255))

    connect4.draw(screen,SIZE/2,SIZE[0]*0.5)
    #render drawn shapes
    pygame.display.update()
    #render blitted images
    pygame.display.flip()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False

pygame.quit()
