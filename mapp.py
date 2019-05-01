import pygame
from settings import *

class Map:
	def __init__(self, filename):
		self.data = []
		with open(filename, 'rt') as file:
			for line in file:
				self.data.append(line.strip()) # strip to remove \n and fix the camera
		self.tilewidth = len(self.data[0])
		self.tileheight = len(self.data)
		self.width = self.tilewidth * TILESIZE
		self.height = self.tileheight * TILESIZE

class Cam:
	# camera to follow player that adjusts using map offset
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.camera = pygame.Rect(0,0,width,height)

	def call(self, entity):
		# shifts the rectangular camera by 64 pixels
		return entity.rect.move(self.camera.topleft)

	def update(self, entity):
		x = -entity.rect.x + int(WIDTH / 2) - 32
		y = -entity.rect.y + int(HEIGHT / 2)

		x = min(0, x)
		y = min(0, y)
		x = max(WIDTH - self.width, x)
		y = max(HEIGHT - self.height, y)
		self.camera = pygame.Rect(x, y, self.width, self.height)
