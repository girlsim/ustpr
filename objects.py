import pygame
import random
import math
from pygame.locals import *

import data
from helpers import *

class Dialogue:

    def __init__(self,speakers,portraits,file):

	self.speakers = speakers
	self.portraits = portraits
	f = open(file,"r")
	self.exchanges = f.readlines() # unfortunately, this leaves ugly newline characters at the end of each phrase. Need to come up with a way around that.

	self.currentSpeaker = 0
	self.currentExchange = 0

    def next(self):

	self.currentExchange += 1
	if self.currentExchange >= len(self.exchanges):
	    data.dialogue_on = False
	    self.finished()
	self.currentSpeaker += 1
	if self.currentSpeaker >= len(self.speakers):
	    self.currentSpeaker = 0

    def finished(self): # called when the dialogue ends--unused by default, but could come in handy

	pass

class powerUp(pygame.sprite.Sprite):

    def __init__(self,centerPoint,imgs,type,value):
	pygame.sprite.Sprite.__init__(self)
	self.frames = imgs
	self.frame = 0
	self.image = self.frames[self.frame]
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint

	self.type = type # "score", "power"
	self.value = value
	self.yMove = 3

    def update(self,player):

	self.frame += 1
	if self.frame <= len(self.frames):
	    self.frame = 0
	self.image = self.frames[self.frame]

	self.rect.move_ip(0,self.yMove)

	if pygame.sprite.collide_rect(self,player) and not player.dying:
	    if self.type == "score":
		data.score += self.value
	    elif self.type == "power":
		player.currentPower += self.value
	    data.PickupSoundsChannel.play(data.PowerUpSounds[0])
	    self.kill()

class Image(pygame.sprite.Sprite):

    def __init__(self,centerPoint,imgs,xMove=0,yMove=0,repeat=True):
	pygame.sprite.Sprite.__init__(self)
	self.frames = imgs
	self.frame = 0
	self.image = self.frames[self.frame]
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint

	self.xMove,self.yMove = xMove,yMove
	self.repeat = repeat

    def update(self):

	self.frame += 1
	if self.frame >= len(self.frames):
	    self.frame = 0
	    if not self.repeat:
		self.kill()
	self.image = self.frames[self.frame]

	self.rect.move_ip(self.xMove,self.yMove)

class Hitbox(pygame.sprite.Sprite):

    def __init__(self,centerPoint,image):
	pygame.sprite.Sprite.__init__(self)
	self.img_visible = image
	self.img_invisible = pygame.transform.scale(load_image('hitbox.png',-1),(self.img_visible.get_rect().w,self.img_visible.get_rect().h)) # blank image
	self.image = self.img_invisible
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint
	self.dying = False

	self.health = 1

class Player(pygame.sprite.Sprite):

    def __init__(self,centerPoint,imageList):
	pygame.sprite.Sprite.__init__(self)
	self.image = imageList[0]
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint

	self.xMove,self.yMove = 0,0

	self.slow = False
	self.firing = False
	self.currentPower = 0.0
	self.maxPower = 5
	self.currentCharges = 2
	self.currentLives = 2

	self.currentFrame = 0

	self.hitbox = Hitbox(self.rect.center,self.hitbox_image)

	self.dying = False
	self.dead = False

    def update(self, enemy_bullets):

	if not self.dying: # Normal stuff -- cycle through frames, update movement
	    self.image = self.imageList[self.currentFrame]
	    self.currentFrame += 1
	    if self.currentFrame == len(self.imageList):
		self.currentFrame = 0
	    if not self.slow:
		self.rect.move_ip(self.xMove,self.yMove)
		x,y = self.rect.center
		if y > data.playable_height or y < 0:
		    self.rect.y -= self.yMove
		if x > data.playable_width or x < 0:
		    self.rect.x -= self.xMove
	    else:
		self.rect.move_ip(self.xMove/2,self.yMove/2)
		x,y = self.rect.center
		if y > data.playable_height or y < 0:
		    self.rect.y -= self.yMove/2
		if x > data.playable_width or x < 0:
		    self.rect.x -= self.xMove/2

	    for bullet in enemy_bullets:
		if self.rect.colliderect(bullet.rect) and not bullet.grazed and data.game_on:
		    data.graze += 1
		    bullet.grazed = True
		    x,y = bullet.rect.center
		    px,py = self.rect.center
		    xMove,yMove = 0,0
		    if x > px:
			xMove = random.randint(-6,-4)
		    else:
			xMove = random.randint(4,6)
		    if y > py:
			yMove = random.randint(-1,0)
		    else:
			yMove = random.randint(0,1)
		    data.spawned_anims.append(Image(bullet.rect.center,[load_image('sparkle-1.png',-1),load_image('sparkle-2.png',-1),load_image('sparkle-3.png',-1),load_image('sparkle-4.png',-1)],xMove,yMove,False))

	    if self.slow: # hitbox image
		self.hitbox.image = self.hitbox.img_visible
	    else:
		self.hitbox.image = self.hitbox.img_invisible

	    if self.currentPower > self.maxPower:
		self.currentPower = self.maxPower

	    self.hitbox.rect.center = self.rect.center
	    if self.hitbox.dying: # Did the hitbox get hit? If so, reset all values for respawn
		self.dying = True
		self.firing = False
		self.slow = False
		self.currentFrame = 0
		self.hitbox.kill()
	else: # Cycle through death frames
	    self.image = self.deathImageList[self.currentFrame]
	    self.currentFrame += 1
	    if self.currentFrame == len(self.deathImageList):
		self.dead = True
		self.currentFrame = 0

    def commandKeyDown(self, key):
	if (key == data.keys[2]):
	    self.xMove += self.x_dist
	elif (key == data.keys[0]):
	    self.xMove += -self.x_dist
	elif (key == data.keys[1]):
	    self.yMove += -self.y_dist
	elif (key == data.keys[3]):
	    self.yMove += self.y_dist
	elif (key == data.keys[4]) and self.dead == False and self.dying == False:
	    if not data.dialogue_on:
		self.firing = True
	    else:
		data.current_dialogue.next()
	elif (key == data.keys[5]) and self.dead == False and self.dying == False:
	    self.slow = True

    def commandKeyUp(self, key):

	if (key == data.keys[2]):
		self.xMove += -self.x_dist
	elif (key == data.keys[0]):
		self.xMove += self.x_dist
	elif (key == data.keys[1]):
		self.yMove += self.y_dist
	elif (key == data.keys[3]):
		self.yMove += -self.y_dist
	elif (key == data.keys[4]):
	    self.firing = False
	elif (key == data.keys[5]):
	    self.slow = False


