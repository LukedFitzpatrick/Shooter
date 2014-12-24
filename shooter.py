import pygame
from pygame.locals import *
from random import randrange
from graphics import *
from engine import *
from engineConstants import *


def resetGame():
    global bullets, monsters, keysDown, grid
    bullets, monsters, keysDown, grid = [], [], [], []

    generateGrid()
    
    global playerWalking, flip
    playerWalking = False
    flip = False
    
    global playerx, playery, playerxv, playeryv, playerAlive
    playerx, playery = PLAYERSTARTINGX, PLAYERSTARTINGY
    playerxv, playeryv = 0, 0
    playerAlive = True
    
    global currentBulletCooldown, currentMonsterCooldown
    currentBulletCooldown, currentMonsterCooldown = 0, 0
    
    global currentScreenShake, screenShakeOn, screenShakeCountdown
    currentScreenShake = 0
    screenShakeOn = False
    screenShakeCountdown = MAXSCREENSHAKECOUNTDOWN
    
    
def generateGrid():
    global grid
    grid = []
    line = []
    for x in range(0, 25):
        line = []
        for y in range(0, 15):
            line.append(0)
        grid.append(line)

    #platforms
    for x in range(9, 17):
        grid[x][3] = 1

    for x in range(0, 9):
        grid[x][6] = 1
    for x in range(17, 25):
        grid[x][6] = 1

    for x in range(6, 20):
        grid[x][11] = 1

    for x in range(0, 7):
        grid[x][14] =1
    for x in range(18, 25):
        grid[x][14] = 1
        
        
        
def displayTitleScreen():
   titleScreen = pygame.image.load('titleScreen.png').convert()
   windowSurface.blit(titleScreen, (0, 0))
   pygame.display.flip()
   buttonPressed = False
   while buttonPressed == False:
      for event in pygame.event.get():
         if event.type == pygame.KEYDOWN:
            buttonPressed = True

def updatePlayer():
    global keysDown
    global playerx
    global playery
    global playerxv
    global playeryv
    global flip
    global playerWalking
    global bullets
    global currentBulletCooldown
    global grid
    global playerAlive
    global screenShakeCountdown
    global screenShakeOn

    #key handling
    if (K_d in keysDown):
        playerxv += PLAYERRUNSPEED
        flip = True
    if (K_a in keysDown):
        playerxv -= PLAYERRUNSPEED
        flip = False
    #jump
    if (K_w in keysDown):
        if(playery <= (SCREENHEIGHT - PLAYERHEIGHT)):
            keysDown.remove(K_w)
            playeryv -= PLAYERJUMPSPEED
    #shooting
    if (K_SPACE in keysDown):
        if(currentBulletCooldown <= 0):
            direction = 0
            if (flip == True):
                direction = 1
            bulletInstance = [playerx, playery+(PLAYERWIDTH/2), BULLETLIFETIME, direction]
            bullets.append(bulletInstance)
            currentBulletCooldown = TOTALBULLETCOOLDOWN 
            if(flip == True):
                playerxv -= 1
            else:
                playerxv += 1
            screenShakeOn = True
            screenShakeCountdown = 20
    currentBulletCooldown -= 1

    #boundary collisions
    if (playerx < 0):
        playerx = 0
        playerxv *= WALLBOUNCEFACTOR
    if (playerx > (SCREENWIDTH-PLAYERWIDTH)):
        playerx = SCREENWIDTH-PLAYERWIDTH
        playerxv *= WALLBOUNCEFACTOR
    if (playery > (SCREENHEIGHT-PLAYERHEIGHT)):
        playerAlive = False
    if (playery < 0):
        playery = 0
        playeryv *= TOPBOUNCEFACTOR


    #changing animations from standing to running
    if( (playerxv < 2) and (playerxv > -2)):
        playerWalking = False
    else:
        playerWalking = True

    #gravity
    if( playery < (SCREENHEIGHT - 32)):
        playeryv += 0.5

    #find distance to nearest obstacle:
    obstacleDistance = playeryv #if no obstacles less than playeryv away, just move playeryv  
    playeryTile = int(playery/32)
    playerxTile = int(playerx/32)
    if (playeryv > 0): #falling down
        for tile in range(playeryTile+1, 15):
            if grid[playerxTile][tile] > 0:
                distanceToTile = (32*tile) - (playery + 32)
                if (distanceToTile < obstacleDistance):
                    obstacleDistance = distanceToTile
                    playeryv = 0
    elif (playeryv < 0):
        for tile in range(0, playeryTile):
            if grid[playerxTile][tile] > 0:
                distanceToTile = (32*(tile+1) - (playery))
                if (distanceToTile > obstacleDistance):
                    obstacleDistance = (-1 *distanceToTile)
                    playeryv = 0
    playery += obstacleDistance
    
    
    obstacleDistance = playerxv
    if (playerxv > 0):
        for tile in range(playerxTile+1, 25):
            if grid[tile][playeryTile] > 0:
                distanceToTile = (32*tile) - (playerx + 32)
                if (distanceToTile < obstacleDistance):
                    obstacleDistance = distanceToTile
                    playerxv = 0

    elif (playerxv < 0):
        for tile in range(0, playerxTile):
            if grid[tile][playeryTile] > 0:
                distanceToTile = (32*(tile+1) - playerx)
                if (distanceToTile > obstacleDistance):
                    obstacleDistance = (-distanceToTile)
                    playerxv = 0

    
    playerx += obstacleDistance
    



