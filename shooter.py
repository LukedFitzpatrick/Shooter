import pygame
from pygame.locals import *
import pyganim
from random import randrange

#Initialisation
#
pygame.init()

SCREENWIDTH=800 #25 tiles wide
SCREENHEIGHT=480 #15 tiles high

windowSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
background_colour = (255,255,255)
clock = pygame.time.Clock()

# create the PygAnimation objects
playerStandingFlip = pyganim.PygAnimation([('player1.png', 0.4), ('player2.png', 0.4)])
playerWalkingFlip = pyganim.PygAnimation([('player1.png', 0.4), ('player2.png', 0.4)])
playerStanding = pyganim.PygAnimation([('player1flip.png', 0.4), ('player2flip.png', 0.4) ])
playerWalking = pyganim.PygAnimation([('player1flip.png', 0.4), ('player2flip.png', 0.4)])
bullet = pyganim.PygAnimation([('bullet.png', 0.4)])
monster1 = pyganim.PygAnimation([('monster.png', 0.4)])
playerStanding.play()
playerWalking.play()
playerStandingFlip.play()
playerWalkingFlip.play()
bullet.play()
monster1.play()

screenShake = 0
screenShakeOn = False
screenShakeCountdown = 20

wall = pygame.image.load('platform.png')
platform = pygame.image.load('wall.png')


def resetGame():
    global bullets, monsters, keysDown, walking, flip, playerx, playery, playerxv, playeryv, playerHeight, playerWidth
    global alive, playerRunSpeed, playerJumpSpeed, wallBounceFactor, bottomBounceFactor, topBounceFactor
    global bulletLifetime, totalCooldown, cooldown, bulletSpeed, grid, monsterCooldown
    bullets = []
    monsters = []
    keysDown = []
    grid = []
    generateGrid()
    walking = False
    flip = False

    #starting position
    playerx = (SCREENWIDTH-32)
    playery = (SCREENHEIGHT-64)
    playerxv = 0
    playeryv = 0
    playerHeight = 32
    playerWidth = 32

    alive = True

    playerRunSpeed = 0.5
    playerJumpSpeed = 12

    wallBounceFactor = -0.5
    bottomBounceFactor = -0.3
    topBounceFactor = -0.5
    #How many frames bullets last for
    bulletLifetime = 50
    #How many frames between each bullet
    totalCooldown = 10
    cooldown = 0
    #How fast the bullet travels
    bulletSpeed = 30

    monsterCooldown = 0

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
    global walking
    global bullets
    global cooldown
    global grid
    global alive
    global screenShakeCountdown
    global screenShakeOn

    #key handling
    if (K_d in keysDown):
        playerxv += playerRunSpeed
        flip = True
    if (K_a in keysDown):
        playerxv -= playerRunSpeed
        flip = False
    #jump
    if (K_w in keysDown):
        if(playery <= (SCREENHEIGHT - playerHeight)):
            keysDown.remove(K_w)
            playeryv -= playerJumpSpeed
    #shooting
    if (K_SPACE in keysDown):
        if(cooldown <= 0):
            direction = 0
            if (flip == True):
                direction = 1
            bulletInstance = [playerx, playery+(playerWidth/2), bulletLifetime, direction]
            bullets.append(bulletInstance)
            cooldown = totalCooldown 
            if(flip == True):
                playerxv -= 1
            else:
                playerxv += 1
            screenShakeOn = True
            screenShakeCountdown = 20
    cooldown -= 1

    #boundary collisions
    if (playerx < 0):
        playerx = 0
        playerxv *= wallBounceFactor
    if (playerx > (SCREENWIDTH-playerWidth)):
        playerx = SCREENWIDTH-playerWidth
        playerxv *= wallBounceFactor
    if (playery > (SCREENHEIGHT-playerHeight)):
        alive = False
    if (playery < 0):
        playery = 0
        playeryv *= topBounceFactor


    #changing animations from standing to running
    if( (playerxv < 2) and (playerxv > -2)):
        walking = False
    else:
        walking = True

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
    global walking
    global flip
    
    #decide which sprite to display
    if (walking == False):
        if (flip == False):
            playerStanding.blit(windowSurface, (playerx+screenShake, playery+screenShake))
        else:
            playerStandingFlip.blit(windowSurface, (playerx+screenShake, playery+screenShake))
    else:
        if (flip == False):
            playerWalking.blit(windowSurface, (playerx+screenShake, playery+screenShake))
        else:
            playerWalkingFlip.blit(windowSurface, (playerx+screenShake, playery+screenShake)) 


def bulletMonsterCollision(playerx, playery, monsterx, monstery):
    if ((playerx + 4) > monsterx) and ((playerx+4) < (monsterx + 32)):
        if ((playery + 4) > monstery) and ((playery+4) < (monstery + 32)):
            return True
    if ((playerx) > monsterx) and ((playerx) < (monsterx + 32)):
        if ((playery) > monstery) and ((playery) < (monstery + 32)):
            return True
    if ((playerx + 8) > monsterx) and ((playerx+8) < (monsterx + 32)):
        if ((playery + 8) > monstery) and ((playery+8) < (monstery + 32)):
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
            bullet.blit(windowSurface, (i[0], i[1]))
            i[2] = i[2] - 1
            if(i[3] == 0):
                          
                i[0] -= bulletSpeed
            else:
                i[0] += bulletSpeed    
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
    global alive
    for i in monsters:
        monster1.blit(windowSurface, (i[0], i[1]))
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
            alive = False

def createMonster():
    global monsters
    xStart = randrange(0, SCREENWIDTH - 32)
    direction = randrange(0, 1)
    singleMonster = [xStart, 0, 3, direction, 1]
    monsters.append(singleMonster)

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


def displayGrid():
    global grid
    global screenShake
    global screenShakeOn
    global screenShakeCountdown
    if(screenShakeOn == True):
        if screenShake == 0:
            screenShake = 3
        else:
            screenShake = 0
    else:
        screenShake = 0
    screenShakeCountdown -= 1
    if (screenShakeCountdown < 0):
        screenShakeCountdown = 20
        screenShakeOn = False
    
    

    
    for x in range(0, 25):
        for y in range(0, 15):
            image = wall
            if (grid[x][y] == 0): image = wall
            elif (grid[x][y] == 1): image = platform
            windowSurface.blit(image, ((x*32) + screenShake, (y*32) + screenShake))
    

def playGame():
    global alive
    global monsters
    global monsterCooldown
    
    while alive == True: # main loop
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

        if monsterCooldown <= 0:
            createMonster()
            monsterCooldown = randrange(10, 200)
        else:
            monsterCooldown-=1
      
        pygame.display.update()

        
while True:
    displayTitleScreen()
    resetGame()
    playGame()
