import pygame as pg
from settings import *

class Textbox:
	def __init__ (self, text, game, icon):
		self.game = game
		self.game.screen.blit(icon,(0, self.game.screen.get_height() - 64)) # puts npc icon in the bottom left of the screen
		barPos = (64, self.game.screen.get_height() - 64)
		barSize = (self.game.screen.get_width() - 64, 64)
		pg.draw.rect(self.game.screen,(0,0,0),pg.Rect(barPos,barSize))
		font = pg.font.Font(pg.font.match_font('papyrus'), 44)
		displayText = font.render(text,1,(255,255,255),(0,0,0))
		self.game.screen.blit(displayText,(40 + WIDTH / 2 - font.size(text)[0] / 2, self.game.screen.get_height() - 64))  #put it onto the screen
		cont = True
		while cont: #now we have a while loop so the game effectively pauses 
			pg.event.pump() #keep pygame updated
			if pg.key.get_pressed()[pg.K_x]: 
				cont = False
			pg.display.flip()
			self.game.clock.tick(60)