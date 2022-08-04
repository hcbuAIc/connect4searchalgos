import pygame,random,numpy as np,gameboard,tree,SearchAgent

#change this if you want to increase the screen's resolution
SIZE = np.array((1200,980))
screen = pygame.display.set_mode(SIZE)

connect4 = gameboard.GameBoard(np.array((7,6)),gameboard.CONNECT4_STYLE)

for i in range(0):
    connect4.gameInput(1,x=random.randint(0,6))
    connect4.gameInput(2,x=random.randint(0,6))



tictactoe = gameboard.GameBoard(np.array((3,3)),gameboard.TICTACTOE_STYLE)
tictactoe.gameInput(2,x=0,y=0)
tictactoe.gameInput(1,x=1,y=0)

root = tree.node(0,1,None)
maxDepth = 4
minChildren = 1
maxChildren = 4
fifo = [root]
while (len(fifo) > 0):
    current = fifo[0]

    if (current.depth < maxDepth):
        for i in range(0,random.randint(minChildren,maxChildren)):
            current.addChild(0,1)
            fifo.append(current.children[-1])
    fifo.pop(0)


run = True

isPlayerTurn = True
isPlayerTurn2 = True

unclick = 0


jerryDaniels = SearchAgent.searchAgent(connect4)
jerryDaniels.constructMinimaxMoveTree()

while run:

    screen.fill((255,255,255))
    mousePos = np.array(pygame.mouse.get_pos())
    connect4.draw(screen,np.array((SIZE[0]/4,SIZE[1]/2)),SIZE[0]*1/3)
    tictactoe.draw(screen,np.array((SIZE[0]/4 * 3,SIZE[1]/2)),SIZE[0]*1/3)
    
    if (isPlayerTurn and unclick):
        madeMove=connect4.gamePlayerInput(mousePos,pygame.mouse.get_pressed())
        if (madeMove):
            jerryDaniels.constructMinimaxMoveTree()
            jerryDaniels.makeMove()
        #isPlayerTurn = isPlayerTurn and not madeMove
    if (isPlayerTurn2 and unclick):
        madeMove=tictactoe.gamePlayerInput(mousePos,pygame.mouse.get_pressed())
        
        #isPlayerTurn2 = isPlayerTurn2 and not madeMove

    unclick = pygame.mouse.get_pressed()[0] == 0
    tree.drawTree(screen,jerryDaniels.possibilities,SIZE/2 - np.array((0,(5/6*SIZE[1])/2)),1.5,32,0)

    #render drawn shapes
    pygame.display.update()
    #render blitted images
    pygame.display.flip()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            run = False
    
pygame.quit()
