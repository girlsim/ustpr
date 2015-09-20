import os,sys
import pygame

import data

class StartMenu:

    def __init__(self):

	self.choices = ["New game","Exit"]
	self.functions = [self.newGame,self.exit]

    def newGame(self):

	data.game_on = True
	data.menu_on = False

    def exit(self):

	sys.exit()
