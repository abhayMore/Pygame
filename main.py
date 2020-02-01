
#music by onky Hardmoon / Arjen Schumacher
#art by kenny
import pygame
import random
import time
from os import path

img_dir = path.join(path.dirname(__file__),'Assets','Images')
snd_dir = path.join(path.dirname(__file__),'Assets','Music')



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
pygame.display.set_caption("SPACE DOSDGING")
clock = pygame.time.Clock()


def buttons(msg,x,y,w,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y + h > mouse[1] > y  :		
		pygame.draw.rect(game, ac,[x,y,w,h])
		if click[0] ==1 and action != None:
			if action == "cplay":
				unpause()		
			elif action == "play":
				menu = False
				game_loop()
			elif action == "back":
				intro()
			elif action == "quit":
				pygame.quit()
				quit()
			elif action == "nplay":
				game_loop()
    else :	
		pygame.draw.rect(game, ic,[x,y,w,h])

    smalltxt = pygame.font.Font("freesansbold.ttf",25)
    txtsurf, txtrect = text_objects(msg, smalltxt,BLACK)
    txtrect.center = ((x + (w/2)),(y + (h/2)))
    game.blit(txtsurf, txtrect)


def text_objects(text, font,color):
    txtSurface = font.render(text, True, color)
    return txtSurface, txtSurface.get_rect()

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
	
	def update(self):
		self.speedx = 0
		k = pygame.key.get_pressed()
		if k[pygame.K_LEFT]:
			self.speedx = -8
		elif k[pygame.K_RIGHT]:
			self.speedx = 8
		self.rect.x += self.speedx
		if self.rect.right -99 > width:
			self.rect.right = 0
		elif  self.rect.left + 99< 0:
			self.rect.left = width 
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


		
#loading Assets
	
bground = pygame.image.load(path.join(img_dir,"background.jpg")).convert()
bground_rect = bground.get_rect()
ship = pygame.image.load(path.join(img_dir,"ship.png")).convert()
meteor_img = []
meteor_list = [ 'meteor1.png','meteor2.png','meteor3.png','meteor4.png','meteor5.png',
		'meteor6.png','meteor7.png','meteor8.png','meteor9.png','meteor10.png',
		'meteor11.png','meteor12.png','meteor13.png','meteor14.png','meteor15.png',
		'meteor16.png','meteor17.png','meteor18.png','meteor19.png','meteor20.png'
			]
for img in meteor_list :
	meteor_img.append(pygame.image.load(path.join(img_dir,img)).convert())


#loading sounds and music

shoot_snd = pygame.mixer.Sound(path.join(snd_dir,'shoot.wav'))
pygame.mixer.music.fadeout(2)
	
explo_snd = pygame.mixer.Sound(path.join(snd_dir,'explosion.wav'))
pygame.mixer.music.fadeout(5)
	
pygame.mixer.music.load(path.join(snd_dir,'music.ogg'))
pygame.mixer.music.set_volume(1)
	
	
	
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
	
player = Player()
all_sprites.add(player)
	
for i in range(8):
	newmob()
pause = True

def unpause():
	global pause
	pause = False

def paused():
	while pause :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()		
		game.blit(bground, bground_rect)	
		buttons("PAUSED",320,130,150,50,WHITE,WHITE,"")
		buttons("CONTINUE!",320,200,150,50,WHITE,WHITE,"cplay")
		buttons("START!",320,270,150,50,BLUE,BBLUE,"nplay")
		buttons("BACK",320,340,150,50,GREEN,BGREEN,"back")
		buttons("EXIT",320,410,150,50,RED,BRED,"quit")

		
		pygame.display.update()
		clock.tick(60)

def intro():
	intro = True
	while intro :
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					intro = False					
					menu()
					
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		game.blit(bground, bground_rect)
		draw(game,' Space Dodging',80,width/4,height/4, BBLUE)
		draw(game,' Press Spacebar to continue',40,width/4 + 25,height/3+80,BRED)		
		pygame.display.update()
		clock.tick(60)

def menu():
	menu = True
	while True :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()		
		game.blit(bground, bground_rect)		
		buttons("START!",320,200,150,50,BLUE,BBLUE,"play")
		buttons("BACK",320,270,150,50,GREEN,BGREEN,"back")
		buttons("EXIT",320,340,150,50,RED,BRED,"quit")

		
		pygame.display.update()
		clock.tick(60)	

def game_loop():	
	score = 0
	global pause
	
	pygame.mixer.music.play()
	running = True
	while running :
	
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					player.shoot()
				elif event.key == pygame.K_ESCAPE:
					pause = True
					paused()
	
			
		all_sprites.update()
		hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
		
		for hit in hits :
			score += 50 - hit.radius
			explo_snd.play()		
			newmob()
	   
		hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
	
		for hit in hits :
			player.shield -= hit.radius * 2
			newmob()		
			if player.shield <= 0 :		
				menu()
	
		#game.fill(BLACK)
		game.blit(bground, bground_rect)
		all_sprites.draw(game)
		draw(game, 'score ='+str(score),30,width-120,0,BGREEN)
		draw_shield(game, 5, 5, player.shield)
		pygame.display.update()
intro()
menu()
game_loop()	
pygame.quit()
quit()
