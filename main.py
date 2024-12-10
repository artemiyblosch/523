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

pygame.font.init()
pygame.init()

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font1 = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 12)

hardmode = False
slope = -1
fps = 360
player_y = 200
velocity = -100/fps*slope
blocks = [generate_at(400+200*i) for i in range(20 if hardmode else 10)]
menu_mode = True

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
        velocity = 100/fps*slope
    else:
        velocity = -100/fps*slope
    if menu_mode and k[pygame.K_h]:
        hardmode = not hardmode
    elif menu_mode and k[pygame.K_RETURN]: menu_mode = False
    
    if menu_mode:
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,400,400),0)
        screen.blit(title,titleRect)
        hm = font2.render(f"Hardmode(H to toggle): {hardmode}", False, (255,255,255))
        hmRect = title.get_rect()
        hmRect.center = (200,150)
        screen.blit(hm,hmRect)
        pygame.display.flip()
        continue

    player_y += velocity
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,400,400),0)
    if velocity == 0:
        pygame.draw.polygon(screen,(0,0,0),[(95,player_y-5),(105,player_y),(95,player_y+5)])
    elif velocity > 0:
        pygame.draw.polygon(screen,(0,0,0),[(92,player_y+3),(98,player_y - 3),(95+7,player_y+7)])
    elif velocity < 0:
        pygame.draw.polygon(screen,(0,0,0),[(92,player_y-3),(95+7,player_y - 7),(98,player_y+3)])
    
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

    if player_y <= 5:
        player_y = 5
        on_ground += 1/fps
        velocity = 0
    elif player_y >= 395: 
        player_y = 395
        on_ground += 1/fps
        velocity = 0
    
    if on_ground >= (0.75 if hardmode else 1.5):
        blocks.append(Block(450,0,1450,25))
        blocks.append(Block(450,375,1450,400))
        on_ground = 0

    pygame.display.flip()
    clock.tick(fps)
