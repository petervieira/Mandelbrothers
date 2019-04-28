import pygame
import sys
import os
from settings import *
from sprites import *
from os import path
from mapp import *

# HUD
def draw_player_health(surface,x,y,percent):
	if percent < 0:
		percent = 0
	BAR_LENGTH = 512
	BAR_HEIGHT = 30
	fill = percent * BAR_LENGTH
	outlineRect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
	fillRect = pygame.Rect(x,y,fill,BAR_HEIGHT)
	if percent > .6:
		color = (0,255,0)
	elif percent > .3:
		color = (255,255,0)
	else:
		color = (255,0,0)
	pygame.draw.rect(surface,color,fillRect)
	pygame.draw.rect(surface,(255,255,255),outlineRect, 2)
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
		pygame.mixer.music.load('music/intro.wav')
		pygame.mixer.music.set_volume(.5)
		pygame.mixer.music.play(-1, 0.0)
		self.map = Map(path.join(gameFolder, 'overworld.txt'))
		self.player_img = pygame.transform.scale(pygame.image.load('images/back.png').convert_alpha(), (64,64))
		self.es_img = pygame.transform.scale(pygame.image.load('images/electric_snake.png').convert_alpha(), (64,64))
		self.reap_img = pygame.transform.scale(pygame.image.load('images/reaper.png').convert_alpha(), (64,64))
		self.snail_img = pygame.transform.scale(pygame.image.load('images/snail.png').convert_alpha(), (64,64))
		self.floor_img = pygame.transform.scale(pygame.image.load('images/floor.png').convert_alpha(), (64,64))
		self.boundary_img = pygame.image.load('images/wall.png').convert_alpha()
		#self.boundary_img = pygame.transform.scale(pygame.image.load('images/ames.png').convert_alpha(), (64,64))
		# add another boundary scaled down to allow for smooth passage
		self.arrow_img = pygame.image.load('images/arrow.png').convert_alpha()

	def newGame(self):
		self.all_sprites = pygame.sprite.Group()
		self.boundaries = pygame.sprite.Group()
		self.mobs = pygame.sprite.Group()
		self.projectiles = pygame.sprite.Group()
		for row in range(0, len(self.map.data)):
			for col in range (0, len(self.map.data[row])):
				if self.map.data[row][col] == ',':
					Boundary(self,col,row)
				if self.map.data[row][col] == 'P':
					self.player = Player(self,col,row)
				if self.map.data[row][col] == 'E':
					Mob(self,col,row,'E')
				if self.map.data[row][col] == 'R':
					Mob(self,col,row,'R')
				if self.map.data[row][col] == 'S':
					Mob(self,col,row,'S')
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
		# player gets hit by mob
		hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
		for hit in hits:
			self.player.health -= hit.damage
			hit.vel = vector(0,0)
			if self.player.health <= 0:
				self.playing = False
		
		# add knockback or cooldown for attacks
		
		# mob gets hit by player
		hits = pygame.sprite.groupcollide(self.mobs, self.projectiles, False, True)
		for hit in hits:
			hit.health -= PROJECTILE_DAMAGE
			hit.vel = vector(0,0)
	
	def drawGrid(self):
		# outlines tiles
		for x in range(0, WIDTH, TILESIZE):
			pygame.draw.line(self.screen, (0,0,0), (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pygame.draw.line(self.screen, (0,0,0), (0, y), (WIDTH, y))
	
	def drawScreen(self):
		# renders the screen
		#pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		self.screen.fill(BACKGROUND_COLOR)
		for i in range (0, WIDTH//TILESIZE):
			for j in range (0, HEIGHT//TILESIZE):
				self.screen.blit(self.floor_img, [i*TILESIZE,j*TILESIZE])
		#self.drawGrid()
		for sprite in self.all_sprites:
			if isinstance(sprite, Mob):
				sprite.drawHealth()
			self.screen.blit(sprite.image, self.camera.call(sprite))
		#pygame.draw.rect(self.screen, (255,255,255), self.camera.call(self.player), 2)
		draw_player_health(self.screen,256,728,self.player.health/self.player.fullHealth)
		
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
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.quit()

# here we create the game and run it
game = Game()
game.initScreen()
while True:
	game.newGame()
	game.run()
	game.mainScreen()