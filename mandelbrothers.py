import pygame
import sys
import os
from settings import *
from sprites import *
from os import path
from mapp import *

class Game:
	def __init__(self):
		os.environ['SDL_VIDEO_CENTERED'] = "1"
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(250, 100) # while holding down key, parameter 1 is number of milliseconds before game performs key press twice. It will then occur every (parameter 2) milliseconds
		self.load_data()

	def load_data(self):
		gameFolder = path.dirname(__file__)
		imageFolder = path.join(gameFolder, 'images')
		self.map = Map(path.join(gameFolder, 'overworld.txt'))
		self.player_img = pygame.image.load(path.join(imageFolder, PLAYER_IMAGE)).convert_alpha()
	
	def newGame(self):
		self.all_sprites = pygame.sprite.Group()
		self.boundaries = pygame.sprite.Group()
		for row in range(0, len(self.map.data)):
			for col in range (0, len(self.map.data[row])):
				if self.map.data[row][col] == ',':
					Boundary(self,col,row)
				if self.map.data[row][col] == 'P':
					self.player = Player(self,col,row)
		self.camera = Cam(self.map.width, self.map.height)
					
	def run(self):
		# game loop
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.drawScreen()

	def quit(self):
		pygame.quit()
		sys.exit()

	def update(self):
		self.all_sprites.update()
		self.camera.update(self.player)
	
	def drawGrid(self):
		# outlines tiles
		for x in range(0, WIDTH, TILESIZE):
			pygame.draw.line(self.screen, (0,0,0), (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pygame.draw.line(self.screen, (0,0,0), (0, y), (WIDTH, y))
	
	def drawScreen(self):
		# renders the screen
		self.screen.fill(BACKGROUND_COLOR)
		self.drawGrid()
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.call(sprite))
		#pygame.draw.rect(self.screen, (255,255,255), self.camera.call(self.player), 2)
		pygame.display.flip()
	
	def initScreen(self):
		# main menu
		pass

	def mainScreen(self):
		# actual game
		pass

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
				# add something for escape

# here we create the game and run it
game = Game()
game.initScreen()
while True:
	game.newGame()
	game.run()
	game.mainScreen()