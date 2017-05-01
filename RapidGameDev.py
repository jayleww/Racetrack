import pygame, math, sys
from pygame.locals import *
screen = pygame.display.set_mode((1024,768))
car = pygame.image.load('car.png')
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
speed = direction = 0
position = (100, 100)
turn_speed = 5
acceleration = 2
maxfspeed = 10
maxrspeed = -5
black = (0,0,0)

while 1:
    #USER INPUT
    clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event,'key'):
            continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT:
            k_right = down * -5
        elif event.key == K_LEFT:
            k_left = down * 5
        elif event.key == K_UP:
            k_up = down * 2
        elif event.key == K_DOWN:
            k_down = down * -2
        elif event.key == K_ESCAPE:
            sys.exit(0)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    screen.fill(black)

    #SIMULATION
    speed += (k_up + k_down)
    if speed > maxfspeed:
        speed = maxfspeed
    if speed < maxrspeed:
        speed = maxrspeed
    direction += (k_right + k_left)
    x,y = position
    rad = direction * math.pi/180
    x += -speed*math.sin(rad)
    y += -speed*math.cos(rad)
    position = (x,y)

    #RENDERING
    rotated = pygame.transform.rotate(car,direction)
    rect = rotated.get_rect()
    rect.center = position
    screen.blit(rotated,rect)
    pygame.display.flip()



