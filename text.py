import pygame as pg
from settings import *

class Textbox:
	def __init__ (self, text, game, icon):
		self.game = game
		self.icon = icon
		self.pos = (64, self.game.screen.get_height() - 66)
		self.size = (self.game.screen.get_width() - 66, 64)
		self.font = pg.font.Font(pg.font.match_font('papyrus'), 36)
		self.text = text

	def render(self):
		self.game.screen.blit(self.icon, (0, self.game.screen.get_height() - 64)) # puts npc icon in the bottom left of the screen
		pg.draw.rect(self.game.screen, (200, 200, 200), pg.Rect((self.pos[0] - 2, self.pos[1] - 2), (self.size[0] + 4, self.size[1] + 4)))
		pg.draw.rect(self.game.screen, (0, 0, 0), pg.Rect(self.pos, self.size))
		surface = self.font.render(self.text, 1, (255, 255, 255), (0, 0, 0))
		self.game.screen.blit(surface, (40 + WIDTH / 2 - self.font.size(self.text)[0] / 2, self.game.screen.get_height() - 64))  # put it onto the screen
		self.game.screen.blit(pg.font.Font(pg.font.get_default_font(), 50).render('Z', 1, (255, 0, 255), (80, 80, 80)), (WIDTH - 32, self.game.screen.get_height() - 120))