import pygame as pg
import random
import math
from random import randint
from settings import *
from os import path
from mapp import *
from text import *

vector = pg.math.Vector2

def collision(sprite, group, direction):
    # also positions the character to press against the wall and remove any space
    if direction == 'x':
        collide = pg.sprite.spritecollide(sprite, group, False)
        if collide:
            if sprite.vel.x > 0:
                sprite.pos.x = collide[0].rect.left - sprite.rect.width
            if sprite.vel.x < 0:
                sprite.pos.x = collide[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
    if direction == 'y':
        collide = pg.sprite.spritecollide(sprite, group, False)
        if collide:
            if sprite.vel.y > 0:
                sprite.pos.y = collide[0].rect.top - sprite.rect.height
            if sprite.vel.y < 0:
                sprite.pos.y = collide[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__ (self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.sprites['back']
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.vel = vector(0,0)
        self.pos = vector(x,y)
        self.last_shot = 0
        self.health = STATUS['health']
        self.fullHealth = STATUS['fullHealth']
        self.money = STATUS['money']
        self.walkcount = 0
        self.left = False
        self.right = False
        self.down = False
        self.up = False
        self.walkRight = [game.sprites['side2_walk2'], game.sprites['side2_walk']]
        self.walkLeft = [game.sprites['side_walk2'], game.sprites['side_walk']]
        self.walkUp = [game.sprites['walk2'], game.sprites['walk']]
        self.walkDown = [game.sprites['front_walk2'], game.sprites['front_walk']]


    def getKeys(self):
        self.vel = vector(0,0)
        keys = pg.key.get_pressed()
        if not self.game.interact:
            if keys[pg.K_a] or keys[pg.K_LEFT]:
                self.image = self.walkLeft[self.walkcount//12]
                if keys[pg.K_LSHIFT]:
                    self.vel.x = -PLAYER_SPEED * 1.5
                    self.walkcount += 2
                else:
                    self.vel.x = -PLAYER_SPEED
                    self.walkcount += 1
                self.left = True
                self.right = False
                self.down = False
                self.up = False
            elif keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.image = self.walkRight[self.walkcount//12]
                if keys[pg.K_LSHIFT]:
                    self.vel.x = PLAYER_SPEED * 1.5
                    self.walkcount += 2
                else:
                    self.vel.x = PLAYER_SPEED
                    self.walkcount += 1
                self.left = False
                self.right = True
                self.down = False
                self.up = False
            elif keys[pg.K_s] or keys[pg.K_DOWN]:
                self.image = self.walkDown[self.walkcount//12]
                if keys[pg.K_LSHIFT]:
                    self.vel.y = PLAYER_SPEED * 1.5
                    self.walkcount += 2
                else:
                    self.vel.y = PLAYER_SPEED
                    self.walkcount += 1
                self.left = False
                self.right = False
                self.down = True
                self.up = False
            elif keys[pg.K_w] or keys[pg.K_UP]:
                self.image = self.walkUp[self.walkcount//12]
                if keys[pg.K_LSHIFT]:
                    self.vel.y = -PLAYER_SPEED * 1.5
                    self.walkcount += 2
                else:
                    self.vel.y = -PLAYER_SPEED
                    self.walkcount += 1
                self.left = False
                self.right = False
                self.down = False
                self.up = True
            else:
                if self.left:
                    self.image = self.game.sprites['side']
                elif self.right:
                    self.image = self.game.sprites['side2']
                elif self.down:
                    self.image = self.game.sprites['front']
                elif self.up:
                    self.image = self.game.sprites['back']

            # check attacks
            if (keys[pg.K_z] or keys[pg.K_SPACE]) and not keys[pg.K_LSHIFT]:
                type = 'arrow'
                if SHOP['shoot']:
                    rate = PROJECTILE_RATE / 1.5
                else:
                    rate = PROJECTILE_RATE
                if self.last_shot > rate:
                    self.last_shot = 0
                    dir = vector(0,0)
                    dir2 = vector(0,0)
                    dir3 = vector(0,0)
                    pos = vector(self.pos)
                    dir2pos = vector(self.pos) # the arrow shooting left needs an extra offset due to the position calculation using the corner of the sprite
                    if self.left:
                        dir = vector(-1,0)
                        dir2 = vector(-1,-.3)
                        dir3 = vector(-1,.3)
                        pos += (-15,20)
                        dir2pos += (-14,3)
                    elif self.right:
                        dir = vector(1,0)
                        dir2 = vector(1,-.3)
                        dir3 = vector(1,.3)
                        pos += (10,30)
                        dir2pos += (10,10)
                    elif self.down:
                        dir = vector(0,1)
                        dir2 = vector(-.3,1)
                        dir3 = vector(.3,1)
                        pos += (16,15)
                        dir2pos += (3,15)
                    else:
                        dir = vector(0,-1)
                        dir2 = vector(-.3,-1)
                        dir3 = vector(.3,-1)
                        pos += (17,-10)
                        dir2pos += (3,-10)
                    Projectile(self.game, pos, dir, type)
                    if SHOP['triplebow']:
                        Projectile(self.game, dir2pos, dir2, type)
                        Projectile(self.game, pos, dir3, type)
                    self.game.sounds['shoot'].play()
                    self.game.sounds['shoot'].set_volume(.25)
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= .7071

    def update(self):
        if self.walkcount >= 24:
            self.walkcount = 0
        self.getKeys()
        self.pos.x += self.vel.x * self.game.dt
        self.pos.y += self.vel.y * self.game.dt
        self.rect.x = self.pos.x
        collision(self, self.game.boundaries,'x')
        self.rect.y = self.pos.y
        collision(self, self.game.boundaries,'y')
        self.last_shot += self.game.dt * 1000

class Obstacle (pg.sprite.Sprite):
    def __init__ (self, game, x, y, w, h):
        self.groups = game.boundaries
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x,y,w,h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y

class Mob(pg.sprite.Sprite):
    def __init__ (self, game, x, y, type):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        if type == 'E':
            self.image = game.sprites['electric_snake']
            self.health = 100
            self.fullHealth = 100
            self.damage = 30
            self.speed = 100
            self.maxSpeed = 100
            self.coins = 1
            self.ghost = False
        elif type == 'R':
            self.image = game.sprites['reaper']
            self.health = 150
            self.fullHealth = 150
            self.damage = 50
            self.speed = 150
            self.maxSpeed = 150
            self.coins = 2
            self.ghost = True
        elif type == 'S':
            self.image = game.sprites['snail']
            self.health = 50
            self.fullHealth = 50
            self.damage = 5
            self.speed = 10
            self.maxSpeed = 10
            self.coins = 0
            self.ghost = False
        elif type == 'F':
            self.image = game.sprites['flame']
            self.health = 175
            self.fullHealth = 175
            self.damage = 60
            self.speed = 50
            self.maxSpeed = 50
            self.coins = 3
            self.ghost = False
        elif type == 'G':
            self.image = game.sprites['golem']
            self.health = 500
            self.fullHealth = 500
            self.damage = 100
            self.speed = 100
            self.maxSpeed = 100
            self.coins = 10
            self.ghost = False
        elif type == 'L':
            self.image = game.sprites['lantern']
            self.health = 250
            self.fullHealth = 250
            self.damage = 70
            self.speed = 250
            self.maxSpeed = 250
            self.coins = 15
            self.ghost = True
        elif type == 'B':
            self.image = game.sprites['bear']
            self.health = 300
            self.fullHealth = 300
            self.damage = 80
            self.speed = 150
            self.maxSpeed = 150
            self.coins = 8
            self.ghost = False
        elif type == 'O':
            self.image = game.sprites['octodaddypog']
            self.health = 50000
            self.fullHealth = 50000
            self.damage = 200
            self.speed = 0
            self.maxSpeed = 0
            self.coins = 1000
            self.ghost = False

        self.default_image = self.image
        self.rect = self.image.get_rect()
        self.pos = vector(x,y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.vec = 0
        self.vel = vector(0,0)
        self.acc = vector(0,0)
        self.last_attack = 0
        self.slowtime = 0
        self.last_hit = 0
        self.throwtime = 0
        self.damaged = 0

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < MOB_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        self.vec = (self.game.player.pos - self.pos).angle_to(vector(1,0))
        self.last_hit += self.game.dt * 1000

        # rotate enemy based on position relative to player
        if self.type != 'O':
            if self.vec > -90 and self.vec < 90:
                self.image = pg.transform.flip(self.default_image, True, False)
            elif self.vec < -90 or self.vec > 90:
                self.image = pg.transform.flip(self.default_image, False, False)
        else:
            time = pg.time.get_ticks()
            if time - self.damaged > 300:
                self.damaged = time
                self.image = self.game.sprites['octodaddypog']

        self.rect = self.image.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if abs(self.game.player.pos.x - self.pos.x) + abs(self.game.player.pos.y - self.pos.y) < 700:
            self.acc = vector(1, 0).rotate(-self.vec)
            self.avoid_mobs()
            time = pg.time.get_ticks()
            self.acc.scale_to_length(self.maxSpeed)
            if time - self.slowtime <= SLOW_COOLDOWN:
                if self.type != 'B' and self.type != 'G':
                    self.vel = vector(0,0)
            if self.type != 'R' and self.type != 'L':
                self.acc += self.vel * -1
            else:
                self.acc += self.vel * -.5
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + .5 * self.acc * self.game.dt ** 2
            self.rect.x = self.pos.x
            if not self.ghost:
                collision(self, self.game.boundaries, 'x')
            self.rect.y = self.pos.y
            if not self.ghost:
                collision(self, self.game.boundaries, 'y')
            if self.type == 'G':
                time = pg.time.get_ticks()
                if time - self.throwtime > 2000:
                    self.throwtime = time
                    Projectile(self.game, self.pos + (53,80), vector(1,0).rotate(-(self.game.player.pos - self.pos).angle_to(vector(1,0))), 'icyrock')
        if self.health <= 0:
            # spawn coins around the enemy
            for i in range(0, self.coins):
                Coin(self.game, (self.rect.center[0] + randint(-20, 20), self.rect.center[1] + randint(-20, 20)))
            self.kill()

    def drawHealth(self):
        if self.health > .6 * self.fullHealth:
            color = (0, 255, 0)
        elif self.health > .3 * self.fullHealth:
            color = (255,255,0)
        else:
            color = (255,0,0)
        width = int(self.rect.width * self.health/self.fullHealth)
        self.health_bar = pg.Rect(0,0,width,7)
        if self.health < self.fullHealth:
            pg.draw.rect(self.image, color, self.health_bar)

class NPC(pg.sprite.Sprite):
    def __init__ (self, game, x, y, type):
        self.groups = game.all_sprites, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        if type == 'OM':
            self.image = game.sprites['oldman']
        self.rect = self.image.get_rect()
        self.pos = vector(x,y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.vec = 0
        self.textboxes = [
            Textbox("Egads! You have broken my floor!", self.game, self.image),
            Textbox("...", self.game, self.image),
            Textbox("Huh? You... You are not from Mandelbrot...", self.game, self.image),
            Textbox("You whippersnappers always trespass into forbidden lands.", self.game, self.image),
            Textbox("It is not safe here. Not anymore...", self.game, self.image),
            Textbox("The overworld is infested with ravenous creatures these days.", self.game, self.image),
            Textbox("It is foolish to wander around in this corrupted nation", self.game, self.image),
            Textbox("...though I suppose you may use my shop if you wish", self.game, self.image),
            Textbox("...", self.game, self.image),
            Textbox("Good luck, kid", self.game, self.image)
        ]

    def update(self):
        self.vec = (self.game.player.pos - self.pos).angle_to(vector(1,0))
        self.distance = abs(self.game.player.pos.x - self.pos.x) + abs(self.game.player.pos.y - self.pos.y)
        if self.type == 'OM':
            if SHOP['boss'] == False:
                if SHOP["shop"] == False:
                    self.game.interact = True
                    SHOP["shop"] = True
                    self.game.textboxes = self.textboxes
            else:
                if SHOP["spoke"] == False:
                    self.game.interact = True
                    SHOP["spoke"] = True
                    self.game.textboxes = [
                        Textbox("It appears we have found the cause of this ruckus.", self.game, self.image),
                        Textbox("Octodaddy has been causing tremors with his tentacles", self.game, self.image),
                        Textbox("and has disturbed the tranquility of Mandelbrot.", self.game, self.image),
                        Textbox("The future of this nation lies in your hands.", self.game, self.image)
                    ]
            if self.distance < 150:
                # rotate npc based on position relative to player
                if self.vec > -45 and self.vec < 45:
                    self.image = self.game.sprites['oldman_right']
                elif self.vec > 45 and self.vec < 135:
                    self.image = self.game.sprites['oldman_back']
                elif self.vec > 135 or self.vec < -135:
                    self.image = self.game.sprites['oldman_left']
                elif self.vec < -45 and self.vec > -135:
                    self.image = self.game.sprites['oldman']
            if pg.key.get_pressed()[pg.K_z] and not self.game.interact and self.rect.colliderect(self.game.player.rect):
                self.game.interact = True
                if SHOP['boss'] == False:
                    randint = random.randint(1,10)
                    if randint == 1:
                        self.game.textboxes = [Textbox("How was the weather up there?", self.game, self.image)]
                    elif randint > 1 and randint < 5:
                        self.game.textboxes = [Textbox("It's a bit chilly down here...", self.game, self.image)]
                    else:
                        self.game.textboxes = [Textbox("Buy anything you like!", self.game, self.image)]
                else:
                    self.game.textboxes = [Textbox("Octodaddy relies heavily on his sight!", self.game, self.image)]

class Projectile(pg.sprite.Sprite):
    def __init__ (self, game, pos, dir, type):
        self.groups = game.all_sprites, game.projectiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        if type == 'arrow':
            if SHOP['icebow']:
                self.image = game.sprites['icearrow']
            else:
                self.image = game.sprites['arrow']
            self.image = pg.transform.rotate(self.image, -90)
            self.image = pg.transform.rotate(self.image, math.atan2(dir.y * -1,dir.x)*180/math.pi) # formula to angle arrows properly
        elif type == 'icyrock':
            self.image = game.sprites['icyrock']
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.x = pos.x
        self.rect.y = pos.y
        if type == 'arrow':
            self.vel = dir * PROJECTILE_SPEED
        elif type == 'icyrock':
            self.vel = dir * PROJECTILE_SPEED / 3
        self.lifetime = 0

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.lifetime += self.game.dt * 1000
        if pg.sprite.spritecollideany(self, self.game.boundaries):
            self.kill()
        if self.type == 'arrow':
            if self.lifetime > PROJECTILE_LIFETIME:
                self.kill()
        elif self.type == 'icyrock':
            if self.lifetime > PROJECTILE_LIFETIME * 3:
                self.kill()

class Coin(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.game = game
        self.image = game.sprites['coin1']
        self.frames = [1, 2, 3, 4, 5, 4, 3, 2]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.time = random.randint(0, 79)

    def update(self):
        self.time = (self.time + 1) % 80
        self.image = self.game.sprites['coin' + str(self.frames[math.floor(self.time / 10)])]

        if pg.sprite.collide_rect(self, self.game.player):
            self.game.player.money += 1
            STATUS['money'] += 1
            self.game.sounds['coin'].play()
            self.kill()

class WarpZone(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        self.groups = game.all_sprites, game.warps
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.image = game.sprites['warp']
        self.rect = self.image.get_rect()
        self.pos = vector(x,y)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            if self.type == 'shop':
                pg.mixer.music.load(path.join(self.game.gameFolder, 'music/intro.wav'))
                pg.mixer.music.set_volume(.3)
                self.game.map = TiledMap(path.join(self.game.gameFolder, 'maps/shop.tmx'))
            if self.type == 'overworld':
                pg.mixer.music.load(path.join(self.game.gameFolder, 'music/theme2.wav'))
                pg.mixer.music.set_volume(.5)
                self.game.map = TiledMap(path.join(self.game.gameFolder, 'maps/overworld' + str(STATUS['overVisit']) + '.tmx'))
                self.game.wave += 1
                if STATUS['overVisit'] < 8:
                    STATUS['overVisit'] += 1
                    self.game.alpha += 22
                    self.game.temp.fill((0,0,0))
                    self.game.temp.set_alpha(self.game.alpha)
            pg.mixer.music.play(-1, 0.0)
            self.game.map_img = self.game.map.make_map()
            self.game.map_rect = self.game.map_img.get_rect()
            self.game.minimap.update()
            self.game.newGame()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.game = game
        if type == 'icebow':
            self.image = game.sprites['icebow']
        elif type == 'health':
            self.image = game.sprites['health']
        elif type == 'armor':
            self.image = game.sprites['shield']
        elif type == 'triplebow':
            self.image = game.sprites['triplearrow']
        elif type == 'end-game':
            self.image = game.sprites['end-game']
        elif type == 'shoot':
            self.image = game.sprites['speed']
        elif type == 'damage':
            self.image = game.sprites['damage']
        elif type == 'pierce':
            self.image = game.sprites['pierce']
        self.rect = pg.Rect(pos[0], pos[1], self.image.get_rect().width, self.image.get_rect().height)
        self.cost = ITEMS[type]['cost']
        self.desc = ITEMS[type]['desc']
        self.type = type

    def update(self):
        if self.rect.colliderect(self.game.player.rect) and pg.key.get_pressed()[pg.K_b] and not SHOP[self.type] and self.game.player.money >= self.cost:
            self.game.sounds['coin'].play()
            self.game.player.money -= self.cost
            STATUS['money'] -= self.cost
            if self.type == 'health':
                self.game.player.health = self.game.player.fullHealth
                STATUS['health'] = self.game.player.fullHealth
                SHOP[self.type] = True
            elif self.type == 'end-game':
                self.game.interact = True
                self.game.textboxIndex = 0
                self.game.textboxDelay = 0
                self.game.textboxes = [Textbox("Brother, you've freed me from the ice!", self.game, self.game.sprites['brother']),
                                       Textbox("The citizens of Mandelbrot will forever be grateful.", self.game, self.game.sprites['brother'])]
                self.game.win = True
            elif self.type == 'armor':
                self.game.player.fullHealth = 200
                STATUS['fullHealth'] = 200
                SHOP[self.type] = True
                self.kill()
            elif self.type in ['icebow', 'shoot', 'damage', 'triplebow', 'pierce']:
                SHOP[self.type] = True
                self.kill()
            else:
                SHOP[self.type] = True

    def draw_textbox(self):
        rect = pg.Rect(0, 0, 256, 128)
        rect.center = (self.rect.x + self.rect.width / 2, self.rect.y - 100)
        rect = rect.move(self.game.camera.camera.topleft)

        color = (128, 255, 128) if self.game.player.money >= self.cost else (255, 128, 128)

        pg.draw.rect(self.game.screen, color, pg.Rect((rect.x - 2, rect.y - 2), (rect.width + 4, rect.height + 4)))
        pg.draw.rect(self.game.screen, (0, 0, 0), rect)

        font = pg.font.Font(pg.font.match_font('Consolas'), 14)
        surface = font.render(self.desc[0], True, color)
        self.game.screen.blit(surface, (rect.x + 8, rect.y + 8))
        surface = font.render(self.desc[1], True, color)
        self.game.screen.blit(surface, (rect.x + 8, rect.y + 24))

        surface = font.render(f'Press B to buy ({self.cost} coins)', True, color)
        self.game.screen.blit(surface, (rect.x + 8, rect.y + rect.height - 16))
