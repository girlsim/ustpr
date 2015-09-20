import pygame
import math
import random

import data
import objects
import projectiles
from helpers import *

######## Dummy monster for spawning dialogues #######

class DialogueDummy(objects.Monster):

    def __init__(self,dialogue): # takes the dialogue instead of coordinates in the level's monster list

	self.imageList = [load_image("hitbox.png",-1)]
	objects.Monster.__init__(self,(0,0),self.imageList)

	self.dialogue = dialogue

    def update(self): # note that this makes the dialogue start on the refresh /after/ the monster spawns, rather than right away

	data.dialogue_on = True
	data.current_dialogue = self.dialogue()
	self.kill()

######## Faerie ##########

class Faerie(objects.Monster):

    def __init__(self,centerPoint):

	img = load_image('faerie.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Monster.__init__(self,centerPoint,self.imageList)

	self.health = 40
	self.xMove,self.yMove = 0,0

	self.currentAI = self.moveDownAI # move down a certain distance, fire for a while, move back up

	self.ai_counter = 0
	self.move_max = 20
	self.fire_max = 100
	self.wait_max = 150
	self.move_up_speed = -8

	self.bullet_angle = 0
	self.bullet_angle_change = 30
	self.bullet_base_change = 5

	self.firing = False

	self.speed = 5

	self.angle = 0

	self.drops = [[[load_image('power-block-big.png',-1)],"power",.5],[[load_image('points-block.png',-1)],"points",5],[[load_image('points-block.png',-1)],"points",5]]

    def update(self):

	self.currentAI()
	objects.Monster.update(self)

    def moveDownAI(self):

	if self.ai_counter < self.move_max:
	    self.ai_counter += 1
	    self.rect.move_ip(0,self.speed)
	else:
	    self.currentAI = self.fireAI
	    self.ai_counter = 0 # need to reset because the same counter is used for the other states

    def fireAI(self):

	if self.ai_counter < self.fire_max:
	    self.ai_counter += 1
	    while 360./(self.bullet_angle+1) > 1:
		bullet = projectiles.faerieBullet(self.rect.center,self.bullet_angle+self.bullet_base_change*self.ai_counter)
		data.monster_bullets.append(bullet)
		self.bullet_angle += self.bullet_angle_change
	    self.bullet_angle = 0

	else:
	    self.currentAI = self.waitAI
	    self.ai_counter = 0

    def waitAI(self):

	if self.ai_counter >= self.wait_max:
	    self.currentAI = self.moveUpAI
	    self.ai_counter = 0
	else:
	    self.ai_counter += 1

    def moveUpAI(self):

	self.speed = self.move_up_speed # because move_up_speed is negative and larger in magnitude than speed, this makes the faerie esscape from above
	self.currentAI = self.moveDownAI

######## Bakeha (placeholders because Finder is crashed and I can't get at image stuff) #######

class Bakeha(objects.Monster):

    def __init__(self,centerPoint):

	img = load_image('bakeha.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Monster.__init__(self,centerPoint,self.imageList)

	self.health = 5
	self.xMove,self.yMove = 0,0

	self.currentAI = self.crossAI

	self.fire_counter = 0
	self.fire_max = 20
	self.firing_counter = 0
	self.firing_max = 1
	self.firing = False

	self.speed = 5 # positive goes to the right, negative to the left
	if self.rect.x >= data.playable_width/2: # decide which direction to go in based on which side of the screen we're on
	    self.speed = -self.speed

	self.angle = 0

	if random.randint(0,1) == 1:
	    self.drops = [[[load_image('points-block.png',-1)],"score",5]]
	else:
	    self.drops = [[[load_image('power-block.png',-1)],"power",.05]]

    def update(self):

	self.currentAI()
	objects.Monster.update(self)

    def crossAI(self): # cross the screen firing, then disappear

	rotation = self.angle * (math.pi / 180)
	self.xMove = math.cos(rotation) * self.speed
	self.yMove = math.sin(rotation) * self.speed

	if self.firing == False:
	    self.fire_counter += 1
	    if self.fire_counter == self.fire_max:
		self.fire_counter = 0
		self.firing = True
	if self.firing == True:
	    self.basicFire()
	    self.firing_counter += 1
	    if self.firing_counter == self.firing_max:
		self.firing = False
		self.firing_counter = 0

    def basicFire(self):

	bullet = projectiles.bakehaBullet(self.rect.center)
	bullet.angle = 90
	data.monster_bullets.append(bullet)

######## Kitsune #########

class Kitsune(objects.Monster):

    def __init__(self,centerPoint):

	img = load_image('kitsune.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Monster.__init__(self,centerPoint,self.imageList)

	self.health = 20
	self.xMove,self.yMove = 0,0

	self.currentAI = self.circleAI

	self.fire_counter = 0
	self.fire_max = 20
	self.firing_counter = 0
	self.firing_max = 1
	self.firing = False

	self.moveAI_counter = 0
	self.moveAI_max = 40
	self.speed = 5
	self.angle = 60

	self.drops = [[[load_image('points-block.png',-1)],"score",10],[[load_image('power-block.png',-1)],"power",.2]]

    def update(self):

	self.currentAI()
	objects.Monster.update(self)

    def circleAI(self):

	if self.rect.x > data.playable_width and self.speed > 0:
	    self.speed = -self.speed
	if self.rect.x < 0 and self.speed < 0:
	    self.speed = -self.speed

	self.moveAI_counter += 1
	if self.moveAI_counter == self.moveAI_max:
	    self.angle = -self.angle
	    self.moveAI_counter = 0

	rotation = self.angle * (math.pi / 180)
	self.xMove = math.cos(rotation) * self.speed
	self.yMove = math.sin(rotation) * self.speed

	if self.firing == False:
	    self.fire_counter += 1
	    if self.fire_counter == self.fire_max:
		self.fire_counter = 0
		self.firing = True
	if self.firing == True:
	    self.basicFire()
	    self.firing_counter += 1
	    if self.firing_counter == self.firing_max:
		self.firing = False
		self.firing_counter = 0

    def basicFire(self):

	bullet = projectiles.kitsuneBullet(self.rect.center)
	bullet.angle = 120
	data.monster_bullets.append(bullet)
	bullet = projectiles.kitsuneBullet(self.rect.center)
	bullet.angle = 90
	data.monster_bullets.append(bullet)
	bullet = projectiles.kitsuneBullet(self.rect.center)
	bullet.angle = 60
	data.monster_bullets.append(bullet)
	data.HitSoundsChannel.play(data.FireSounds[1]) # play bullet hit sound

class ExplodeBakeha(objects.Monster):

    def __init__(self,centerPoint):

	img = load_image('bakeha.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Monster.__init__(self,centerPoint,self.imageList)

	self.health = 35
	self.xMove,self.yMove = 0,0

	self.currentAI = self.circleAI

	self.fire_counter = 0
	self.fire_max = 20
	self.firing_counter = 0
	self.firing_max = 1
	self.firing = False

	self.moveAI_counter = 0
	self.moveAI_max = 40
	self.speed = 5
	self.angle = 60

	self.exploded = False

	if random.randint(0,1) == 1:
	    self.drops = [[[load_image('points-block.png',-1)],"score",5]]
	else:
	    self.drops = [[[load_image('power-block.png',-1)],"power",.05]]

    def update(self):

	self.currentAI()
	objects.Monster.update(self)

    def circleAI(self):

	if self.rect.x > data.playable_width and self.speed > 0:
	    self.speed = -self.speed
	if self.rect.x < 0 and self.speed < 0:
	    self.speed = -self.speed

	self.moveAI_counter += 1
	if self.moveAI_counter == self.moveAI_max:
	    self.angle = -self.angle
	    self.moveAI_counter = 0

	rotation = self.angle * (math.pi / 180)
	self.xMove = math.cos(rotation) * self.speed
	self.yMove = math.sin(rotation) * self.speed

	if self.firing == False:
	    self.fire_counter += 1
	    if self.fire_counter == self.fire_max:
		self.fire_counter = 0
		self.firing = True
	if self.firing == True:
	    self.basicFire()
	    self.firing_counter += 1
	    if self.firing_counter == self.firing_max:
		self.firing = False
		self.firing_counter = 0

	if self.dying == True and self.exploded == False:

	    angle = 0
	    while angle < 360:
		bullet = projectiles.bakehaExplode(self.rect.center)
		bullet.angle = angle
		data.monster_bullets.append(bullet)
		angle += 10

    def basicFire(self):

	bullet = projectiles.bakehaBullet(self.rect.center)
	bullet.angle = 90
	data.monster_bullets.append(bullet)
	data.HitSoundsChannel.play(data.FireSounds[1]) # play bullet hit sound

########## Kawakami Suiko (boss) #########

class Suiko(objects.Monster):

    def __init__(self,centerPoint):

	img = load_image('kappa.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]
	objects.Monster.__init__(self,centerPoint,self.imageList)

	self.health = 1000
	self.xMove,self.yMove = 0,0

	self.AIswitchPoint = 500
	self.recordedX = 0

	self.goal = 325,50
	self.nextAI = self.bakehaSpawnAI
	self.nextGoal = 200,50
	self.nextNextAI = self.secondAI

	self.currentAI = self.transitionAI

	self.fire_counter = 0
	self.fire_max = 20
	self.firing_counter = 0
	self.firing_max = 41
	self.firing = False
	self.fireFunction = None

	self.spawn_bakeha_counter = 9

	self.moveAI_counter = 0
	self.moveAI_max = 40
	self.speed = 8
	self.oldSpeed = self.speed
	self.angle = 60
	self.angleFactor = 2.5
	self.oldFactor = self.angleFactor

	self.bulletAngleBase = 90
	self.bulletAngle = self.bulletAngleBase
	self.bulletAngleChange = 30

    def update(self):

	if self.health < self.AIswitchPoint and self.currentAI == self.bakehaSpawnAI:
	    self.currentAI = self.transitionAI
	self.currentAI()
	objects.Monster.update(self)

    def bakehaSpawnAI(self):

	self.angle += self.angleFactor

	if self.angle == 270 and self.angleFactor > 0 or self.angle == 90 and self.angleFactor < 0:
	    self.angleFactor = -self.angleFactor
	    self.speed = -self.speed
	    self.oldSpeed = self.speed
	    self.speed = 0
	    self.oldFactor = self.angleFactor
	    self.angleFactor = 0
	    self.firing = True
	    self.fireFunction = self.spawnBakeha
	    self.bulletAngle = self.bulletAngleBase
	    self.bulletAngleChange = -self.bulletAngleChange

	rotation = self.angle * (math.pi / 180)
	self.xMove = math.cos(rotation) * self.speed
	self.yMove = math.sin(rotation) * self.speed

	if self.firing:
	    self.firing_counter += 1
	    self.spawn_bakeha_counter += 1
	    bullet = projectiles.suikoBullet(self.rect.center,self.bulletAngle) # fire a bullet every refresh while firing
	    #x,y = self.rect.x,self.rect.y
	    #px,py = data.player.hitbox.rect.x,data.player.hitbox.rect.y
	    #bullet.angle = (180/math.pi) * math.acos((px-x)/math.sqrt((px-x)*(px-x)+(y-py)*(y-py)))
	    data.monster_bullets.append(bullet)
	    self.bulletAngle += self.bulletAngleChange
	    data.HitSoundsChannel.play(data.FireSounds[1]) # play bullet hit sound
	    if self.spawn_bakeha_counter == 10:
		self.fireFunction()
		self.spawn_bakeha_counter = 0
	    if self.firing_counter == self.firing_max:
		self.firing = False
		self.speed = self.oldSpeed
		self.angleFactor = self.oldFactor
		self.firing_counter = 0
		self.spawn_bakeha_counter = 9

    def transitionAI(self):

	self.xMove,self.yMove = 0,0

	x,y = self.goal
	if self.rect.x >= x-10 and self.rect.x <= x+10 and self.rect.y <= y+10 and self.rect.y >= y-10:
	    self.currentAI = self.nextAI
	    self.recordedX = self.rect.x
	    self.nextAI = self.nextNextAI # this is pretty dumb
	    self.goal = self.nextGoal
	    self.oldSpeed = 3
	else:
	    if self.rect.x < x-5:
		self.rect.x += 4
	    elif self.rect.x > x+5:
		self.rect.x -= 4
	    if self.rect.y < y-5:
		self.rect.y += 4
	    elif self.rect.y > y+5:
		self.rect.y -= 4

    def secondAI(self):

	if self.rect.x == self.recordedX and self.firing == False:
	    self.firing = True
	    if self.xMove != 0:
		self.oldSpeed = self.xMove
		self.xMove = 0

	if self.firing == True:
	    self.firing_counter += 1
	    self.spawn_bakeha_counter += 1
	    if self.spawn_bakeha_counter == 10:
		self.spawnBakehaCorners()
		self.spawn_bakeha_counter = 0
	    if self.firing_counter == self.firing_max:
		self.firing = False
		self.firing_counter = 0
		self.xMove = self.oldSpeed
		self.spawn_bakeha_counter = 9
	else:

	    if self.rect.x > 350 and self.xMove > 0:
		self.xMove = -self.xMove
	    if self.rect.x < 50 and self.xMove < 0:
		self.xMove = -self.xMove

    def spawnBakeha(self):

	monster = Bakeha(self.rect.center) # spawn a leaf
	data.spawned_monsters.append(monster)

    def spawnBakehaCorners(self):

	monster = ExplodeBakeha((0,0))
	data.spawned_monsters.append(monster)
	monster = ExplodeBakeha((data.playable_width,0))
	monster.speed = -monster.speed
	monster.angle = -monster.angle
	data.spawned_monsters.append(monster)
