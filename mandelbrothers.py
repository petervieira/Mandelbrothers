import pygame
import sys
import os
from settings import *
from sprites import *
from os import path
from mapp import *
from minimap import *

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
	pygame.draw.rect(surface, (255,255,255), outlineRect, 2)

class Game:
	def __init__(self):
		os.environ['SDL_VIDEO_CENTERED'] = "1"
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.mixer.init()
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption(TITLE)
		self.clock = pygame.time.Clock()
		pygame.key.set_repeat(250, 100) # while holding down key, parameter 1 is number of milliseconds before game performs key press twice. It will then occur every (parameter 2) milliseconds
		self.on_main_menu = True
		self.paused = False
		self.minimap = Minimap()
		self.load_data()

	def load_data(self):
		gameFolder = path.dirname(__file__)
		pygame.mixer.music.load('music/theme.wav')
		pygame.mixer.music.set_volume(.5)
		pygame.mixer.music.play(-1, 0.0)
		self.map = TiledMap(path.join(gameFolder, 'maps/overworld.tmx'))
		self.map_img = self.map.make_map()
		self.map_rect = self.map_img.get_rect()
		self.player_img = pygame.transform.scale(pygame.image.load('images/back.png').convert_alpha(), (48,64))
		self.es_img = pygame.transform.scale(pygame.image.load('images/electric_snake.png').convert_alpha(), (64,64))
		self.reap_img = pygame.transform.scale(pygame.image.load('images/reaper.png').convert_alpha(), (64,64))
		self.snail_img = pygame.transform.scale(pygame.image.load('images/snail.png').convert_alpha(), (64,64))
		self.flame_img = pygame.image.load('images/flame.png').convert_alpha()
		self.arrow_img = pygame.image.load('images/arrow.png').convert_alpha()
		self.boundary_img = pygame.image.load('images/wall.png').convert_alpha()
		self.coin_img = pygame.transform.scale(pygame.image.load('images/coin.png').convert_alpha(), (32, 32))
		self.load_sounds(['hit', 'shoot', 'coin'])

	def load_sounds(self, sounds):
		self.sounds = dict([(name, pygame.mixer.Sound('sounds/' + name + '.wav')) for name in sounds])

	def newGame(self):
		self.all_sprites = pygame.sprite.Group()
		self.boundaries = pygame.sprite.Group()
		self.mobs = pygame.sprite.Group()
		self.projectiles = pygame.sprite.Group()
		#for row in range(0, len(self.map.data)):
		#	for col in range (0, len(self.map.data[row])):
		#		if self.map.data[row][col] == ',':
		#			Boundary(self,col,row)
		#		if self.map.data[row][col] == 'P':
		#			self.player = Player(self,col,row)
		#		if self.map.data[row][col] == 'E':
		#			Mob(self,col,row,'E')
		#		if self.map.data[row][col] == 'R':
		#			Mob(self,col,row,'R')
		#		if self.map.data[row][col] == 'F':
		#			Mob(self,col,row,'F')
		#		if self.map.data[row][col] == 'S':
		#			Mob(self,col,row,'S')
		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == 'player':
				self.player = Player(self, tile_object.x, tile_object.y)
			if tile_object.name == 'wall':
				Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
			if tile_object.name == 'snake':
				Mob(self,tile_object.x,tile_object.y,'E')
			if tile_object.name == 'snail':
				Mob(self,tile_object.x,tile_object.y,'S')
			if tile_object.name == 'reaper':
				Mob(self,tile_object.x,tile_object.y,'R')
			if tile_object.name == 'flame':
				Mob(self,tile_object.x,tile_object.y,'F')
		self.camera = Cam(self.map.width, self.map.height)
	
	def main_menu(self):
		font = pygame.font.Font(pygame.font.get_default_font(), 64)
		surface = font.render('Mandelbrothers', True, (255, 255, 255))
		rect = surface.get_rect()
		rect.center = (WIDTH // 2, 100)
		self.screen.blit(surface, rect)

		font = pygame.font.Font(pygame.font.get_default_font(), 32)
		surface = font.render('Press space to begin', True, (255, 255, 255))
		rect = surface.get_rect()
		rect.center = (WIDTH // 2, 600)
		self.screen.blit(surface, rect)

		pygame.display.flip()	

	def run(self):
		# game loop
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			if self.on_main_menu:
				self.main_menu()
			else:
				if not self.paused:
					self.update()
				self.drawScreen()

	def quit(self):
		pygame.quit()
		sys.exit()

	def update(self):
		self.all_sprites.update()
		self.camera.update(self.player)
		
		# player gets hit by mob
		for hit in pygame.sprite.spritecollide(self.player, self.mobs, False):
			time = pygame.time.get_ticks()
			if time - hit.last_attack > ENEMY_COOLDOWN:
				self.player.health -= hit.damage
				hit.last_attack = time
				self.sounds['hit'].play()
			hit.vel = vector(0,0)
			if self.player.health <= 0:
				self.playing = False
		
		# mob gets hit by player
		for hit in pygame.sprite.groupcollide(self.mobs, self.projectiles, False, True):
			self.sounds['hit'].play()
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
		#self.screen.fill(BACKGROUND_COLOR)
		self.screen.blit(self.map_img, self.camera.callRect(self.map_rect))
		#for i in range (0, WIDTH//TILESIZE):
		#	for j in range (0, HEIGHT//TILESIZE):
		#		self.screen.blit(self.floor_img, [i*TILESIZE,j*TILESIZE])
		#self.drawGrid()
		for sprite in self.all_sprites:
			if isinstance(sprite, Mob):
				sprite.drawHealth()
			self.screen.blit(sprite.image, self.camera.call(sprite))
		#pygame.draw.rect(self.screen, (255,255,255), self.camera.call(self.player), 2)
		draw_player_health(self.screen,256,728,self.player.health/self.player.fullHealth)
		self.minimap.draw(self.screen, self.boundaries, self.mobs, self.player)
		font = pygame.font.Font(pygame.font.get_default_font(), 32)
		surface = font.render(f'Money: {self.player.money}', True, (255, 255, 255))
		rect = surface.get_rect()
		rect.topleft = (10, 10)
		self.screen.blit(surface, rect)
		if self.paused:
			font = pygame.font.Font(pygame.font.get_default_font(), 64)
			surface = font.render('Paused', True, (255, 255, 255))
			rect = surface.get_rect()
			rect.center = (WIDTH // 2, HEIGHT // 2)
			self.screen.blit(surface, rect)
		
		pygame.display.flip()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.quit()
				elif event.key == pygame.K_SPACE and self.on_main_menu:
					self.newGame()
					self.on_main_menu = False
				elif event.key == pygame.K_p:
					if self.paused:
						pygame.mixer.music.unpause()
						self.paused = False
					else:
						pygame.mixer.music.pause()
						self.paused = True

# create the game and run it
while True:
	game = Game()
	game.run()