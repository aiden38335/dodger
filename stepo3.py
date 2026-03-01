import pygame, random, sys
from pygame.locals import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
playerImage = pygame.image.load(str(ASSETS_DIR / "player.png"))

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type ==QUIT:
                terminate()
            if event.type ==KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return 


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)
playerRect = playerImage.get_rect()

windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()


waitForPlayerToPressKey()

playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50 )
moveLeft = moveRight = moveUp = moveDown = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = True
                moveLeft = False
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type ==KEYUP:
            if event.key == K_ESCAPE:
                terminate()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False

    if moveLeft and playerRect.left > 0:
        playerRect.move_ip(-1* PLAYERMOVERATE, 0)
    if moveRight and playerRect.right < WINDOWWIDTH:
        playerRect.move_ip(PLAYERMOVERATE, 0)
    if moveUp and playerRect.top > 0:
        playerRect.move_ip(0, -1* PLAYERMOVERATE)
    if moveDown and playerRect.bottom < WINDOWHEIGHT:
        playerRect.move_ip(0, PLAYERMOVERATE)

    windowSurface.fill(BACKGROUNDCOLOR)
    windowSurface.blit(playerImage, playerRect)

    
    pygame.display.update()
    mainClock.tick(FPS)