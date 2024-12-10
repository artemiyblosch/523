import pygame
import sys
from random import randint

def generate_at(x_b):
    if randint(0,10) == 1:
        return Block(x_b,(y_b:=randint(0,350)),randint(200,600)+x_b,y_b+randint(50,100))
    if randint(0,10) == 1:
        return Block(x_b,(y_b:=randint(0,350)),25+x_b,y_b+randint(150,250))
    return Block(x_b,(y_b:=randint(0,350)),randint(50,200)+x_b,y_b+randint(50,150))

class Block:
    def __init__(self,x_b,y_b,x_e,y_e):
        self.x_b = x_b
        self.y_b = y_b
        self.x_e = x_e
        self.y_e = y_e
    
    def collide(self,player_y):
        return self.x_b<100<self.x_e and self.y_b<player_y<self.y_e

    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),\
            pygame.Rect(self.x_b,self.y_b,self.x_e - self.x_b,self.y_e - self.y_b))

pygame.init()

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

hardmode = True
fps = 360
player_y = 200
velocity = -100/fps
blocks = [generate_at(400+200*i) for i in range(20 if hardmode else 10)]

on_ground = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            velocity = 100/fps
        if event.type == pygame.KEYUP:
            velocity = -100/fps
    
    player_y += velocity
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,400,400),0)
    pygame.draw.polygon(screen,(0,0,0),[(95,player_y-5),(105,player_y),(95,player_y+5)])

    for index,i in enumerate(blocks):
        i.x_b -= 100/fps
        i.x_e -= 100/fps
        i.draw(screen)
        if i.x_e < 0 and hardmode == False:
            m = max([i.x_e for i in blocks])
            blocks = blocks[0:index]+blocks[index+1:]+[generate_at(m+50 if m+50 > 400 else 400)]
        elif i.x_e < 0:
            blocks = blocks[0:index]+blocks[index+1:]+[generate_at(400)]
        
        if i.collide(player_y):
            pygame.quit()
            sys.exit()

    if player_y < 5:
        player_y = 5
        on_ground += 1/fps
    elif player_y > 395: 
        player_y = 395
        on_ground += 1/fps
    
    if on_ground >= (0.75 if hardmode else 1.5):
        blocks.append(Block(450,0,1450,25))
        blocks.append(Block(450,375,1450,400))
        on_ground = 0

    pygame.display.flip()
    clock.tick(fps)
