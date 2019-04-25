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
				self.image = walkLeft[walkcount//12].convert_alpha()
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
				self.image = walkRight[walkcount//12].convert_alpha()
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
				self.image = walkDown[walkcount//12].convert_alpha()
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
				self.image = walkUp[walkcount//12].convert_alpha()
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
		self.collision('x')
		self.rect.y = self.pos.y
		self.collision('y')

		
	def collision(self, direction):
		# position the character to press against the wall and remove any space
		# smooths out the movement and allows sliding on walls
		if direction == 'x':
			collide = pygame.sprite.spritecollide(self, self.game.boundaries, False)
			if collide:
				if self.vel.x > 0:
					self.pos.x = collide[0].rect.left - self.rect.width
				if self.vel.x < 0:
					self.pos.x = collide[0].rect.right
				self.vel.x = 0
				self.rect.x = self.pos.x
		if direction == 'y':
			collide = pygame.sprite.spritecollide(self, self.game.boundaries, False)
			if collide:
				if self.vel.y > 0:
					self.pos.y = collide[0].rect.top - self.rect.height
				if self.vel.y < 0:
					self.pos.y = collide[0].rect.bottom
				self.vel.y = 0
				self.rect.y = self.pos.y

class Boundary (pygame.sprite.Sprite):
	def __init__ (self, game, x, y):
		self.groups = game.all_sprites, game.boundaries
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pygame.Surface((TILESIZE,TILESIZE))
		self.image.fill((70,70,70))
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE