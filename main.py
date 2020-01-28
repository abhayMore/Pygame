import pygame
import time
import random

pygame.init()

window_width = 800
window_height = 600
ship_width = 99
ship_height = 75

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

game = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Space Dodging')


clock = pygame.time.Clock()

sshipimg = pygame.image.load('ship.png')

def scorecard(count):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("SCORE: "+str(count), True, green)
    game.blit(text,(650,0))

def objects(objx, objy, objw, objh, colour):
    pygame.draw.rect(game, colour, [objx, objy, objw, objh])

def sship(x,y):
    game.blit(sshipimg,(x,y))

def text_objects(text, font):
    txtSurface = font.render(text, True, red)
    return txtSurface, txtSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect =text_objects(text, largeText)
    TextRect.center = ((window_width/2),(window_height/2))
    game.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

    game_loop()

def crash():
    message_display('You Crashed')

def game_loop():
    x = (window_width * 0.45)
    y = (window_height * 0.8)

    x_change = 0
    y_change= 0

    obj_y = -600
    obj_x = random.randrange(0, window_width )
    obj_speed = 7
    obj_width = 100
    obj_height = 100
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

          game.fill(white)

          #objects(objx, objy, objw, objh, colour):
          objects(obj_x, obj_y, obj_width, obj_height, black)
          obj_y +=obj_speed

          scorecard(score)
          sship(x,y)

          if x + ship_width < 0 :
             x = window_width
          if x > window_width :
             x= 0 - ship_width
          if y < 0 or y + ship_height > window_height:
             crash()
          if obj_y > window_height :
             obj_y = 0 - obj_height
             obj_x = random.randrange(0,window_width)
             score += 1
             obj_speed += 0.5

          if y < obj_y+obj_height:
             if ((obj_x) < x) and ((obj_x + obj_width) > x ) or ((x+ship_width) > (obj_x)) and ((x+ship_width) < (obj_x + obj_width)):
                crash()

          pygame.display.update()
          clock.tick(60)

game_loop()
pygame.quit()
quit()