class Monster(pygame.sprite.Sprite):

    def __init__(self,centerPoint,imageList):

	pygame.sprite.Sprite.__init__(self)
	self.image = imageList[0]
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint

	self.health = 0
	self.speed = 0
	self.currentAI = None

	self.dying = False
	self.currentFrame = 0

	self.drops = [] #[[image,type,value]]

    def update(self):

	if self.dying == False:

	    self.image = self.imageList[self.currentFrame]
	    self.currentFrame += 1
	    if self.currentFrame == len(self.imageList):
		self.currentFrame = 0
	    self.rect.move_ip(self.xMove,self.yMove)

	    if self.rect.y > data.playable_height + 50 or self.rect.y < -50 or self.rect.x > data.playable_width + 50 or self.rect.x < -50:
		self.kill()

	else:

	    self.image = self.deathImageList[self.currentFrame]
	    self.currentFrame += 1
	    if self.currentFrame == len(self.deathImageList):
		self.kill()
		for drop in self.drops:
		    x,y = self.rect.center
		    data.power_ups.append(powerUp((x+random.randint(-10,10),y+random.randint(-10,10)),drop[0],drop[1],drop[2]))

class Bullet(pygame.sprite.Sprite):

    def __init__(self,centerPoint,imageList):

	pygame.sprite.Sprite.__init__(self)
	self.image = imageList[0]
	self.rect = self.image.get_rect()
	self.rect.center = centerPoint

	self.currentFrame = 0

	self.dying = False
	self.grazed = False # bullets can only be grazed once!

	self.xMove,self.yMove = 0,0
	self.xRemainder,self.yRemainder = 0,0

    def update(self,enemyGroup):

	if self.dying == True:

	    self.image = self.deathImageList[self.currentFrame]
	    self.currentFrame += 1
	    if self.currentFrame == len(self.deathImageList):
		self.kill()

	else:

	    if self.rect.y > data.playable_height + 50 or self.rect.y < -50 or self.rect.x > data.playable_width + 50 or self.rect.x < -50:

		self.kill()

	    self.image = self.imageList[self.currentFrame]
	    self.currentFrame += 1
	    if self.currentFrame == len(self.imageList):
		self.currentFrame = 0
	    self.rect.move_ip(self.xMove,self.yMove)

	    for enemy in enemyGroup:
		if self.rect.colliderect(enemy.rect) and not enemy.dying and data.game_on:
		    data.HitSoundsChannel.play(data.FireSounds[0]) # play bullet hit sound
		    enemy.health -= self.damage
		    data.score += self.damage - 1 # -1 is so that enemy bullets don't give score
		    if enemy.health < 1:
			enemy.dying = True
		    self.dying = True
		    self.currentFrame = 0

    def angleMove(self):

	rotation = (math.pi / 180.) * self.angle
	self.xMove = math.cos(rotation) * self.speed
	self.yMove = math.sin(rotation) * self.speed

	self.xRemainder += self.xMove % 1 # messy, but the only way I've come across so far
	self.yRemainder += self.yMove % 1

	if self.xRemainder > 1:
	    self.xRemainder -= 1
	    self.xMove += 1
	elif self.xRemainder < -1:
	    self.xRemainder += 1
	    self.xMove -= 1
	if self.yRemainder > 1:
	    self.yRemainder -= 1
	    self.yMove += 1
	elif self.yRemainder < -1:
	    self.yRemainder += 1
	    self.yMove -= 1
