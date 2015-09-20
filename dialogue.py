import pygame

import data
import objects

from helpers import * 

class TestDialogue(objects.Dialogue):

    def __init__(self):

	objects.Dialogue.__init__(self,["Inspector Hound"],[pygame.image.load("images/hound-portrait.png").convert_alpha()],"text/first-dialogue.txt")
