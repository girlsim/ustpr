import pygame

import data
import monsters
import dialogue

class LevelOne:

    def __init__(self):

	self.bgm = None
	self.background = None
	self.monsterSpawnList = [
	    [15,(0,100),monsters.Bakeha],
	    [25,(0,100),monsters.Bakeha],
	    [35,(0,100),monsters.Bakeha],
	    [45,(0,100),monsters.Bakeha],
	    [65,(data.playable_width,150),monsters.Bakeha],
	    [75,(data.playable_width,150),monsters.Bakeha],
	    [85,(data.playable_width,150),monsters.Bakeha],
	    [95,(data.playable_width,150),monsters.Bakeha],
	    [150,(182,0),monsters.Faerie]
	    ]
