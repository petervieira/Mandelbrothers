import pygame as pg
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
	outlineRect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
	fillRect = pg.Rect(x,y,fill,BAR_HEIGHT)
	if percent > .6:
		color = (0,255,0)
	elif percent > .3:
		color = (255,255,0)
	else:
		color = (255,0,0)
	pg.draw.rect(surface,color,fillRect)
	pg.draw.rect(surface, (255,255,255), outlineRect, 2)
	
def draw_boss_health(surface,x,y,percent):
	if percent < 0:
		percent = 0
	BAR_LENGTH = 712
	BAR_HEIGHT = 30
	fill = percent * BAR_LENGTH
	outlineRect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
	fillRect = pg.Rect(x,y,fill,BAR_HEIGHT)
	if percent > .6:
		color = (120,0,0)
	elif percent > .3:
		color = (180,0,0)
	else:
		color = (255,0,0)
	pg.draw.rect(surface,color,fillRect)
	pg.draw.rect(surface, (255,255,255), outlineRect, 2)

class Game:
	def __init__(self):
		os.environ['SDL_VIDEO_CENTERED'] = "1"
		pg.mixer.pre_init(44100, -16, 2, 2048)
		pg.mixer.init()
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # add parameter, pg.FULLSCREEN when finished
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		# pg.key.set_repeat(250, 100) # while holding down key, parameter 1 is number of milliseconds before game performs key press twice. It will then occur every (parameter 2) milliseconds
		self.on_main_menu = True
		self.paused = False
		self.game_over = False
		self.win = False
		self.interact = True
		self.sprites = {}
		self.wave = 1
		self.textboxIndex = 0
		self.textboxDelay = 0
		self.alpha = 0
		self.load_data()


	def load_data(self):
		if getattr(sys, 'frozen', False):
		    gameFolder = os.path.dirname(sys.executable)
		else:
		    gameFolder = os.path.dirname(os.path.realpath(__file__))

		pg.mixer.music.load('music/theme.wav')
		pg.mixer.music.set_volume(.5)
		pg.mixer.music.play(-1, 0.0)
		self.map = TiledMap(path.join(gameFolder, 'maps/overworld.tmx'))
		self.map_img = self.map.make_map()
		self.map_rect = self.map_img.get_rect()
		self.minimap = Minimap(self)
		self.load_sprites(['flame', 'arrow', 'icyrock', 'oldman', 'oldman_back', 'oldman_left', 'oldman_right', 'warp', 'golem', 'lantern', 'bear', 'icebow', 'icearrow', 'brother', 'triplearrow', 'speed', 'damage', 'end-game', 'health', 'octodaddypog', 'octodaddyhit', 'menu', 'shield', 'pierce'])
		self.load_sprites_scaled([
			('side', 48, 64),
			('side2', 48, 64),
			('front', 48, 64),
			('back', 48, 64),
			('walk', 48, 64),
			('walk2', 48, 64),
			('front_walk', 48, 64),
			('front_walk2', 48, 64),
			('side_walk', 48, 64),
			('side_walk2', 48, 64),
			('side2_walk', 48, 64),
			('side2_walk2', 48, 64),
			('electric_snake', 64, 64),
			('reaper', 64, 64),
			('snail', 64, 64),
			('coin1', 32, 32),
			('coin2', 32, 32),
			('coin3', 32, 32),
			('coin4', 32, 32),
			('coin5', 32, 32)
		])
		self.load_sounds(['hit', 'shoot', 'coin'])
		self.textboxes = [
			Textbox('Welcome to Mandelbrothers!', self, self.sprites['brother']),
			Textbox('Use the WASD keys or the arrow keys to move around.', self, self.sprites['brother']),
			Textbox('Use SHIFT to sprint, but you can\'t shoot while sprinting.', self, self.sprites['brother']),
			Textbox('Use Z or SPACE to shoot, and Z to interact with people.', self, self.sprites['brother']),
			Textbox('The goal is to make it to the portal at the top of the map.', self, self.sprites['brother']),
			Textbox('Good luck!', self, self.sprites['brother'])]

	def load_sprites(self, sprites):
		for name in sprites:
			self.sprites[name] = pg.image.load('images/' + name + '.png').convert_alpha()

	def load_sprites_scaled(self, images):
		for (name, w, h) in images:
			self.sprites[name] = pg.transform.scale(pg.image.load('images/' + name + '.png').convert_alpha(), (w, h))

	def load_sounds(self, sounds):
		self.sounds = dict([(name, pg.mixer.Sound('sounds/' + name + '.wav')) for name in sounds])

	def newGame(self):
		self.all_sprites = pg.sprite.LayeredUpdates()
		self.boundaries = pg.sprite.Group()
		self.mobs = pg.sprite.Group()
		self.npcs = pg.sprite.Group()
		self.projectiles = pg.sprite.Group()
		self.warps = pg.sprite.Group()
		self.items = pg.sprite.Group()
		self.coins = pg.sprite.Group()

		self.camera = Cam(self.map.width, self.map.height)

		for tile_object in self.map.tmxdata.objects:
			if tile_object.name == 'player':
				self.player = Player(self, tile_object.x, tile_object.y)
			if tile_object.name == 'oldman':
				NPC(self, tile_object.x, tile_object.y, 'OM')
			if tile_object.name == 'shop':
				WarpZone(self, tile_object.x, tile_object.y, 'shop')
			if tile_object.name == 'overworld':
				WarpZone(self, tile_object.x, tile_object.y, 'overworld')
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
			if tile_object.name == 'golem':
				Mob(self,tile_object.x,tile_object.y,'G')
			if tile_object.name == 'lantern':
				Mob(self,tile_object.x,tile_object.y,'L')
			if tile_object.name == 'bear':
				Mob(self,tile_object.x,tile_object.y,'B')
			if tile_object.name == 'octodaddy':
				Mob(self,tile_object.x,tile_object.y,'O')
			if tile_object.name in ['icebow', 'triplebow', 'shoot', 'damage', 'armor', 'health', 'end-game', 'pierce'] and not SHOP[tile_object.name]:
				Item(self, (tile_object.x, tile_object.y), tile_object.name)

		SHOP['health'] = False

	def main_menu(self):
		self.screen.blit(self.sprites['menu'], (0,0))
		pg.display.flip()

	def run(self):
		# game loop
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			if self.on_main_menu:
				self.main_menu()
			else:
				if not (self.paused or self.game_over) and (not self.win or self.interact):
					self.update()
				self.drawScreen()

	def quit(self):
		pg.quit()
		sys.exit()

	def update(self):
		self.all_sprites.update()
		self.camera.update(self.player)

		# player gets hit by mob
		for hit in pg.sprite.spritecollide(self.player, self.mobs, False):
			time = pg.time.get_ticks()
			if time - hit.last_attack > ENEMY_COOLDOWN:
				self.player.health -= hit.damage
				STATUS['health'] -= hit.damage
				hit.last_attack = time
				self.sounds['hit'].play()
				self.sounds['hit'].set_volume(.3)
			hit.vel = vector(0,0)

		if self.interact and self.textboxIndex == len(self.textboxes) - 1 and self.textboxDelay > TEXTBOX_DELAY and any(pg.key.get_pressed()) and not pg.key.get_pressed()[pg.K_z]:
			self.textboxIndex = 0
			self.interact = False
		self.textboxDelay += self.dt * 1000

		# mob gets hit by player projectile
		collisions = pg.sprite.groupcollide(self.mobs, self.projectiles, False, False)
		for hit in collisions:
			for projectile in collisions[hit]:
				if projectile.type == 'arrow':
					if hit.last_hit > ENEMY_HIT_COOLDOWN:
						hit.last_hit = 0
						self.sounds['hit'].play()
						self.sounds['hit'].set_volume(.3)
						if SHOP['icebow']:
							hit.slowtime = pg.time.get_ticks()
						if SHOP['damage']:
							damage = PROJECTILE_DAMAGE * 2
						else:
							damage = PROJECTILE_DAMAGE
						hit.health -= damage * len(collisions[hit])
						if not SHOP['pierce'] or hit.type == 'O':
							for projectile in collisions[hit]:
								projectile.kill()
					if hit.type == 'B':
						hit.speed = 450
						hit.maxSpeed = 450
					if hit.type == 'O':
						hit.damaged = pg.time.get_ticks()
						hit.image = game.sprites['octodaddyhit']
		for hit in pg.sprite.spritecollide(self.player, self.projectiles, False):
			if hit.type == 'icyrock':
				self.player.health -= 15
				hit.kill()

		if self.player.health <= 0:
			self.game_over = True
			SHOP['shop'] = False
			SHOP['icebow'] = False
			SHOP['triplebow'] = False
			SHOP['damage'] = False
			SHOP['shoot'] = False
			SHOP['armor'] = False
			SHOP['health'] = False
			SHOP['pierce'] = False
			SHOP['end-game'] = False
			STATUS['money'] = 0
			STATUS['health'] = 100
			STATUS['fullHealth'] = 100
			STATUS['overVisit'] = 1
			STATUS['shopvisit'] = 0

	def drawScreen(self):
		# renders the screen
		pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
		#self.map_img.set_alpha(25)
		self.screen.blit(self.map_img, self.camera.callRect(self.map_rect))
		temp = pg.Surface((1024, 768))
		temp.fill((0,0,0))
		temp.set_alpha(self.alpha)
		self.screen.blit(temp, (0,0))

		for sprite in self.items:
			self.screen.blit(sprite.image, self.camera.call(sprite))

		for sprite in self.all_sprites:
			if not isinstance(sprite, Item):
				if isinstance(sprite, Mob):
					if sprite.type != 'O':
						sprite.drawHealth()
				elif isinstance(sprite, Player):
					pg.draw.ellipse(self.screen, (32, 32, 32), pg.Rect(sprite.rect.x + 8, sprite.rect.y + 48, sprite.rect.width - 16, 16).move(self.camera.camera.topleft))
			self.screen.blit(sprite.image, self.camera.call(sprite))
			if isinstance(sprite, Mob):
				if sprite.type == 'O':
					draw_boss_health(self.screen, 156, 10, sprite.health / sprite.fullHealth)
					font = pg.font.Font(pg.font.match_font('papyrus'), 22)
					surface = font.render('Octodaddy', True, (0, 0, 0))
					rect = surface.get_rect()
					rect.center = (512, 26)
					self.screen.blit(surface, rect)

		self.minimap.draw()

		if self.interact:
			self.textboxes[self.textboxIndex].render()
		else:
			draw_player_health(self.screen, 256, 728, self.player.health / self.player.fullHealth)
			font = pg.font.Font(pg.font.match_font('papyrus'), 48)
			surface = font.render(str(self.player.health), True, (0, 0, 0))
			rect = surface.get_rect()
			rect.center = (512, 743)
			self.screen.blit(surface, rect)
		for hit in pg.sprite.spritecollide(self.player, self.items, False):
			hit.draw_textbox()

		self.screen.blit(self.sprites['coin1'], (16, 16))
		font = pg.font.Font(pg.font.match_font('papyrus'), 48)
		surface = font.render(str(self.player.money), True, (255, 255, 255))
		rect = surface.get_rect()
		rect.midleft = (52, 32)
		self.screen.blit(surface, rect)

		if self.paused:
			font = pg.font.Font(pg.font.get_default_font(), 32)
			surface = font.render('Paused', True, (255, 255, 255))
			rect = surface.get_rect()
			rect.center = (WIDTH // 2, HEIGHT // 2)
			self.screen.blit(surface, rect)

		if self.game_over:
			font = pg.font.Font(pg.font.match_font('papyrus'), 96)
			font2 = pg.font.Font(pg.font.match_font('papyrus'), 32)
			surface = font.render('Game Over', True, (255, 255, 255))
			surface2 = font2.render(f'Made it to wave {self.wave}', True, (255, 255, 255))
			surface3 = font2.render('Press space to continue', True, (255, 255, 255))
			rect = surface.get_rect()
			rect2 = surface2.get_rect()
			rect3 = surface3.get_rect()
			rect.center = (WIDTH // 2, HEIGHT // 2)
			rect2.center = (WIDTH // 2, HEIGHT // 2 + 80)
			rect3.center = (WIDTH // 2, HEIGHT - 80)
			self.screen.blit(surface, rect)
			self.screen.blit(surface2, rect2)
			self.screen.blit(surface3, rect3)

		if self.win and not self.interact:
			font = pg.font.Font(pg.font.match_font('papyrus'), 96)
			surface = font.render('Congrats! You win!', True, (255, 255, 255))
			rect = surface.get_rect()
			rect.center = (WIDTH // 2, HEIGHT // 2)
			self.screen.blit(surface, rect)

		pg.display.flip()

	def events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				elif event.key == pg.K_SPACE:
					if self.on_main_menu:
						pg.mixer.music.load('music/theme2.wav')
						pg.mixer.music.set_volume(.5)
						pg.mixer.music.play(-1, 0.0)
						self.newGame()
						self.on_main_menu = False
					elif self.game_over:
						self.playing = False
					elif self.win and not self.interact:
						self.playing = False
				elif event.key == pg.K_p:
					if self.paused:
						pg.mixer.music.unpause()
						self.paused = False
					elif not self.on_main_menu:
						pg.mixer.music.pause()
						self.paused = True
				elif event.key == pg.K_z and self.interact and self.textboxDelay > TEXTBOX_DELAY and self.textboxIndex < len(self.textboxes) - 1:
						self.textboxDelay = 0
						self.textboxIndex += 1

# create the game and run it
while True:
	game = Game()
	game.run()
