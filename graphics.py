import pygame
from pygame.locals import *
import pyganim

# create the PygAnimation objects
spritePlayerStandingFlip = pyganim.PygAnimation([('graphics/player1.png', 0.4), ('graphics/player2.png', 0.4)])
spritePlayerWalkingFlip = pyganim.PygAnimation([('graphics/player1.png', 0.4), ('graphics/player2.png', 0.4)])
spritePlayerStanding = pyganim.PygAnimation([('graphics/player1flip.png', 0.4), ('graphics/player2flip.png', 0.4) ])
spritePlayerWalking = pyganim.PygAnimation([('graphics/player1flip.png', 0.4), ('graphics/player2flip.png', 0.4)])
spriteBullet = pyganim.PygAnimation([('graphics/bullet.png', 0.4)])
spriteMonster1 = pyganim.PygAnimation([('graphics/monster.png', 0.4)])

spritePlayerStanding.play()
spritePlayerWalking.play()
spritePlayerStandingFlip.play()
spritePlayerWalkingFlip.play()
spriteBullet.play()
spriteMonster1.play()

wall = pygame.image.load('graphics/platform.png')
platform = pygame.image.load('graphics/wall.png')