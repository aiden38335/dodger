import pygame, random, sys
from pygame.locals import *
from pathlib import Path

#Final version of the dodger game
# Directory --> a way of importing fileswithout having to move to other files, its like a parent file 
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
#player image is recallinga player image
playerImage = pygame.image.load(str(ASSETS_DIR / "player.png"))
# baddie image is bringing the baddie image file 
baddieImage = pygame.image.load(str(ASSETS_DIR / "baddie.png"))

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

# it revolves and circles around in a loop until a key is pressed and the loop stops 
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

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies: 
        if playerRect.colliderect(b['rect']):
            return True 
    return False

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)

#bringing the game sound in
game_over_sound = pygame.mixer.Sound(str(ASSETS_DIR/'gameover.wav'))
pygame.mixer.music.load(str(ASSETS_DIR/'background.mid'))

playerRect = playerImage.get_rect()

windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()


waitForPlayerToPressKey()

playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50 )
moveLeft = moveRight = moveUp = moveDown = False

baddies = []
baddieAddCounter = 0

topScore = 0

while True:
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    move_left = move_right = move_up = move_down = False
    baddie_add_counter = 0

    #MUSIC song on 
    pygame.mixer.music.play(-1,0.0)

    while True: 
        score += 1

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

        #if key is up then there will be no movement like a break mechanim

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1* PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1* PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

# Start
# this is the part where it codes for the loop of the baddie consistently comming out but also codes for the where the baddie is spawned
        baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {
                'rect': pygame.Rect(
                    random.randint(0, WINDOWWIDTH - baddieSize),
                    0- baddieSize, 
                    baddieSize,
                    baddieSize
                ),
                'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))
            }
            baddies.append(newBaddie)

        for b in baddies:
            b['rect'].move_ip(0, b['speed'])
        
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

# End
        windowSurface.fill(BACKGROUNDCOLOR)
        
        drawText(f"Score: {score}", font, windowSurface, 10, 0)
        drawText(f"Top Score: {topScore}", font, windowSurface, 10, 40)
        
        
        windowSurface.blit(playerImage, playerRect)

        for b in baddies: 
            windowSurface.blit(b['surface'], b['rect'])

        
        pygame.display.update()
# if score is over topscore change top score to score 
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score
            break
        mainClock.tick(FPS)


    pygame.mixer.music.stop()
    game_over_sound.play()

    
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH /3), (WINDOWHEIGHT/3))
    drawText(' PRESS a key to play again.', font, windowSurface, (WINDOWWIDTH/3)-80, (WINDOWHEIGHT/3)+50)

    pygame.display.update()
    waitForPlayerToPressKey()