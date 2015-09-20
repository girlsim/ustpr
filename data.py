from pygame.locals import *

screen_height = 650
screen_width = 600
playable_height = 650
playable_width = 400
screen = []

ms_per_refresh = 10
rounds_passed = 0

game_on = False
menu_on = True
dialogue_on = False

current_menu = None
current_choice = 0
current_dialogue = None

player = None
player_bullets = []
monster_bullets = []
spawned_monsters = []
spawned_anims = []
power_ups = []

keys = [K_LEFT,K_UP,K_RIGHT,K_DOWN,K_x,K_c,K_z] # Left, up, right, down, fire, slow, bomb

respawn_time = 100
respawn_counter = 0

player_choice = []
lives_remaining = 3
score = 0
display_score = 0
stored_xMove,stored_yMove = 0,0
stored_power = 0
display_power = 0
graze = 0
display_graze = 0

# sounds! These may get complicated

HitSoundsChannel = None
PickupSoundsChannel = None
FireSounds = []
PowerUpSounds = []
