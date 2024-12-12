from objects import *
from random import randint

on_ground = 0

def update_level(objects,hardmode,screen,fps):
    global on_ground
    player = objects[0]
    if player.y <= 5:
        player.y = 5
        player.vslope = 0
        on_ground += 1/fps
        player.yvel = 0
    elif player.y >= 395: 
        player.y = 395
        player.vslope = 0
        on_ground += 1/fps
        player.yvel = 0
    
    
    k = pygame.key.get_pressed()
    if k[pygame.K_SPACE] or k[pygame.K_UP]:
        player.slope = 1
        player.yvel = -100/fps*player.slope
    else:
        player.slope = -1
        player.yvel = -100/fps*player.slope

    if on_ground >= (0.75 if hardmode else 1.5):
        objects.append(Block(450,0,1450,25,100))
        objects.append(Block(450,375,1450,400,100))
        on_ground = 0
    
    player.y += player.yvel
    player.draw(screen)
    player.update_slope()

    i,keep_going = 1,True
    while i < len(objects):
        objects[i].draw(screen)
        obj = objects[i]

        if isinstance(obj,Block) and obj.x_e < 0 and obj.speed > 0:
            m = max([j.x_e for j in objects if isinstance(j,Block)])
            m += randint(-10,25) if hardmode else randint(25,50)
            objects = objects[:i] + objects[i+1:] + (generate_at(m if m > 400 else 400,hardmode) if obj.respawn else [])
            continue
        elif isinstance(obj,Block) and obj.x_b > 400 and obj.speed < 0:
            m = max([j.x_e for j in objects if isinstance(j,Block)])
            m += randint(-10,25) if hardmode else randint(25,50)
            objects = objects[:i] + objects[i+1:] + (generate_at(m if m > 400 else 400,hardmode) if obj.respawn else [])
            continue
        elif isinstance(obj,Block):
            obj.x_e -= obj.speed/fps
            obj.x_b -= obj.speed/fps
            if obj.collide(player): keep_going = False
        
        i+=1
        
    return objects, keep_going
        

def generate_at(pos,hardmode):
    if randint(0,4 if hardmode else 7) == 1:
        pos = -pos + 400
        return [Block(pos - randint(50,200),(y_b:=randint(0,350)),pos,y_b+randint(50,150),randint(-120 if hardmode else -80,-60))]
    if randint(0,10) == 1:
        return [Block(pos,(y_b:=randint(0,350)),randint(200,600)+pos,y_b+randint(50,100),randint(80, 150 if hardmode else 100))]
    if randint(0,10) == 1:
        return [Block(pos,(y_b:=randint(0,350)),25+pos,y_b+randint(150,250),randint(80, 150 if hardmode else 100))]
    if randint(0,20) == 1 and hardmode:
        a = [Block(pos,(y_b:=randint(0,350)),50+pos,y_b+50,randint(300,500)) for i in range(randint(2,4))]
        for i in a[1:]:
            i.respawn = False
        return a
    return [Block(pos,(y_b:=randint(0,350)),randint(50,200)+pos,y_b+randint(50,150),randint(80, 150 if hardmode else 100))]