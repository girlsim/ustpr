import pygame
from pygame.locals import *

import data
import objects
import projectiles
from helpers import *

class Hound(objects.Player):

    def __init__(self,centerPoint):

	img = load_image('hound.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]

	self.hitbox_image = load_image('hitbox-ormrinn.png',-1)
	objects.Player.__init__(self,centerPoint,self.imageList)

	self.x_dist,self.y_dist = 5,5

	# firing variables!
	self.bullet_fire = True
	self.missile_counter = 20

    def update(self,bullets):

	objects.Player.update(self,bullets)

    def fire(self):

	x,y = self.rect.center
	if self.currentPower < 1:
	    self.fire_bullet(self.rect.center)
	elif self.currentPower < 2:
	    self.fire_bullet((x-15,y))
	    self.fire_bullet((x+15,y))
	elif self.currentPower < 3:
	    self.fire_bullet((x-15,y))
	    self.fire_bullet((x+15,y))
	    self.fire_missile(self.rect.center)
	elif self.currentPower < 4:
	    self.fire_bullet((x-15,y))
	    self.fire_bullet((x+15,y))
	    self.fire_missile((x-10,y))
	    self.fire_missile((x+10,y))
	else:
	    self.fire_bullet((x-15,y))
	    self.fire_bullet((x+15,y))
	    self.fire_bullet((x,y-15))
	    self.fire_missile((x-10,y))
	    self.fire_missile((x+10,y))
	    self.fire_missile((x,y+10))

	if self.missile_counter == 20:
	    self.missile_counter = 0
	else:
	    self.missile_counter += 1
	self.bullet_fire = not self.bullet_fire

    def fire_bullet(self,centerPoint):

	if self.bullet_fire:
	    bullet = projectiles.MagicBullet(centerPoint)
	    data.player_bullets.append(bullet)

    def fire_missile(self,centerPoint):
	if self.missile_counter == 20:
	    missile = projectiles.MagicMissile(centerPoint)
	    data.player_bullets.append(missile)

class Ormrinn(objects.Player):

    def __init__(self,centerPoint):

	img = load_image('ormrinn.png',-1)
	self.imageList = [img]
	self.deathImageList = [img]

	self.hitbox_image = load_image('hitbox-ormrinn.png',-1)
	objects.Player.__init__(self,centerPoint,self.imageList)

	self.x_dist,self.y_dist = 5,5

    def update(self):

	objects.Player.update(self)

    def fire(self):

	if self.currentPower < 4:
	    bullet = projectiles.OrmrinnDagger(self.rect.center)
	    data.player_bullets.append(bullet)
	elif self.currentPower < 6:
	    bullet = projectiles.OrmrinnDagger(self.rect.center)
	    data.player_bullets.append(bullet)
	elif self.currentPower < 9:
	    bullet = projectiles.OrmrinnDagger(self.rect.center)
	    data.player_bullets.append(bullet)
	elif self.currentPower == 10:
	    bullet = projectiles.OrmrinnDagger(self.rect.center)
	    data.player_bullets.append(bullet)
