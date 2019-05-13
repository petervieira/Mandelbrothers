# main variables for game state

WIDTH = 1024 #768
HEIGHT = 768 #576
FPS = 60
TITLE = "Mandelbrothers"
BACKGROUND_COLOR = (0,0,0)
TILESIZE = 64
GRID_W = WIDTH / TILESIZE
GRID_H = HEIGHT / TILESIZE

PLAYER_SPEED = 250
PROJECTILE_SPEED = 800
PROJECTILE_LIFETIME = 600
PROJECTILE_RATE = 500
PROJECTILE_DAMAGE = 50
ENEMY_COOLDOWN = 1000
MOB_RADIUS = 50
SLOW_COOLDOWN = 3000

TEXTBOX_DELAY = 750

STATUS = {"money": 0, "health": 100, "fullHealth": 100, "overVisit": 1, "shopVisit": 0}
SHOP = {"shop": False, 'icebow': False, 'triplebow': False, 'damage': False, 'shoot': False, 'armor': False, 'health': False, 'end-game': False}

ITEMS = {
    'icebow': {'cost': 50, 'desc': ['Ice Bow: an ancient bow found', 'in the glaciers of Greenland']},
    'triplebow': {'cost': 100, 'desc': ['Triple Bow: a bow capable of', 'firing three arrows at once']},
    'shoot': {'cost': 30, 'desc': ['Shoot speed upgrade: makes you', 'fire at a higher rate']},
    'damage': {'cost': 40, 'desc': ['Damage upgrade: makes your', 'arrows deal more damage']},
    'armor': {'cost': 50, 'desc': ['Armor upgrade: makes you more', 'impervious to enemy damage']},
    'health': {'cost': 20, 'desc': ['Health pack: restores your', 'health fully']},
    'end-game': {'cost': 1000, 'desc': ['Release your brother from', 'the ice, winning the game']}
}
