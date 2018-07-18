# Threes
# By othermoose

import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
TILEHEIGHT = 80 
TILEWIDTH = 60
GAPSIZE = 20 # size of gaps between tiles
BOARDSIZE = 4 # how many rows and columns are there

XMARGIN = int((WINDOWWIDTH - (BOARDSIZE * (TILEWIDTH + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDSIZE * (TILEHEIGHT + GAPSIZE))) / 2)

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

THREE = 1
TWO = -2
ONE = -1

def main():
	global FPSCLOCK, DISPLAYSURF, FONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	FONT = pygame.font.Font('freesansbold.ttf', 32)

	mainBoard = generateRandomBoard()

	DISPLAYSURF.fill(BGCOLOUR)

	while True: # main loop
		DISPLAYSURF.fill(BGCOLOUR)
		drawBoard(mainBoard)
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and (event.key == K_ESCAPE or event.key == K_q)):
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN: # key was pressed
				if event.key == K_UP or event.key == K_w:
					slideBoard(mainBoard)
				elif event.key == K_LEFT or event.key == K_a:
					rotateBoard(mainBoard)
					rotateBoard(mainBoard)
					rotateBoard(mainBoard)
					slideBoard(mainBoard)
					rotateBoard(mainBoard)
				elif event.key == K_DOWN or event.key == K_s:
					rotateBoard(mainBoard)
					rotateBoard(mainBoard)
					slideBoard(mainBoard)
					rotateBoard(mainBoard)
					rotateBoard(mainBoard)
				elif event.key == K_RIGHT or event.key == K_d:
					rotateBoard(mainBoard)
					slideBoard(mainBoard)
					rotateBoard(mainBoard)
					rotateBoard(mainBoard)
					rotateBoard(mainBoard)

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

def getTopLeftCorner(tilex, tiley): # gets pixel coords of tile in specified row and column
	x = tilex * (TILEWIDTH + GAPSIZE) + XMARGIN
	y = tiley * (TILEHEIGHT + GAPSIZE) + YMARGIN
	return x, y

def slideBoard(board): # slides the tiles up
	moved = []
	for tilex in range(BOARDSIZE):
		for tiley in range(1, BOARDSIZE):
			moveValidity = checkValidity(board, tilex, tiley) 
			if  moveValidity == 1: # valid move, two numbers that are the same
				board[tilex][tiley - 1] += 1
				board[tilex][tiley] = 0
			elif moveValidity == 2: # valid move, combining a one and a two
				board[tilex][tiley - 1] = 1
				board[tilex][tiley] = 0
			elif moveValidity == 0: # valid move, moving into empty space
				board[tilex][tiley - 1] = board[tilex][tiley]
				board[tilex][tiley] = 0
			if moveValidity >= 0:
				moved.append(tilex)
	addNewTile(board, moved)

def addNewTile(board, moved):
	if len(moved) > 0:
		tilex = random.choice(moved)
		board[tilex][3] = randomTile(board)
				
def randomTile(board):
	choices = [ONE,TWO,THREE,THREE]
	for x in range(BOARDSIZE):
		for y in range(BOARDSIZE):
			if board[x][y] == TWO:
				choices.append(ONE)
			elif board[x][y] == ONE:
				choices.append(TWO)	
	return random.choice(choices)

def rotateBoard(board): # rotates the board 90 degrees counterclockwise
	# make a copy of the board
	copy = [[0 for x in range(BOARDSIZE)] for y in range(BOARDSIZE)]
	for x in range(BOARDSIZE): 
		for y in range(BOARDSIZE):
			copy[x][y] = board[x][y]

	for x in range(BOARDSIZE): # rotate the board
		for y in range(BOARDSIZE):
			board[y][BOARDSIZE - x - 1] = copy[x][y]

def checkValidity(board, tilex, tiley): # 1 = success, -1 = no success, 2 = success pairing 1 and 2, 0 = moving into an empty tile
	tileOne = board[tilex][tiley]
	tileTwo = board[tilex][tiley - 1]
	if tileOne == tileTwo and tileOne >= 1:
		return 1
	elif (tileOne == -1 and tileTwo == -2) or (tileOne == -2 and tileTwo == -1):
		return 2
	elif tileOne != 0 and tileTwo == 0:
		return 0
	else:
		return -1

main()

          

