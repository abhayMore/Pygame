import pygame
import time
import random

pygame.init()

window_width = 800
window_height = 600

ship_width = 99
ship_height = 75

a_width = 75
a_height = 75

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

game = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Dodging')


clock = pygame.time.Clock()

background = pygame.image.load('background.jpg')
asteroid = pygame.image.load('asteroid.png')
sshipimg = pygame.image.load('ship.png')

def scorecard(count):			#scorecard count
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("SCORE: "+str(count), True, green)
    game.blit(text,(650,0))

def bground(a,b):			#background image
	game.blit(background,(a,b))

def aroid(ax,ay):			#asteroid image
	game.blit(asteroid,(ax,ay))
	
def sship(x,y):				#spaceship image
    game.blit(sshipimg,(x,y))

def text_objects(text, font,color):
    txtSurface = font.render(text, True, color)
    return txtSurface, txtSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect =text_objects(text, largeText, red)
    TextRect.center = ((window_width/2),(window_height/2))
    game.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

    game_loop()

def crash():
    message_display('You Crashed')

def intro():
	intro = True
	while True :
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					game_loop()
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		bground(0,0)
		Ltxt = pygame.font.Font('freesansbold.ttf',50)
		TextSurf, TextRect =text_objects("Space Dodging", Ltxt, blue)
    		TextRect.center = ((window_width/2),(window_height/2))
    		game.blit(TextSurf, TextRect)

		Stxt = pygame.font.Font('freesansbold.ttf',20)
		TextSurf, TextRect =text_objects("Press spacebar to start", Stxt, green)
		TextRect.center = ((window_width/2 + 10),(window_height/2 + 50))
		game.blit(TextSurf, TextRect)
		pygame.display.update()
		clock.tick(10)
		

def game_loop():
    
    ax= random.randrange(0,window_width)
    ay=-200
    a_speed = 5

    x = (window_width * 0.45)
    y = (window_height * 0.8)

    x_change = 0
    y_change= 0

    score = 0
    
    gameExit = False

    while not gameExit:
          for event in pygame.event.get():
              if event.type==pygame.QUIT:
                 pygame.quit()
                 quit()
              if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_LEFT:
                    x_change = -5
                 elif event.key == pygame.K_RIGHT:
                      x_change = 5
                 elif event.key == pygame.K_DOWN:
                      y_change = 5
                 elif event.key == pygame.K_UP:
                      y_change = -5
              if event.type == pygame.KEYUP:
                 if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                 if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0


          x += x_change
          y += y_change
	  
          bground(0,0)
	 
          pygame.draw.rect(game, black, [ax,ay,a_width,a_height],1)
	  aroid(ax,ay)
	  ay += a_speed

	  scorecard(score)
        
	  pygame.draw.rect(game, green, [x,y,ship_width,ship_height],1)
          sship(x,y) 

	  pygame.draw.line(game, red, (0,0),(800,0), 4)
	  pygame.draw.line(game, red, (0,600),(800,600), 8)


          if x + ship_width < 0 :
             x = window_width

          if x > window_width :
             x= 0 - ship_width

          if y < 0 or y + ship_height > window_height:
             crash()
	  
	  if ay > window_height:
	     ay = -10
	     ax= random.randrange(0,window_width)
	     score += 1

          if (y < (ay + a_height) and (y > ay)) or ((y + ship_height > ay) and (y + ship_height) < (ay + a_height)):
	     if x < ax and x > ax + a_width or x +ship_width > ax and x < ax + a_width:
		crash()

          pygame.display.update()
          clock.tick(60)

intro()
game_loop()
pygame.quit()
quit()
