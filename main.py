import pygame
import sys
from random import randint
from level import *
import math
from objects import *

def init():
    global hardmode, menu_mode,fps,keep_going
    hardmode = False
    fps = 360
    menu_mode = True
    keep_going = True

pygame.font.init()
pygame.init()

def flat(xss):
    return [x for xs in xss for x in xs]

screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
font1 = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 12)

hardmode = False
fps = 360
objects = []
menu_mode = True
hardmode_cooldown = 0
keep_going = True
fps_cooldown = 0
init()

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
    if k[pygame.K_ESCAPE] or not keep_going: init()

    if menu_mode and k[pygame.K_h] and hardmode_cooldown < 0:
        hardmode = not hardmode
        hardmode_cooldown = fps
    elif menu_mode and k[pygame.K_RETURN]: 
        menu_mode = False
        objects = [Player(-1,100,200,0)] + flat([generate_at(400+(150 if hardmode else 200)*i, hardmode) for i in range(70 if hardmode else 40)])
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

    pygame.draw.rect(screen,(255,255,255),pygame.Rect(0,0,400,400),0)

    objects,keep_going = update_level(objects,hardmode,screen,fps)

    pygame.display.flip()
    clock.tick(fps)
