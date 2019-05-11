import pygame as pg
from settings import *

class Textbox:
	def __init__ (self, text, game, icon):
		self.game = game
		self.game.screen.blit(icon,(0, self.game.screen.get_height() - 64)) # puts npc icon in the bottom left of the screen
		barPos = (64, self.game.screen.get_height() - 66)
		barSize = (self.game.screen.get_width() - 66, 64)
		pg.draw.rect(self.game.screen,(200,200,200),pg.Rect((barPos[0]-2,barPos[1]-2),(barSize[0]+4, barSize[1] + 4)))
		pg.draw.rect(self.game.screen,(0,0,0),pg.Rect(barPos,barSize))
		font = pg.font.Font(pg.font.match_font('papyrus'), 36)
		displayText = font.render(text,1,(255,255,255),(0,0,0))
		self.game.screen.blit(displayText,(40 + WIDTH / 2 - font.size(text)[0] / 2, self.game.screen.get_height() - 64))  #put it onto the screen
		cont = True
		while cont:
			pg.event.pump() #keep pygame updated
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.game.quit()
				elif event.type == pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						self.game.quit()
					elif event.key == pg.K_z:
						pg.time.delay(750)
						cont = False
			pg.display.flip()
			self.game.clock.tick(60)