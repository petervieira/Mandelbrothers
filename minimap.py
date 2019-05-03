import pygame as pg
from settings import *

class Minimap:
	def __init__(self):
		self.width = 49 * TILESIZE / 16
		self.height = 68 * TILESIZE / 16
		self.rect = pg.Rect(1, HEIGHT - self.height - 1, self.width, self.height)

	def update(self):
		pass

	def draw(self, surface, boundaries, enemies, player):
		pg.draw.rect(surface, (0, 0, 0), self.rect)
		pg.draw.rect(surface, (0, 0, 255), pg.Rect(self.rect.x - 1, self.rect.y - 1, self.width + 2, self.height + 2), 1)

		for sprite in boundaries:
			pg.draw.rect(surface, (64, 64, 64), pg.Rect(self.rect.x + sprite.x / 16, self.rect.y + sprite.y / 16, sprite.w / 16, sprite.h / 16))
			# FIX PIXEL PROBLEM

		for enemy in enemies:
			x = enemy.pos.x / TILESIZE
			y = enemy.pos.y / TILESIZE
			pg.draw.rect(surface, (255, 0, 0), pg.Rect(self.rect.x + x * 4, self.rect.y + y * 4 , 4, 4))

		x = player.pos.x / TILESIZE
		y = player.pos.y / TILESIZE

		pg.draw.rect(surface, (0, 255, 0), pg.Rect(self.rect.x + x * 4, self.rect.y + y * 4, 4, 4))