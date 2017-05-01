import pygame, math, sys
from pygame.locals import *
width, height = 1024, 768
screen = pygame.display.set_mode((width,height))
car = pygame.image.load('car.png')
clock = pygame.time.Clock()
position = (100, 100)
black = (0,0,0)


class CarSprite(pygame.sprite.Sprite):
    turn_speed = 5
    acceleration = 4
    maxfspeed = 20
    maxrspeed = -5

    def __init__(self,image,position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed = self.direction = 0
        self.k_left = self.k_right = self.k_down = self.k_up = 0

    def update(self, deltat):
        self.speed += (self.k_up + self.k_down)
        if self.speed > self.maxfspeed:
            self.speed = self.maxfspeed
        if self.speed < self.maxrspeed:
            self.speed = self.maxrspeed
        self.direction += (self.k_right + self.k_left)
        x,y = self.position
        rad = self.direction * math.pi/180
        x += -self.speed*math.sin(rad)
        y += -self.speed*math.cos(rad)
        self.position = (x,y)
        self.image = pygame.transform.rotate(self.src_image,self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('padnormal.png')
    hit = pygame.image.load('padhit.png')

    def __init__(self,number, position):
        pygame.sprite.Sprite.__init__(self)
        self.number = number
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position
        self.image = self.normal

    def update(self, hit_list):
        if self in hit_list:
            self.image = self.hit
        else:
            self.image = self.normal


pads = [
    PadSprite(1,(200,200)),
    PadSprite(2,(800,200)),
    PadSprite(4,(200,600)),
    PadSprite(3,(800,600)),
    ]

current_pad_number = 0
pad_group = pygame.sprite.RenderPlain(*pads)
background = pygame.image.load('track.png')
background = pygame.transform.scale(background, (width, height))
rect = screen.get_rect()
car = CarSprite('car.png', rect.center)
screen.blit(background, (0,0))
car_group = pygame.sprite.RenderPlain(car)
while 1:
    #screen.fill(0)
    #USER INPUT
    deltat = clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if not hasattr(event,'key'):
            continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT:
            car.k_right = down * -5
        elif event.key == K_LEFT:
            car.k_left = down * 5
        elif event.key == K_UP:
            car.k_up = down * 2
        elif event.key == K_DOWN:
            car.k_down = down * -2
        elif event.key == K_ESCAPE:
            sys.exit(0)

    #RENDERING
    pad_group.clear(screen,background)
    car_group.clear(screen,background)
    car_group.update(deltat)
    car_group.draw(screen)
    pads = pygame.sprite.spritecollide(car,pad_group,0)
    if pads:
        pad = pads[0]
        if pad.number == current_pad_number + 1:
            pad.image = pad.hit
            current_pad_number += 1
        elif current_pad_number == 4:
            for pad in pad_group.sprites():
                pad.image = pad.normal
                current_pad_number = 0
    #pad_group.update(pads)
    pad_group.draw(screen)
    pygame.display.flip()
    



