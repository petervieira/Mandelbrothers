import pygame
from settings import *
from os import path

vector = pygame.math.Vector2
walkcount = 0
walkRight = [pygame.image.load('images/side2_walk2.png'), pygame.image.load('images/side2_walk.png')]
walkLeft = [pygame.image.load('images/side_walk2.png'), pygame.image.load('images/side_walk.png')]
walkUp = [pygame.image.load('images/walk2.png'), pygame.image.load('images/walk.png')]
walkDown = [pygame.image.load('images/front_walk2.png'), pygame.image.load('images/front_walk.png')]
left = False
right = False
down = False
up = False

def collision(sprite, group, direction):
	# position the character to press against the wall and remove any space
	if direction == 'x':
		collide = pygame.sprite.spritecollide(sprite, group, False)
		if collide:
			if sprite.vel.x > 0:
				sprite.pos.x = collide[0].rect.left - sprite.rect.width
			if sprite.vel.x < 0:
				sprite.pos.x = collide[0].rect.right
			sprite.vel.x = 0
			sprite.rect.x = sprite.pos.x
	if direction == 'y':
		collide = pygame.sprite.spritecollide(sprite, group, False)
		if collide:
			if sprite.vel.y > 0:
				sprite.pos.y = collide[0].rect.top - sprite.rect.height
			if sprite.vel.y < 0:
				sprite.pos.y = collide[0].rect.bottom
			sprite.vel.y = 0
			sprite.rect.y = sprite.pos.y

class Player (pygame.sprite.Sprite):
	
	def __init__ (self, game, x, y):
		self.groups = game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.player_img
		self.rect = self.image.get_rect()
		self.vel = vector(0,0)
		self.pos = vector(x,y) * TILESIZE 

	def getKeys(self):
		global walkcount
		global left
		global right
		global down
		global up
		self.vel = vector(0,0)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] or keys[pygame.K_LEFT]:
			self.image = walkLeft[walkcount//12].convert_alpha()
			if keys[pygame.K_LSHIFT]:
				self.vel.x = -PLAYER_SPEED * 1.5
				walkcount += 2
			else:
				self.vel.x = -PLAYER_SPEED
				walkcount += 1
			left = True
			right = False
			down = False
			up = False
		elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: # change these elifs to ifs once the diagonal images are made
			self.image = walkRight[walkcount//12].convert_alpha()
			if keys[pygame.K_LSHIFT]:
				self.vel.x = PLAYER_SPEED * 1.5
				walkcount += 2
			else:
				self.vel.x = PLAYER_SPEED
				walkcount += 1
			left = False
			right = True
			down = False
			up = False
		elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
			self.image = walkDown[walkcount//12].convert_alpha()
			if keys[pygame.K_LSHIFT]:
				self.vel.y = PLAYER_SPEED * 1.5
				walkcount += 2
			else:
				self.vel.y = PLAYER_SPEED
				walkcount += 1
			left = False
			right = False
			down = True
			up = False
		elif keys[pygame.K_w] or keys[pygame.K_UP]:
			self.image = walkUp[walkcount//12].convert_alpha()
			if keys[pygame.K_LSHIFT]:
				self.vel.y = -PLAYER_SPEED * 1.5
				walkcount += 2
			else:
				self.vel.y = -PLAYER_SPEED
				walkcount += 1
			left = False
			right = False
			down = False
			up = True
		else:
			if left:
				self.image = pygame.image.load('images/side.png')
			elif right:
				self.image = pygame.image.load('images/side2.png')
			elif down:
				self.image = pygame.image.load('images/front.png')
			elif up:
				self.image = pygame.image.load('images/back.png')
			left = False
			right = False
			down = False
			up = False
		if self.vel.x != 0 and self.vel.y != 0:
			self.vel *= .7071

	def update(self):
		global walkcount
		if walkcount >= 24:
			walkcount = 0
		self.getKeys()
		self.pos.x += self.vel.x * self.game.dt
		self.pos.y += self.vel.y * self.game.dt
		self.rect.x = self.pos.x
		collision(self, self.game.boundaries,'x')
		self.rect.y = self.pos.y
		collision(self, self.game.boundaries,'y')

class Boundary (pygame.sprite.Sprite):
	def __init__ (self, game, x, y):
		self.groups = game.all_sprites, game.boundaries
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.boundary_img
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

class Mob(pygame.sprite.Sprite):
	def __init__ (self, game, x, y, type):
		self.groups = game.all_sprites, game.mobs
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		if type == 'E':
			self.image = game.es_img
			self.type = 'E'
		elif type == 'R':
			self.image = game.reap_img
			self.type = 'R'
		elif type == 'S':
			self.image = game.snail_img
			self.type = 'S'
		else:
			self.image = game.es_img
			self.type = "_"
			# temporary
		self.rect = self.image.get_rect()
		self.pos = vector(x,y) * TILESIZE
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		self.vec = 0
		self.vel = vector(0,0)
		self.acc = vector(0,0)
	
	def update(self):
		self.vec = (self.game.player.pos - self.pos).angle_to(vector(1,0))
		if self.vec > -90 and self.vec < 90:
			if self.type == 'E':
				self.image = pygame.transform.flip(self.game.es_img, True, False)
			elif self.type == 'R':
				self.image = pygame.transform.flip(self.game.reap_img, True, False)
			elif self.type == 'S':
				self.image = pygame.transform.flip(self.game.snail_img, True, False)
		elif (self.vec < -90 or self.vec > 90):
			if self.type == 'E':
				self.image = pygame.transform.flip(self.game.es_img, False, False)
			elif self.type == 'R':
				self.image = pygame.transform.flip(self.game.reap_img, False, False)
			elif self.type == 'S':
				self.image = pygame.transform.flip(self.game.snail_img, False, False)
		self.rect = self.image.get_rect()
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		if abs(self.game.player.pos.x - self.pos.x) + abs(self.game.player.pos.y - self.pos.y) < 250:
			self.acc = vector(MOB_SPEED, 0).rotate(-self.vec)
			self.acc += self.vel * -1
			self.vel += self.acc * self.game.dt
			self.pos += self.vel * self.game.dt + .5 * self.acc * self.game.dt ** 2
			self.rect.x = self.pos.x
			collision(self, self.game.boundaries,'x')
			self.rect.y = self.pos.y
			collision(self, self.game.boundaries,'y')