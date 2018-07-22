# Threes
# By othermoose

import random, pygame, sys
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
TILEHEIGHT = 80 
TILEWIDTH = 60
GAPSIZE = 20 # size of gaps between tiles
BOARDSIZE = 4 # how many rows and columns are there

XMARGIN = int((WINDOWWIDTH - (BOARDSIZE * (TILEWIDTH + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - ((BOARDSIZE + 1) * (TILEHEIGHT + GAPSIZE))) / 2)

BOARDWIDTH = TILEWIDTH * BOARDSIZE + GAPSIZE * (BOARDSIZE - 1)

DARKGRAY = (40,40,40)
LIGHTGRAY = (50,50,50)
WHITE = (220,220,220)
BLUE = (85, 153, 255)
RED = (251, 89, 154)
BLACK = (0,0,0)


BGCOLOUR = DARKGRAY
EMPTYTILECOLOUR = LIGHTGRAY
TILECOLOUR = WHITE 
ONECOLOUR = BLUE
TWOCOLOUR = RED

ANIMATESPEED = 10 # pixels per frame

THREE = 1
TWO = -2
ONE = -1

def main():
        global FPSCLOCK, DISPLAYSURF, FONT, nextNum
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        FONT = pygame.font.Font('freesansbold.ttf', 32)

        mainBoard = generateRandomBoard()

        DISPLAYSURF.fill(BGCOLOUR)

        nextNum = randomTile(mainBoard)

        while True: # main loop
                DISPLAYSURF.fill(BGCOLOUR)
                drawBoard(mainBoard)
                drawNext()

                for event in pygame.event.get():
                        if event.type == QUIT or (event.type == KEYUP and (event.key == K_ESCAPE or event.key == K_q)):
                                pygame.quit()
                                sys.exit()
                        elif event.type == KEYDOWN: # key was pressed
                                if event.key == K_UP or event.key == K_w:
                                        slideBoard(mainBoard, "up")
                                elif event.key == K_LEFT or event.key == K_a:
                                        slideBoard(mainBoard, "left")
                                elif event.key == K_DOWN or event.key == K_s:
                                        slideBoard(mainBoard, "down")
                                elif event.key == K_RIGHT or event.key == K_d:
                                        slideBoard(mainBoard, "right")
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def generateRandomBoard(): # generates the board structure with a random starting state
        board = []
        for x in range(BOARDSIZE):
                column = []
                for y in range(BOARDSIZE):
                        column.append(random.choice([ONE,ONE,ONE,TWO,TWO,TWO,0,0,0,0,0,0,0,0,0,0])) 
                board.append(column)
        return board

def drawBoard(board): # draws the board onto the screen
        for tilex in range(BOARDSIZE):
                for tiley in range(BOARDSIZE): #tilex, tiley = row, column of current tile
                        left, top = getTopLeftCorner(tilex, tiley)
                        if board[tilex][tiley] == 0: # empty tile
                                pygame.draw.rect(DISPLAYSURF, EMPTYTILECOLOUR, (left, top, TILEWIDTH, TILEHEIGHT))
                        else: # tile is not empty
                                # ONEs and TWOs have special backgrounds
                                if board[tilex][tiley] == ONE:
                                        pygame.draw.rect(DISPLAYSURF, ONECOLOUR, (left, top, TILEWIDTH, TILEHEIGHT))
                                elif board[tilex][tiley] == TWO: 
                                        pygame.draw.rect(DISPLAYSURF, TWOCOLOUR, (left, top, TILEWIDTH, TILEHEIGHT))
                                else:
                                        pygame.draw.rect(DISPLAYSURF, TILECOLOUR, (left, top, TILEWIDTH, TILEHEIGHT))
                                # draw text
                                drawNum(board[tilex][tiley], (left + left + TILEWIDTH) / 2, (top + top + TILEHEIGHT) / 2)


def drawNum(number, x, y): # draws the numbers on the tiles
        fontColour = BLACK
        # turn numbers used in table into numbers understandable by people
        if number == ONE:  
                number = 1
                fontColour = WHITE # ONEs and TWOs have special colouring
        elif number == TWO:
                number = 2
                fontColour = WHITE
        else:
                number = 3 * (2 ** (number - 1))

        # rendering and blitting onto the main surface
        surface = FONT.render(str(number), True, fontColour)
        rect = surface.get_rect()
        rect.center = (x, y)
        DISPLAYSURF.blit(surface, rect)

def drawNext(): # draws the next number coming
        global nextNum
        if nextNum > 0:
                number = 3 * (2 ** (nextNum - 1))
        else:
                number = -nextNum
                
        if nextNum == ONE:
                pygame.draw.rect(DISPLAYSURF, ONECOLOUR, (XMARGIN, YMARGIN, BOARDWIDTH, TILEHEIGHT / 2))
        elif nextNum == TWO: 
                pygame.draw.rect(DISPLAYSURF, TWOCOLOUR, (XMARGIN, YMARGIN, BOARDWIDTH, TILEHEIGHT / 2))
        else:
                pygame.draw.rect(DISPLAYSURF, TILECOLOUR, (XMARGIN, YMARGIN, BOARDWIDTH, TILEHEIGHT / 2))

def getTopLeftCorner(tilex, tiley): # gets pixel coords of tile in specified row and column
        x = tilex * (TILEWIDTH + GAPSIZE) + XMARGIN
        y = (tiley + 1) * (TILEHEIGHT + GAPSIZE) + YMARGIN
        return x, y

def slideBoard(board, direction): # slides the tiles up
        moved = []
        if direction == 'up' or direction == "left":
                start = 0
                stop = BOARDSIZE
                increment = 1
        elif direction == 'down' or direction == 'right': # for these directions, the loop needs to go in reverse
                start = BOARDSIZE
                stop = -1
                increment = -1
                
        for tilex in range(start, stop, increment):
                for tiley in range(start, stop, increment):
                        # get coordinate of tile being moved into based on direction
                        if direction == "up":
                                targetTilex = tilex
                                targetTiley = tiley - 1
                        elif direction == "left":
                                targetTilex = tilex - 1
                                targetTiley = tiley
                        elif direction == "down":
                                targetTilex = tilex
                                targetTiley = tiley + 1
                        elif direction == "right":
                                targetTilex = tilex + 1
                                targetTiley = tiley
                                
                        moveValidity = checkValidity(board, tilex, tiley, targetTilex, targetTiley)
                        if moveValidity >= 0:
                                moved.append((tilex, tiley, board[tilex][tiley]))
                        if  moveValidity == 1: # valid move, two numbers that are the same
                                board[targetTilex][targetTiley] += 1
                                board[tilex][tiley] = 0
                        elif moveValidity == 2: # valid move, combining a one and a two
                                board[targetTilex][targetTiley] = 1
                                board[tilex][tiley] = 0
                        elif moveValidity == 0: # valid move, moving into empty space
                                board[targetTilex][targetTiley] = board[tilex][tiley]
                                board[tilex][tiley] = 0
        if len(moved) > 0:
                moved.append(addNewTile(board, moved, direction))
        animate(board, moved, direction)

def animate(board, moved, direction):
        xOffset = 0
        yOffset = 0

        if direction == 'up' or direction == 'down':
                end = TILEHEIGHT                        
        elif direction == 'left' or direction == 'right':
                end = TILEWIDTH
        for offset in range(0, end + GAPSIZE + 1, ANIMATESPEED):
                for tile in moved:
                        if tile[2] == ONE:
                                tileColour = ONECOLOUR
                        elif tile[2] == TWO:
                                tileColour = TWOCOLOUR
                        else:
                                tileColour = TILECOLOUR
                        left, top = getTopLeftCorner(tile[0], tile[1])
                        if direction == 'up':
                                yOffset = -offset
                        elif direction == "left":
                                xOffset = -offset
                        elif direction == "down":
                                yOffset = offset
                        elif direction == "right":
                                xOffset = offset
                        pygame.draw.rect(DISPLAYSURF, BGCOLOUR, (left - GAPSIZE, top - GAPSIZE, TILEWIDTH + GAPSIZE * 2, TILEHEIGHT + GAPSIZE * 2)) # draw first the dark gray background (margin area)
                        if moved.index(tile) != len(moved) - 1: # if this is the last thing to move, its the new tile
                                pygame.draw.rect(DISPLAYSURF, EMPTYTILECOLOUR, (left, top, TILEWIDTH, TILEHEIGHT)) # draw second the blank tile background
                        pygame.draw.rect(DISPLAYSURF, tileColour, (left + xOffset, top + yOffset, TILEWIDTH, TILEHEIGHT)) # now draw the moved tile
                        drawNum(tile[2], (left + left + TILEWIDTH) / 2 + xOffset, (top + top + TILEHEIGHT) / 2 + yOffset) # tile[2] = number that we saved in slideBoard
                drawNext()
                pygame.display.update()
                FPSCLOCK.tick(FPS)
        pygame.event.clear() # makes it so that you can't stack movements while animation is happening



def addNewTile(board, moved, direction):
        global nextNum
        oldNum = nextNum
        tile = random.choice(moved)
        if direction == 'up':
                tilex = tile[0]
                tiley = 4
                board[tilex][3] = nextNum
        elif direction == 'left':
                tilex = 4
                tiley = tile[1]
                board[3][tiley] = nextNum
        elif direction == 'down':
                tilex = tile[0]
                tiley = -1
                board[tilex][0] = nextNum
        elif direction == 'right':
                tilex = -1
                tiley = tile[1]
                board[0][tiley] = nextNum
        nextNum = randomTile(board)
        return (tilex, tiley, oldNum)


                                
def randomTile(board):
        choices = [ONE,TWO,THREE,THREE]
        for x in range(BOARDSIZE):
                for y in range(BOARDSIZE):
                        if board[x][y] == TWO:
                                choices.append(ONE)
                        elif board[x][y] == ONE:
                                choices.append(TWO)     
        return random.choice(choices)

def checkValidity(board, tilex, tiley, targetTilex, targetTiley): # 1 = success, -1 = no success, 2 = success pairing 1 and 2, 0 = moving into an empty tile
        if targetTilex == -1 or targetTiley == -1 or targetTilex >= BOARDSIZE or targetTiley >= BOARDSIZE:
                return -1
        tileOne = board[tilex][tiley]
        tileTwo = board[targetTilex][targetTiley]
        if tileOne == tileTwo and tileOne >= 1:
                return 1
        elif (tileOne == -1 and tileTwo == -2) or (tileOne == -2 and tileTwo == -1):
                return 2
        elif tileOne != 0 and tileTwo == 0:
                return 0
        else:
                return -1

main()

                  

