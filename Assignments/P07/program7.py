from quadTree import *
import pygame
from random import randint 

import os
  
# Get the size
# of the terminal
size = os.get_terminal_size()

x,y = size
x *= 12
y *= 12
size = (x,y)
print(x,y)


pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('QuadTree')
radius = 3

def genPoints(bbox, x=100):
    points  = []
    for p in range(x):
        x = randint(radius,bbox.w-radius)
        y = randint(radius,bbox.h-radius)
        points.append(Point(x,y))
    return points

def highlightPoints(foundPoints):
    for p in foundPoints:
        pygame.draw.circle(screen,(255,255,0),[p.x,p.y],radius+3)


if __name__=='__main__':

    print((size[0]//2,size[1]//2,size[0],size[1]))

    bbox = Rect(size[0]//2,size[1]//2,size[0],size[1])
    
    qt = QuadTree(bbox)

    points = genPoints(bbox,100)

    nw = (size[0]//4,size[1]//4,size[0]//2,size[1]//2)

    for p in points:
        qt.insert(p);

    foundPoints = []
    
    
    rectWidth = 50
    prevy=0 
    # creating a bool value which checks
    # if game is running
    running = True
    r = pygame.Rect(0,0,rectWidth,rectWidth)
    # Game loop
    # keep game running till running is true
    while running:
        
        screen.fill((255,255,255))
        

        qt.draw(screen,radius)
        highlightPoints(foundPoints)
        
        
        pygame.draw.rect(screen,(0,0,0), r, 3)

        for event in pygame.event.get():
          if event.type == pygame.MOUSEBUTTONDOWN:
            rx,ry=pygame.mouse.get_pos()
            mouserect= pygame.Rect(rx,ry,100,100)
            pygame.draw.rect(screen,(0,0,0),mouserect , 3)
            for p in points: 
              if mouserect.collidepoint(p.x,p.y):
               pygame.draw.circle(screen,(255,255,0),[p.x,p.y],radius+3)
          if event.type == pygame.KEYDOWN:
                # if press the left arrow key.
                if event.key == pygame.K_a:
                  r = pygame.Rect.move(r,-10,0)
                if event.key == pygame.K_d:
                  r = pygame.Rect.move(r,10,0)      
                if event.key == pygame.K_w:
                  r = pygame.Rect.move(r,0,-10)
                if event.key == pygame.K_s:
                  r = pygame.Rect.move(r,0,10)
          if event.type == pygame.QUIT:
              running = False

            
        for p in points:      
           if r.collidepoint(p.x,p.y):
             pygame.draw.circle(screen,(255,255,0),[p.x,p.y],radius+3)


        pygame.display.flip()
