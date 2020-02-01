
#music by onky Hardmoon / Arjen Schumacher

import pygame
import random
import time
import os

width = 800
height = 600
FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

pygame.init() 
pygame.mixer.init()
game = pygame.display.set_mode((width,height))
pygame.display.set_caption("SPACE DOSDGING")
clock = pygame.time.Clock()


font_name =pygame.font.match_font('comic')
def draw(surf, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	txt_surface = font.render(text, True, GREEN)
	txt_rect =txt_surface.get_rect()
	txt_rect = (x,y)
	surf.blit(txt_surface,txt_rect)


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
	
	def update(self):
		self.speedx = 0
		k = pygame.key.get_pressed()
		if k[pygame.K_LEFT]:
			self.speedx = -8
		elif k[pygame.K_RIGHT]:
			self.speedx = 8
		self.rect.x += self.speedx
		if self.rect.right > width:
			self.rect.right = width
		elif  self.rect.left < 0:
			self.rect.left = 0
	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		shoot_snd.play()

class Mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_img)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width * 0.85/ 2)
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
		self.image = pygame.Surface((10,20))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		self.speedy = -10
	
	def update(self):
		self.rect.y += self.speedy
		if self.rect < 0 :
			self.kill()		
		
bground = pygame.image.load('background.jpg').convert()
bground_rect = bground.get_rect()
ship = pygame.image.load('ship.png').convert()
meteor_img = []
meteor_list = [ 'meteor1.png','meteor2.png','meteor3.png','meteor4.png','meteor5.png',
		'meteor6.png','meteor7.png','meteor8.png','meteor9.png','meteor10.png',
		'meteor11.png','meteor12.png','meteor13.png','meteor14.png','meteor15.png',
		'meteor16.png','meteor17.png','meteor18.png','meteor19.png','meteor20.png'
		]
for img in meteor_list :
	meteor_img.append(pygame.image.load(img).convert())

shoot_snd = pygame.mixer.Sound('shoot.wav')
pygame.mixer.music.fadeout(2)
explo_snd = pygame.mixer.Sound('explosion.wav')
pygame.mixer.music.fadeout(5)


pygame.mixer.music.load('music.ogg')
pygame.mixer.music.set_volume(1)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()

all_sprites.add(player)

for i in range(8):
	m = Mob()
	all_sprites.add(m)
	mobs.add(m)

score = 0

pygame.mixer.music.play()
running = True
while running :

	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()

		
	all_sprites.update()
	hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
	
	for hit in hits :
		score += 50 - hit.radius
		explo_snd.play()		
		m = Mob()
		all_sprites.add(m)
		mobs.add(m)


	hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)

	if hits :
		running = False

	game.fill(BLACK)
	game.blit(bground, bground_rect)
	all_sprites.draw(game)
	draw(game, 'score ='+str(score),30,0,0)
	pygame.display.flip()

pygame.quit()
quit()
