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

STATUS = {"money": 0, "health": 100, "overVisit": 1, "shopVisit": 0}
SHOP = {"shop": False, 'icebow': True, 'triplebow': True}

ITEMS = {
    'ice-bow': {cost: 5},
    'triple': {cost: 5},
    'explosive': {cost: 5},
    'shoot': {cost: 5},
    'damage': {cost: 5},
    'armor': {cost: 5},
    'health': {cost: 5},
    'end-game': {cost: 5}
}