def displayScreen():
    global playerWalking
    global flip
    
    #decide which sprite to display
    if (playerWalking == False):
        if (flip == False):
            spritePlayerStanding.blit(windowSurface, (playerx+currentScreenShake, playery+currentScreenShake))
        else:
            spritePlayerStandingFlip.blit(windowSurface, (playerx+currentScreenShake, playery+currentScreenShake))
    else:
        if (flip == False):
            spritePlayerWalking.blit(windowSurface, (playerx+currentScreenShake, playery+currentScreenShake))
        else:
            spritePlayerWalkingFlip.blit(windowSurface, (playerx+currentScreenShake, playery+currentScreenShake)) 


def bulletMonsterCollision(bulletx, bullety, monsterx, monstery):
    if ((bulletx + 4) > monsterx) and ((bulletx+4) < (monsterx + 32)):
        if ((bullety + 4) > monstery) and ((bullety+4) < (monstery + 32)):
            return True
    if ((bulletx) > monsterx) and ((bulletx) < (monsterx + 32)):
        if ((bullety) > monstery) and ((bullety) < (monstery + 32)):
            return True
    if ((bulletx + 8) > monsterx) and ((bulletx+8) < (monsterx + 32)):
        if ((bullety + 8) > monstery) and ((bullety+8) < (monstery + 32)):
            return True
    return False

def playerMonsterCollision(playerx, playery, monsterx, monstery):
    if ((playerx + 16) > monsterx) and ((playerx+16) < (monsterx + 32)):
        if ((playery + 16) > monstery) and ((playery+16) < (monstery + 32)):
            return True
    if ((playerx) > monsterx) and ((playerx) < (monsterx + 32)):
        if ((playery) > monstery) and ((playery) < (monstery + 32)):
            return True
    if ((playerx + 32) > monsterx) and ((playerx+32) < (monsterx + 32)):
        if ((playery + 32) > monstery) and ((playery+32) < (monstery + 32)):
            return True
    return False

def updateBullets():
    global monsters
    global bullets
    global grid
    #update and display the bullets
    for i in bullets:    
        if(i[2] > 0):
            bulletxTile = int(i[0]/32)
            bulletyTile = int(i[1]/32)
            spriteBullet.blit(windowSurface, (i[0], i[1]))
            i[2] = i[2] - 1
            if(i[3] == 0):
                          
                i[0] -= BULLETSPEED
            else:
                i[0] += BULLETSPEED    
            #check for hitting monsters
            for monster in monsters:
                if (bulletMonsterCollision(i[0], i[1], monster[0], monster[1])):
                    if(i in bullets):
                        bullets.remove(i)
                        monster[4] -= 1
        else:
            bullets.remove(i)


def updateMonsters():
    global monsters
    global playerx
    global playery
    global playerAlive
    for i in monsters:
        spriteMonster1.blit(windowSurface, (i[0], i[1]))
        i[0] += i[2]
        if(i[0] < 0 or i[0] > (SCREENWIDTH-32)):
            i[2] *= -1
        if i[4] == 0:
            monsters.remove(i)
        #gravity
        if( i[1] < (SCREENHEIGHT - 32)):
            i[3] += 0.5
        
        #find distance to nearest obstacle:
        obstacleDistance = i[3] 
        monsteryTile = int(i[1]/32)
        monsterxTile = int(i[0]/32)
        if (i[3] > 0): #falling down
            for tile in range(monsteryTile+1, 15):
                if grid[monsterxTile][tile] >= 1:
                    distanceToTile = (32*tile) - (i[1] + 32)
                    if (distanceToTile < obstacleDistance):
                        obstacleDistance = distanceToTile
                        i[3] = 0
        i[1] += obstacleDistance
        if(i[1] > (SCREENHEIGHT)):
            i[1] = 0
            if (i[2]>0): i[2] += 2
            else: i[2] -= 2
        if(playerMonsterCollision(playerx, playery, i[0], i[1])):
            playerAlive = False

           
def createMonster():
    global monsters
    xStart = randrange(0, SCREENWIDTH - 32)
    direction = randrange(0, 1)
    singleMonster = [xStart, 0, 3, direction, 1]
    monsters.append(singleMonster)

def handleScreenShake():
    global screenShake
    global screenShakeOn
    global screenShakeCountdown
    
    if(screenShakeOn == True):
        if screenShake == 0:
            screenShake = SCREENSHAKEINCREMENT
        else:
            screenShake = 0
    else:
        screenShake = 0
    screenShakeCountdown -= 1
    
    if (screenShakeCountdown < 0):
        screenShakeCountdown = MAXSCREENSHAKECOUNTDOWN
        screenShakeOn = False        
        

def displayGrid():
    handleScreenShake()
    
    for x in range(0, 25):
        for y in range(0, 15):
            if (grid[x][y] == 0): image = wall
            elif (grid[x][y] == 1): image = platform
            windowSurface.blit(image, ((x*32) + screenShake, (y*32) + screenShake))
    

def playGame():

    global playerAlive
    global monsters
    global currentMonsterCooldown
    
    while playerAlive == True: # main loop
        time_passed = clock.tick(60)
        windowSurface.fill((0, 0, 0))
        #handle input
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                keysDown.append(event.key)
            if event.type == pygame.KEYUP:
                if(event.key in keysDown):
                    keysDown.remove(event.key)

        #update the player
        updatePlayer()
        
        displayGrid()
        displayScreen()
        updateBullets()
        updateMonsters()

        if currentMonsterCooldown <= 0:
            createMonster()
            currentMonsterCooldown = randrange(FASTESTMONSTERGEN, SLOWESTMONSTERGEN)
        else:
            currentMonsterCooldown-=1
      
        pygame.display.update()



        
#Initialisation
#
pygame.init()

windowSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
background_colour = (255,255,255)
clock = pygame.time.Clock()
        
while True:
    displayTitleScreen()
    resetGame()
    playGame()
