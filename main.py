import pygame
import time
import random

pygame.init()

window_width = 800		#display size
window_height = 600

ship_width = 99			#ship size
ship_height = 75		

a_width = 75			#asteroid size
a_height = 75

black = (0,0,0)
white = (255,255,255)

red = (150,0,0)
bred = (255,0,0)		#b = bright
green = (0,150,0)
bgreen = (0,255,0)
blue = (0,0,150)
bblue = (0,0,255)

yellow = (250,234,35)

game = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Dodging')


clock = pygame.time.Clock()

background = pygame.image.load('background.jpg')
asteroid = pygame.image.load('asteroid.png')
sshipimg = pygame.image.load('ship.png')


def buttons(msg,x,y,w,h,ic,ac,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y + h > mouse[1] > y  :		
		pygame.draw.rect(game, ac,[x,y,w,h])
		if click[0] ==1 and action != None:
			if action == "play":
				game_loop()
			elif action == "back":
				intro()
			elif action == "quit":
				pygame.quit()
				quit()
				
    else :	
		pygame.draw.rect(game, ic,[x,y,w,h])

    smalltxt = pygame.font.Font("freesansbold.ttf",25)
    txtsurf, txtrect = text_objects(msg, smalltxt,black)
    txtrect.center = ((x + (w/2)),(y + (h/2)))
    game.blit(txtsurf, txtrect)



def bullets(b1,b2,b3,b4,colour):
    pygame.draw.line(game, yellow, (b1,b2),(b3,b4),1)

def scorecard(count):			#scorecard count
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("SCORE: "+str(count), True, bgreen)
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

def hit():
    message_display('HIT')

def crash():
    message_display('You Crashed')

def intro():
	intro = True
	while True :
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					menu()
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		bground(0,0)
		Ltxt = pygame.font.Font('freesansbold.ttf',50)
		TextSurf, TextRect =text_objects("Space Dodging", Ltxt, bblue)
    		TextRect.center = ((window_width/2),(window_height/2))
    		game.blit(TextSurf, TextRect)

		Stxt = pygame.font.Font('freesansbold.ttf',20)
		TextSurf, TextRect =text_objects("Press spacebar to start", Stxt, bgreen)
		TextRect.center = ((window_width/2 + 10),(window_height/2 + 50))
		game.blit(TextSurf, TextRect)
		pygame.display.update()
		clock.tick(60)
def menu():
	menu = True
	while True :
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()		
		bground(0,0)
		buttons("START!",320,200,150,50,blue,bblue,"play")
		buttons("BACK",320,270,150,50,green,bgreen,"back")
		buttons("EXIT",320,340,150,50,red,bred,"quit")

		
		pygame.display.update()
		clock.tick(60)	
		

def game_loop():
    
    ax= random.randrange(0,window_width)
    ay=-200
    a_speed = 3

    x = (window_width * 0.45)
    y = (window_height * 0.8)

    x_change = 0
    y_change = 0

    b_1 = x + (ship_width/2)
    b_2 = y
    b_3 = x + (ship_width/2)
    b_4 = y + 10
    score = 0
    
    gameExit = False

    while not gameExit:
	  bground(0,0)
	  bullets(b_1,b_2,b_3,b_4,yellow)
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
		 elif event.key == pygame.K_SPACE:
		      bullets(x+ ship_width/2,y,x+ ship_width/2,y+10,yellow)
		 
              if event.type == pygame.KEYUP:
                 if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                 if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0

	  b_2 -= 3
	  b_4 -= 3
          x += x_change
          y += y_change
	  
          
	 
          pygame.draw.rect(game, black, [ax,ay,a_width,a_height],1)
	  
	  aroid(ax,ay)
	  ay += a_speed

	  scorecard(score)
        
	  pygame.draw.rect(game, green, [x,y,ship_width,ship_height],1)

    	  sship(x,y) 

	  pygame.draw.line(game, bred, (0,0),(800,0), 4)		#boundary..
	  pygame.draw.line(game, bred, (0,600),(800,600), 8)		#..lines


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

	  if b_4 < 0 :
	     b_1 =x +ship_width/2
	     b_3 =x +ship_width/2
	     b_2=y
	     b_4=y+10

	  if b_2 < ay + a_height - 5 and b_1 > ax and b_1 < ax + a_width - 5:	     
		hit()

	  if (y < (ay + a_height) and (y > ay)) or ((y + ship_height > ay) and (y + ship_height) < (ay + a_height)):
	     if x < ax and x > ax + a_width or x +ship_width > ax and x < ax + a_width:
		crash()

          pygame.display.update()
          clock.tick(60)

intro()
menu()
game_loop()
pygame.quit()
quit()
