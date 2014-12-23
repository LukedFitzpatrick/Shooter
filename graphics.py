import pygame
from pygame.locals import *
import pyganim

# create the PygAnimation objects
spritePlayerStandingFlip = pyganim.PygAnimation([('player1.png', 0.4), ('player2.png', 0.4)])
spritePlayerWalkingFlip = pyganim.PygAnimation([('player1.png', 0.4), ('player2.png', 0.4)])
spritePlayerStanding = pyganim.PygAnimation([('player1flip.png', 0.4), ('player2flip.png', 0.4) ])
spritePlayerWalking = pyganim.PygAnimation([('player1flip.png', 0.4), ('player2flip.png', 0.4)])
spriteBullet = pyganim.PygAnimation([('bullet.png', 0.4)])
spriteMonster1 = pyganim.PygAnimation([('monster.png', 0.4)])

spritePlayerStanding.play()
spritePlayerWalking.play()
spritePlayerStandingFlip.play()
spritePlayerWalkingFlip.play()
spriteBullet.play()
spriteMonster1.play()

wall = pygame.image.load('platform.png')
platform = pygame.image.load('wall.png')