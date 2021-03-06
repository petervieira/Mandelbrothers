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
		self.currentIndex = 1

	def render(self):
		# draw textbox
		self.game.screen.blit(self.icon, (0, self.game.screen.get_height() - 64)) # puts npc icon in the bottom left of the screen
		
		if len(self.game.textboxes) - 1 != self.game.textboxIndex:
			pg.draw.rect(self.game.screen, (200, 200, 200), pg.Rect(WIDTH - 226, HEIGHT - 117, 226, 119))
			pg.draw.rect(self.game.screen, (20, 20, 20), pg.Rect(WIDTH - 224, HEIGHT - 115, 222, 115))
			self.game.screen.blit(pg.font.Font(pg.font.match_font('papyrus'), 30).render('Continue:', 1, (0, 155, 155), (20, 20, 20)), (WIDTH - 200, HEIGHT - 115))
			self.game.screen.blit(pg.font.Font(pg.font.match_font('papyrus'), 30).render('Z', 1, (155, 0, 155), (20, 20, 20)), (WIDTH - 56, HEIGHT - 115))
		pg.draw.rect(self.game.screen, (200, 200, 200), pg.Rect((self.pos[0] - 2, self.pos[1] - 2), (self.size[0] + 4, self.size[1] + 4)))
		pg.draw.rect(self.game.screen, (0, 0, 0), pg.Rect(self.pos, self.size))

		# draw one more character than last frame
		self.currentIndex = min(self.currentIndex + 1, len(self.text))

		# draw text
		surface = self.font.render(self.text[:self.currentIndex], 1, (255, 255, 255), (0, 0, 0))
		self.game.screen.blit(surface, (40 + WIDTH / 2 - self.font.size(self.text)[0] / 2, self.game.screen.get_height() - 64))  # put it onto the screen
