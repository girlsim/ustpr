import pygame
import math

import data
import objects
from helpers import *

class MagicBullet(objects.Bullet): # Inspector Hound's basic bullet

    def __init__(self,centerPoint):

	img = load_image('magic-bullet.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]

	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 3
	self.xMove,self.yMove = 0,-8

    def update(self,enemyGroup):

	objects.Bullet.update(self,enemyGroup)

class MagicMissile(objects.Bullet): # Inspector Hound's first-level charge bullet

    def __init__(self,centerPoint):

	img = load_image('magic-missile.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]

	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 3
	self.xMove,self.yMove = 0,-2
	self.maxSpeed = -15

    def update(self,enemyGroup):

	objects.Bullet.update(self,enemyGroup)
	if self.yMove > self.maxSpeed:
	    self.yMove -= 1

class OrmrinnDagger(objects.Bullet):

    def __init__(self,centerPoint):

	img = load_image('ormrinn-dagger.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]

	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 5

	self.xMove,self.yMove = 0,-10

    def update(self,enemyGroup):

	objects.Bullet.update(self,enemyGroup)

class faerieBullet(objects.Bullet):

    def __init__(self,centerPoint,angle):
	self.angle = angle
	img = load_image('faerie-bullet.png',-1)
	imgRotation = ((self.angle * -1) - 90)
	self.imageList = [pygame.transform.rotate(img, imgRotation)]
	self.deathImageList = [self.imageList[0]]
	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 1
	self.speed = 4

    def update(self,playerGroup):

	objects.Bullet.angleMove(self)
	objects.Bullet.update(self,playerGroup)

class bakehaBullet(objects.Bullet):

    def __init__(self,centerPoint):
	self.angle = 90
	img = load_image('bakeha-bullet.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 1
	self.speed = 5

    def update(self,playerGroup):

	objects.Bullet.angleMove(self)
	objects.Bullet.update(self,playerGroup)

class kitsuneBullet(objects.Bullet):

    def __init__(self,centerPoint):
	self.angle = 90
	img = load_image('monsterbullet.png',-1)
	img = pygame.transform.rotate(img,self.angle)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 1
	self.speed = 6

    def update(self,playerGroup):

	objects.Bullet.angleMove(self)
	objects.Bullet.update(self,playerGroup)

class suikoBullet(objects.Bullet):

    def __init__(self,centerPoint,angle):
	self.angle = angle
	img = load_image('suiko-bullet.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 1
	self.speed = 0
	self.maxSpeed = 10

    def update(self,playerGroup):

	objects.Bullet.angleMove(self)
	objects.Bullet.update(self,playerGroup)
	if self.speed < self.maxSpeed:
	    self.speed += .25

class bakehaExplode(objects.Bullet):

    def __init__(self,centerPoint):
	self.angle = 90
	img = load_image('bakeha-explode.png',-1)
	img = pygame.transform.rotate(img,self.angle)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Bullet.__init__(self,centerPoint,self.imageList)

	self.damage = 1
	self.speed = 6
	self.spin = 10
	self.stored_spin = 0

    def update(self,playerGroup):

	objects.Bullet.angleMove(self)
	objects.Bullet.update(self,playerGroup)
	if self.currentFrame < len(self.imageList):
	    self.image = pygame.transform.rotate(self.imageList[self.currentFrame],(self.stored_spin))
	self.stored_spin += self.spin
