"""
-----------------------------
Sweeper.py
Name: Phillip Kalmanson
Minesweeper game using pygame library
-----------------------------
"""
import pygame
import random
pygame.init()


#Game Variables
gridHeight = 10
gridWidth = 10
numMines = 10
squareSize = 32
header = 128
border = 16
gameWidth = squareSize * gridWidth + (border * 2)
gameHeight = squareSize * gridHeight + border + header

#Setup
gameDisplay = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Sweeper")
timer = pygame.time.Clock()
grid = []
mines = []

#Colors
DARK_GRAY = (105, 105, 105)
LIGHT_GRAY = (211, 211, 211)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)

#Import Images:
image_empty = pygame.image.load("images/empty.png")
image_flag = pygame.image.load("images/flag.png")
image_mine = pygame.image.load("images/mine.png")
image_mineOpened = pygame.image.load("images/mineOpened.png")
image_mineWrong = pygame.image.load("images/mineWrong.png")
image_square = pygame.image.load("images/square.png")
image_square1 = pygame.image.load("images/square1.png")
image_square2 = pygame.image.load("images/square2.png")
image_square3 = pygame.image.load("images/square3.png")
image_square4 = pygame.image.load("images/square4.png")
image_square5 = pygame.image.load("images/square5.png")
image_square6 = pygame.image.load("images/square6.png")
image_square7 = pygame.image.load("images/square7.png")
image_square8 = pygame.image.load("images/square8.png")


def drawText(txt, s, offset=0, color=BLACK):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, color)
    rect = screen_text.get_rect()
    rect.center = (gridWidth * squareSize / 2 + border, gridHeight * squareSize / 2 + header + offset)
    gameDisplay.blit(screen_text, rect)

class Square:
    def __init__(self, x, y, value):
        self.x = x # x position on grid
        self.y = y # y position on grid
        self.opened = False # if square has been opened
        self.mineOpened = False # if square has been opened and is a mine
        self.flagged = False # if square is flagged
        self.mineWrong = False # if square is flagged but not a mine
        self.rect = pygame.Rect(border + self.x * squareSize, header + self.y * squareSize, squareSize, squareSize)
        self.value = value
        
    #Draw tiles
    def draw(self):
        #If opened
        if self.opened:
            #If mine
            if self.value == -1:
                if self.mineOpened:
                    gameDisplay.blit(image_mineOpened, self.rect)
                else:
                    gameDisplay.blit(image_mine, self.rect)
            #If regular tile
            elif self.value == 0:
                gameDisplay.blit(image_empty, self.rect)
            elif self.value == 1:
                gameDisplay.blit(image_square1, self.rect)
            elif self.value == 2:
                gameDisplay.blit(image_square2, self.rect)
            elif self.value == 3:
                gameDisplay.blit(image_square3, self.rect)
            elif self.value == 4:
                gameDisplay.blit(image_square4, self.rect)
            elif self.value == 5:
                gameDisplay.blit(image_square5, self.rect)
            elif self.value == 6:
                gameDisplay.blit(image_square6, self.rect)
            elif self.value == 7:
                gameDisplay.blit(image_square7, self.rect)
            elif self.value == 8:
                gameDisplay.blit(image_square8, self.rect)
        #If unopened
        else:
            #Flag
            if self.flagged:
                gameDisplay.blit(image_flag, self.rect)
            #Untouched
            else:
                gameDisplay.blit(image_square, self.rect)

    def reveal(self):
        self.opened = True
        #Auto reveal all mines if mine is revealed
        if self.value == -1:
            for m in mines:
                if not grid[m[1]][m[0]].opened:
                    grid[m[1]][m[0]].reveal()
        # Auto reveal if value is 0
        elif self.value == 0:
            for x in range(-1,2): #Check left and right
                if self.x + x >= 0 and self.x + x < gridWidth:
                    for y in range(-1,2): #Check above and below
                        if self.y + y >= 0 and self.y + y < gridHeight:
                            if not grid[self.y + y][self.x + x].opened: #If not opened, open
                                grid[self.y + y][self.x + x].reveal()

    def update(self):
        if self.value != -1: #Skip if bomb
            for x in range(-1,2): #Check left and right
                if self.x + x >= 0 and self.x + x < gridWidth:
                    for y in range(-1,2): #Check above and below
                        if self.y + y >= 0 and self.y + y < gridHeight:
                            if grid[self.y + y][self.x + x].value == -1: #If bomb found, increase by 1
                                self.value += 1
def gameLoop():
    time = 0
    gameState = "Play"
    minesLeft = numMines
    global grid
    grid = []
    global mines
    mines = []

    #Generate Mines
    for i in range(numMines):
        mine_location = [random.randrange(0, gridWidth), random.randrange(0, gridHeight)]
        while mine_location in mines:
            mine_location = [random.randrange(0, gridWidth), random.randrange(0, gridHeight)]
        mines.append(mine_location)

    #Generate grid
    for j in range(gridHeight):
        row = []
        for i in range(gridWidth):
            if [i,j] in mines:
                row.append(Square(i,j, -1))
            else:
                row.append(Square(i,j, 0))
        grid.append(row)

    #Update grid
    for i in grid:
        for j in i:
            j.update()
    #Main loop
    while gameState != "Exit":
        gameDisplay.fill(LIGHT_GRAY)
        
        for j in grid:
            for i in j:
                i.draw()

        #For events
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                # Left click on field
                                if event.button == 1:
                                    j.reveal()
                                    # Toggle flag off
                                    if j.flagged:
                                        minesLeft += 1
                                        j.flagged = False
                                    # If it's a mine
                                    if j.value == -1:
                                        gameState = "Game Over"
                                        j.mineOpened = True
                                elif event.button == 3:
                                    # If the player right clicked
                                    if not j.opened:
                                        # Toggle flag off
                                        if j.flagged:
                                            j.flagged = False
                                            minesLeft += 1
                                        #Toggle flag on
                                        else:
                                            j.flagged = True
        
                                            minesLeft -= 1
        #Check if won
        won = True
        for j in grid:
            for i in j:
                if i.value != -1 and not i.opened:
                    won = False
            if not won:
                break
        if won and gameState != "Exit":
            gameState = "Won"

        #Draw text
        if gameState == "Play":
            time += 1
        elif gameState == "Won":
            drawText("You WON!", 50, -210 , GREEN)
            drawText("R to restart", 35, -175)
        elif gameState == "Game Over":
            drawText("Game Over!", 50, -210 , RED)
            drawText("R to restart", 35, -175)
            for i in grid:
                for j in i:
                    if j.flagged and j.value != -1:
                        j.mineWrong = True

        #Draw mines left
        screen_text = pygame.font.SysFont("Calibri", 50).render(minesLeft.__str__(), True, DARK_GRAY)
        gameDisplay.blit(screen_text, (gameWidth - border - 50, border))

        #Draw Score
        score = str(time // 15)
        screen_text = pygame.font.SysFont("Calibri", 50).render(score, True, DARK_GRAY)
        gameDisplay.blit(screen_text, (border, border))

        
        pygame.display.update()  # Update screen

        timer.tick(15)  # Tick fps


gameLoop()
pygame.quit()
quit()