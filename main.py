import pygame
import sys
from random import randint
import math

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
    
    def collide(self,player):
        return self.x_b<player.x<self.x_e and self.y_b<player.y<self.y_e

    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),\
            pygame.Rect(self.x_b,self.y_b,self.x_e - self.x_b,self.y_e - self.y_b))

class Player:
    def __init__(self,slope,x,y):
        self.x = x
        self.y = y
        self.slope = slope
        self.vslope = slope
    
    def update_slope(self):
        self.vslope = self.slope

    def draw(self,screen):
        points = [(-5,-5),(5,0),(-5,5)]
        angle = math.atan(self.vslope)
        points  = [(math.cos(angle)*i[0] + math.sin(angle)*i[1], -math.sin(angle)*i[0] + math.cos(angle)*i[1]) for i in points]
        points = [(i[0]+self.x,i[1]+self.y) for i in points]
        pygame.draw.polygon(screen,(0,0,0),points)

pygame.font.init()
pygame.init()

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font1 = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 12)

hardmode = False
fps = 360
player = Player(-1,100,200)
velocity = -100/fps*player.slope
blocks = [generate_at(400+100*i) for i in range(20 if hardmode else 10)]
menu_mode = True
hardmode_cooldown = 0
fps_cooldown = 0

title = font1.render("523.py", False, (255,255,255))
titleRect = title.get_rect()
titleRect.center = (200,50)

on_ground = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    k = pygame.key.get_pressed()
    if k[pygame.K_SPACE] or k[pygame.K_UP]:
        player.slope = 1
        velocity = -100/fps*player.slope
    else:
        player.slope = -1
        velocity = -100/fps*player.slope
    
    if k[pygame.K_ESCAPE] and not menu_mode: 
        hardmode = False
        fps = 360
        player = Player(-1,100,200)
        velocity = -100/fps*player.slope
        blocks = [generate_at(400+200*i) for i in range(20 if hardmode else 10)]
        menu_mode = True

    if menu_mode and k[pygame.K_h] and hardmode_cooldown < 0:
        hardmode = not hardmode
        hardmode_cooldown = fps
    elif menu_mode and k[pygame.K_RETURN]: menu_mode = False
    elif menu_mode and k[pygame.K_w] and fps_cooldown < 0: 
        fps += 1
        fps_cooldown = fps / 4
    elif menu_mode and k[pygame.K_s] and fps_cooldown < 0: 
        fps = max(fps - 1, 1)
        fps_cooldown = fps / 4
    
    if menu_mode:
        hardmode_cooldown -= 1
        fps_cooldown -= 1
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,400,400),0)
        screen.blit(title,titleRect)
        hm = font2.render(f"Hardmode(H to toggle): {hardmode}", False, (255,255,255))
        hmRect = hm.get_rect()
        hmRect.center = (200,150)
        screen.blit(hm,hmRect)
        fm = font2.render(f"FPS(W to increase,S to decrease): {fps}", False, (255,255,255))
        fmRect = fm.get_rect()
        fmRect.center = (200,200)
        screen.blit(fm,fmRect)
        pygame.display.flip()
        continue

    player.y += velocity
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,400,400),0)

    player.draw(screen)
    player.update_slope()

    for index,i in enumerate(blocks):
        i.x_b -= 100/fps
        i.x_e -= 100/fps
        i.draw(screen)
        if i.x_e < 0 and hardmode == False:
            m = max([i.x_e for i in blocks])
            blocks = blocks[0:index]+blocks[index+1:]+[generate_at(m+50 if m+50 > 400 else 400)]
        elif i.x_e < 0:
            blocks = blocks[0:index]+blocks[index+1:]+[generate_at(400)]
        
        if i.collide(player):
            hardmode = False
            fps = 360
            player = Player(-1,100,200)
            velocity = -100/fps*player.slope
            blocks = [generate_at(400+200*i) for i in range(20 if hardmode else 10)]
            menu_mode = True

    if player.y <= 5:
        player.y = 5
        player.vslope = 0
        on_ground += 1/fps
        velocity = 0
    elif player.y >= 395: 
        player.y = 395
        player.vslope = 0
        on_ground += 1/fps
        velocity = 0
    
    if on_ground >= (0.75 if hardmode else 1.5):
        blocks.append(Block(450,0,1450,25))
        blocks.append(Block(450,375,1450,400))
        on_ground = 0

    pygame.display.flip()
    clock.tick(fps)
