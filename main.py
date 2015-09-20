import os,sys
import pygame
import re
from pygame.locals import *

import data
import characters
import monsters
import levels
import objects
import menus

from helpers import *

class UStPR:

    def __init__(self):
	
	print ("Initializing Pygame...")
	pygame.init()

	data.screen = pygame.display.set_mode((data.screen_width,data.screen_height))

	data.player_choice = characters.Hound
	data.player = data.player_choice((250,550))
	self.player_group = pygame.sprite.RenderPlain((data.player))
	self.player_hitbox = pygame.sprite.RenderPlain((data.player.hitbox))
	self.player_bullet_group = pygame.sprite.Group()
	self.monster_bullet_group = pygame.sprite.Group()
	self.enemy_group = pygame.sprite.Group()
	self.anims_group = pygame.sprite.Group()
	self.power_ups_group = pygame.sprite.Group()
	statsbar = objects.Image((500,325),[load_image("stats-bar.png")])
	self.anims_group.add(statsbar)

	self.current_level = levels.LevelOne()

	data.current_menu = menus.StartMenu()

	pygame.mixer.init()

	data.HitSoundsChannel = pygame.mixer.Channel(1) # not sure how many channels I want and what they should be for, so...
	data.PickupSoundsChannel = pygame.mixer.Channel(2)

	data.HitSoundsChannel.set_volume(0.3)
	data.PickupSoundsChannel.set_volume(0.5)

	data.FireSounds = [pygame.mixer.Sound("sounds/hit.wav"),pygame.mixer.Sound("sounds/enemy-fire.wav")] # bullet hit, enemy shoot
	data.PowerUpSounds = [pygame.mixer.Sound("sounds/pickup.wav"),pygame.mixer.Sound("sounds/powerup.wav")] # pickup sound, (unused) power up sound

    def menuLoop(self):

	while data.menu_on == True:

	    pygame.time.wait(data.ms_per_refresh)

	    pygame.event.pump()
	    for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    sys.exit()
		elif event.type == KEYDOWN:
		    if event.key == data.keys[4]:
			data.current_menu.functions[data.current_choice]()
			data.current_choice = 0
			data.HitSoundsChannel.play(pygame.mixer.Sound("sounds/menu-select.wav"))
		    elif event.key == data.keys[1]:
			data.current_choice -= 1
			if data.current_choice < 0:
			    data.current_choice = len(data.current_menu.choices)-1
			data.HitSoundsChannel.play(pygame.mixer.Sound("sounds/menu-blip.wav"))
		    elif event.key == data.keys[3]:
			data.current_choice += 1
			if data.current_choice >= len(data.current_menu.choices):
			    data.current_choice = 0
			data.HitSoundsChannel.play(pygame.mixer.Sound("sounds/menu-blip.wav"))

	    pygame.display.flip()
	    data.screen.fill((10,25,25))

	    if pygame.font:
		x = 150
		y = 150
		for choice in data.current_menu.choices:
		    font = pygame.font.Font(None, 30)
		    text = font.render(choice, 1, (55, 105, 110))
		    textpos = x,y
		    data.screen.blit(text, textpos)
		    y += 36
	    data.screen.blit(load_image("pointer.png",-1),(114,140+36*data.current_choice))

	self.gameLoop()

    def gameLoop(self):

	while data.game_on == True:

	    pygame.time.wait(data.ms_per_refresh)
	    for spawn in self.current_level.monsterSpawnList:
		if spawn[0] == data.rounds_passed and not data.dialogue_on: # no spawning monsters with dialogue going! Otherwise the dummy will spawn every refresh
		    monster = spawn[2](spawn[1])
		    self.enemy_group.add(monster)
	    if not data.dialogue_on:
		data.rounds_passed += 1 # this makes it so monsters and things don't spawn while the menu is going

	    pygame.event.pump()
	    for event in pygame.event.get():
		if event.type == pygame.QUIT:
		    sys.exit()
		elif event.type == KEYDOWN:
		    for key in data.keys:
			if event.key == key:
			    data.player.commandKeyDown(event.key)
		elif event.type == KEYUP:
		    for key in data.keys:
			if event.key == key:
			    data.player.commandKeyUp(event.key)

	    data.stored_xMove,data.stored_yMove = data.player.xMove,data.player.yMove
	    data.stored_power = data.player.currentPower

	    self.monster_bullet_group.update(self.player_hitbox)
	    self.enemy_group.update()
	    self.player_bullet_group.update(self.enemy_group)
	    self.anims_group.update()
	    self.power_ups_group.update(data.player)
	    self.player_group.update(self.monster_bullet_group)
	    if data.player.firing == True:
		data.player.fire()
		for bullet in data.player_bullets:
		    self.player_bullet_group.add(bullet)
		data.player_bullets = []
	    for bullet in data.monster_bullets:
		self.monster_bullet_group.add(bullet)
	    data.monster_bullets = []
	    for monster in data.spawned_monsters:
		self.enemy_group.add(monster)
	    data.spawned_monsters = []
	    for anim in data.spawned_anims:
		self.anims_group.add(anim)
	    data.spawned_anims = []
	    for power_up in data.power_ups:
		self.power_ups_group.add(power_up)
	    data.power_ups = []
					

	    pygame.display.flip()
	    data.screen.fill((10,25,25))
	    self.player_bullet_group.draw(data.screen)
	    self.player_group.draw(data.screen)
	    self.player_hitbox.draw(data.screen)
	    self.enemy_group.draw(data.screen)
	    self.monster_bullet_group.draw(data.screen)
	    self.anims_group.draw(data.screen)
	    self.power_ups_group.draw(data.screen)

	    if data.display_score < data.score: # increment display score so we can watch the numbers zip up and down
		data.display_score += 1
	    if data.display_power < data.player.currentPower - .01:
		data.display_power += .01
	    elif data.display_power > data.player.currentPower + .01:
		data.display_power -= .01
	    if data.display_graze < data.graze:
		data.display_graze += 1

	    if pygame.font:
		font = pygame.font.Font(None, 24)

		counter = 0
		while counter < 9: # draw life boxes + lives
		    data.screen.blit(load_image("life-empty.png",-1),(410+20*counter,20))
		    counter += 1
		counter = 0
		while counter < data.lives_remaining:
		    data.screen.blit(load_image("life.png",-1),(410+20*counter,20))
		    counter += 1

		text = font.render("Score: %s" % data.display_score
			       , 1, (55, 105, 110))
		textpos = 410,50
		data.screen.blit(text, textpos)

		if data.display_power < 5:
		    text = font.render("Power: %s" % data.display_power
				       , 1, (55, 105, 110))
		else:
		    text = font.render("Power: MAX", 1, (55, 105, 110))
		textpos = 410,80
		data.screen.blit(text, textpos)

		text = font.render("Graze: %s" % data.display_graze
				   , 1, (55, 105, 110))
		textpos = 410,110
		data.screen.blit(text, textpos)

	    if data.dialogue_on:
		data.screen.blit(load_image("dialogue.png",-1),(0,575))

		split_text = re.split("/n",data.current_dialogue.exchanges[data.current_dialogue.currentExchange])
		for phrase in split_text:
		    re.sub("/n","",phrase)

		phrase_number = 0

		while phrase_number < len(split_text):
		    if pygame.font:
			font = pygame.font.Font(None, 12)
			text = font.render(split_text[phrase_number]
					   , 1, (55, 105, 110))
			x = 12
			y = 587 + (phrase_number * 12)
			textpos = x,y
			data.screen.blit(text, textpos)
			phrase_number += 1

		data.screen.blit(pygame.transform.flip(data.current_dialogue.portraits[data.current_dialogue.currentSpeaker],data.current_dialogue.currentSpeaker,0),(100*data.current_dialogue.currentSpeaker,175))
		font = pygame.font.Font(None, 18)
		text = font.render(data.current_dialogue.speakers[data.current_dialogue.currentSpeaker]
				   , 1, (115, 210, 220))
		textpos = 18+268*data.current_dialogue.currentSpeaker,545
		data.screen.blit(text, textpos)

	    self.playerDead()

    def playerDead(self):

	if data.player.dead == True:
	    data.player.kill()
	    if data.respawn_counter == data.respawn_time:
		data.player = data.player_choice((250,550))
		self.player_group = pygame.sprite.RenderPlain((data.player))
		self.player_hitbox = pygame.sprite.RenderPlain((data.player.hitbox))
		data.respawn_counter = 0
		data.lives_remaining -= 1
		if data.lives_remaining == -1:
		    sys.exit()
		for bullet in self.monster_bullet_group:
		    bullet.kill()
		data.player.xMove,data.player.yMove = data.stored_xMove,data.stored_yMove
		data.player.currentPower = data.stored_power / 2
	    else:
		data.respawn_counter += 1


if __name__ == "__main__":
    MainWindow = UStPR()
    MainWindow.menuLoop()
