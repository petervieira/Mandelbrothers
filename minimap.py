import pygame as pg
from settings import *
import math

class Minimap:
	def __init__(self, game):
		self.game = game
		self.width = 49 * TILESIZE / 16
		self.height = 68 * TILESIZE / 16
		self.rect = pg.Rect(WIDTH - self.width - 1, 1, self.width, self.height)

	def draw(self):
		pg.draw.rect(self.game.screen, (0, 0, 0), self.rect)
		pg.draw.rect(self.game.screen, (0, 0, 255), pg.Rect(self.rect.x - 1, self.rect.y - 1, self.width + 2, self.height + 2), 1)

		for sprite in self.game.boundaries:
			pg.draw.rect(self.game.screen, (64, 64, 64), pg.Rect(self.rect.x + sprite.x / 16, self.rect.y + sprite.y / 16, sprite.w / 16, sprite.h / 16))
		
		for npc in self.game.npcs:
			x = npc.pos.x / TILESIZE
			y = npc.pos.y / TILESIZE
			pg.draw.rect(self.game.screen, (0, 0, 255), pg.Rect(self.rect.x +  x * 4, self.rect.y + y * 4 , 4, 4))

		for mob in self.game.mobs:
			x = mob.pos.x / TILESIZE
			y = mob.pos.y / TILESIZE
			pg.draw.rect(self.game.screen, (255, 0, 0), pg.Rect(self.rect.x + x * 4, self.rect.y + y * 4 , 4, 4))

		x = (self.game.player.pos.x + (self.game.player.rect.width - TILESIZE) / 2) / TILESIZE
		y = self.game.player.pos.y / TILESIZE

		pg.draw.rect(self.game.screen, (0, 255, 0), pg.Rect(self.rect.x + x * 4, self.rect.y + y * 4, 4, 4))
