
#music by onky Hardmoon / Arjen Schumacher
#art by kenny
import pygame
import random
import time
from os import path

bullet_dir = path.join(path.dirname(__file__),'Assets','Images','Lasers')
ship_dir = path.join(path.dirname(__file__),'Assets','Images','Ships')
meteor_dir = path.join(path.dirname(__file__),'Assets','Images','Meteors')
ship_exp_dir = path.join(path.dirname(__file__),'Assets','Images','Explosions','ship_explo_dir')
meteor_exp_dir = path.join(path.dirname(__file__),'Assets','Images','Explosions','meteor_explo_dir')
snd_dir = path.join(path.dirname(__file__),'Assets','Music')
img_dir = path.join(path.dirname(__file__),'Assets','Images')


width = 800
height = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,128)

RED = (150,0,0)
GREEN = (0,200,0)
BLUE = (0,0,200)

BRED = (255,0,0)
BGREEN = (0,255,0)
BBLUE = (0,0,255)

YELLOW = (255,255,0)

pygame.init() 
pygame.mixer.init()
game = pygame.display.set_mode((width,height))
pygame.display.set_caption("SPACE DODGING")
clock = pygame.time.Clock()

font_name =pygame.font.match_font('comicsans')
def draw(surf, text, size, x, y,colour):
	font = pygame.font.Font(font_name, size)
	txt_surface = font.render(text, True, colour)
	txt_rect =txt_surface.get_rect()
	txt_rect = (x,y)
	surf.blit(txt_surface,txt_rect)

def newmob():
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

def draw_shield(surf, x, y, perc):
	if perc < 0:
		perc = 0
	L = 100
	H = 10
	fill =  perc   
	O_rect = pygame.Rect(x, y, L, H)
	fill_rect = pygame.Rect(x, y, fill, H)
	pygame.draw.rect(surf, BGREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, O_rect,2)

def draw_lives(surf, x, y, lives, img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x +35 * i
		img_rect.y = y
		surf.blit(img, img_rect)

def show_go_screen():
	game.blit(bground,bground_rect)
	draw(game, "Space Dodging", 75, width/2 -160 , height/4,BBLUE)
	draw(game, "Arrow keys to move, Spacebar to fire", 50, width/2 -295 , height/2,BRED)
	draw(game, "Press any key", 35, width/2 -65,height*3/4, BGREEN)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYUP:
				waiting = False
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image= pygame.transform.scale(ship,(50,38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		#pygame.draw.circle(self.image, RED,self.rect.center,self.radius, 1)
		self.rect.centerx = width/2
		self.rect.bottom = height - 10
		self.speedx = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()
	
	def update(self):
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = width/2
			self.rect.bottom = height - 10
		self.speedx = 0
		k = pygame.key.get_pressed()
		if k[pygame.K_LEFT]:
			self.speedx = -8
		if k[pygame.K_RIGHT]:
			self.speedx = 8
		if k[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedx
		if self.rect.right -99 > width:
			self.rect.right = 0
		if  self.rect.left + 99< 0:
			self.rect.left = width 
		
	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)
			shoot_snd.play()
	
	def hide(self):
		self.hidden = True
		self.hide_timer= pygame.time.get_ticks()	
		self.rect.center = (width/2,height + 200)

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_img)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * .85/ 2)
		#pygame.draw.circle(self.image, RED, self.rect.center, self.radius,1)
		self.rect.x = random.randrange(0,width - self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(1, 8)
		self.speedx = random.randrange(-3,3)
		self.rot = 0	
		self.rotspeed = random.randrange(-8,8)
		self.t_update = pygame.time.get_ticks()	

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.t_update > 50 :
			self.t_update = now
			self.rot = (self.rot + self.rotspeed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)			
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center	
	
	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
			self.rect.x = random.randrange(width - self.rect.width)
			self.rect.y = random.randrange(-150,-100)
			self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bult
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect < 0 :
			self.kill()		

class explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explo_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 75
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explo_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explo_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


#loading Assets
	
bult = pygame.image.load(path.join(bullet_dir,"laserBlue01.png")).convert()
bground = pygame.image.load(path.join(img_dir,"background.jpg")).convert()
bground_rect = bground.get_rect()
ship = pygame.image.load(path.join(ship_dir,"ship.png")).convert()
mini_ship = pygame.image.load(path.join(ship_dir,"mini_ship.png")).convert()
mini_ship.set_colorkey(BLACK)
meteor_img = []
meteor_list = [ 'meteor1.png','meteor2.png','meteor3.png','meteor4.png','meteor5.png',
		'meteor6.png','meteor7.png','meteor8.png','meteor9.png','meteor10.png',
		'meteor11.png','meteor12.png','meteor13.png','meteor14.png','meteor15.png',
		'meteor16.png','meteor17.png','meteor18.png','meteor19.png','meteor20.png'
			]
for img in meteor_list :
	meteor_img.append(pygame.image.load(path.join(meteor_dir,img)).convert())

explo_anim = {}
explo_anim['lg'] = []
explo_anim['sm'] = []
explo_anim['player'] = []

for i in range(8) :
	filename = 'Explosion0{}.png'.format(i)
	img = pygame.image.load(path.join(meteor_exp_dir,filename)).convert()
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img, (75,75))
	explo_anim['lg'].append(img_lg)
	img_sm = pygame.transform.scale(img, (32,32))
	explo_anim['sm'].append(img_sm)
	filename = 'sExplosion0{}.png'.format(i)
	img = pygame.image.load(path.join(ship_exp_dir,filename)).convert()
	img.set_colorkey(BLACK)
	explo_anim['player'].append(img)

#loading sounds and music

shoot_snd = pygame.mixer.Sound(path.join(snd_dir,'shoot.wav'))
pygame.mixer.music.fadeout(2)
	
explo_snd = pygame.mixer.Sound(path.join(snd_dir,'explosion.wav'))
pygame.mixer.music.fadeout(5)

ship_explo_snd = pygame.mixer.Sound(path.join(snd_dir,'rumble1.ogg'))
	
pygame.mixer.music.load(path.join(snd_dir,'music.ogg'))
pygame.mixer.music.set_volume(1)
	
	
	
	
pygame.mixer.music.play()

game_over = True
running = True
while running :
	if game_over:
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		mobs = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		
		player = Player()
		all_sprites.add(player)
	
		for i in range(8):
			newmob()
	
		score = 0

	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				player.shoot()
			if event.key == pygame.K_ESCAPE:
				pause = True
				paused()
	
			
	all_sprites.update()
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
		
	for hit in hits :
		score += 50 - hit.radius
		explo_snd.play()	
		expl = explosion(hit.rect.center,'lg')
		all_sprites.add(expl)	
		newmob()
	   
	hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	
	for hit in hits :
		player.shield -= hit.radius * 2					
		expl = explosion(hit.rect.center,'sm')
		all_sprites.add(expl)	
		newmob()		
		if player.shield <= 0 :	
			ship_explo_snd.play()
			death_exp = explosion(player.rect.center, 'player')
			all_sprites.add(death_exp)	
			player.hide()
			player.lives -= 1
			player.shield = 100
				
	if player.lives == 0 and not death_exp.alive() :
		game_over = True
	
	#game.fill(BLACK)
	game.blit(bground, bground_rect)
	all_sprites.draw(game)
	draw(game, 'score ='+str(score),30,width-120,0,BGREEN)
	draw_shield(game, 5, 5, player.shield)
	draw_lives(game, 0, 20, player.lives, mini_ship)
	pygame.display.update()


pygame.quit()
quit()
