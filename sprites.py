import pygame as pg
from random import randint
from settings import *
from os import path

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
		self.health = 100
		self.fullHealth = 100
		self.money = 0
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
		if keys[pg.K_SPACE] and not keys[pg.K_LSHIFT]:
			type = 'arrow'
			if self.last_shot > PROJECTILE_RATE:
				self.last_shot = 0
				dir = vector(0,0)
				pos = vector(self.pos)
				if self.left:
					dir = vector(-1,0)
					pos += (-40,10)
				elif self.right:
					dir = vector(1,0)
					pos += (40,40)
				elif self.down:
					dir = vector(0,1)
					pos += (10,40)
				else:
					dir = vector(0,-1)
					pos += (40,-10)
				Projectile(self.game, pos, dir, type)
				self.game.sounds['shoot'].play()
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
			self.coins = 1
		elif type == 'R':
			self.image = game.sprites['reaper']
			self.health = 150
			self.fullHealth = 150
			self.damage = 50
			self.speed = 200
			self.coins = 2
		elif type == 'S':
			self.image = game.sprites['snail']
			self.health = 50
			self.fullHealth = 50
			self.damage = 5
			self.speed = 10
			self.coins = 0
		elif type == 'F':
			self.image = game.sprites['flame']
			self.health = 175
			self.fullHealth = 175
			self.damage = 80
			self.speed = 50
			self.coins = 3

		self.default_image = self.image
		self.rect = self.image.get_rect()
		self.pos = vector(x,y)
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		self.vec = 0
		self.vel = vector(0,0)
		self.acc = vector(0,0)
		self.last_attack = 0

	def avoid_mobs(self):
		for mob in self.game.mobs:
			if mob != self:
				dist = self.pos - mob.pos
				if 0 < dist.length() < MOB_RADIUS:
					self.acc += dist.normalize()

	def update(self):
		self.vec = (self.game.player.pos - self.pos).angle_to(vector(1,0))

		# rotate enemy based on position relative to player
		if self.vec > -90 and self.vec < 90:
			self.image = pg.transform.flip(self.default_image, True, False)
		elif self.vec < -90 or self.vec > 90:
			self.image = pg.transform.flip(self.default_image, False, False)

		self.rect = self.image.get_rect()
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		if abs(self.game.player.pos.x - self.pos.x) + abs(self.game.player.pos.y - self.pos.y) < 500:
			self.acc = vector(1, 0).rotate(-self.vec)
			self.avoid_mobs()
			self.acc.scale_to_length(self.speed)
			self.acc += self.vel * -1
			self.vel += self.acc * self.game.dt
			self.pos += self.vel * self.game.dt + .5 * self.acc * self.game.dt ** 2
			self.rect.x = self.pos.x
			collision(self, self.game.boundaries,'x')
			self.rect.y = self.pos.y
			collision(self, self.game.boundaries,'y')
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

class Projectile(pg.sprite.Sprite):
	def __init__ (self, game, pos, dir, type):
		self.groups = game.all_sprites, game.projectiles
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		if type == 'arrow':
			self.image = game.sprites['arrow']
			if dir.y == 1:
				self.image = pg.transform.rotate(self.image, 180)
			else:
				self.image = pg.transform.rotate(self.image, -90 * dir.x)

		self.rect = self.image.get_rect()
		self.pos = vector(pos)
		self.rect.x = pos.x
		self.rect.y = pos.y
		self.vel = dir * PROJECTILE_SPEED
		self.lifetime = 0

	def update(self):
		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		self.lifetime += self.game.dt * 1000
		if pg.sprite.spritecollideany(self, self.game.boundaries):
			self.kill()
		if self.lifetime > PROJECTILE_LIFETIME:
			self.kill()

class Coin(pg.sprite.Sprite):
	def __init__(self, game, pos):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.pos = pos
		self.game = game
		self.image = game.sprites['coin']
		self.rect = self.image.get_rect()
		self.rect.center = pos

	def update(self):
		if pg.sprite.collide_rect(self, self.game.player):
			self.game.player.money += 1
			self.game.sounds['coin'].play()
			self.kill()
