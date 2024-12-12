import math
import pygame

class RectObject:
    def __init__(self,x_b,y_b,x_e,y_e):
        self.x_b = x_b
        self.y_b = y_b
        self.x_e = x_e
        self.y_e = y_e
    
    def collide(self,other):
        if isinstance(other,RectObject):
            return (other.x_b<=self.x_b<=other.x_e or other.x_b<=self.x_e<=other.x_e\
                   or self.x_b<=other.x_b<=self.x_e or self.x_b<=other.x_e<=self.x_e) and \
                   (other.y_b<=self.y_b<=other.y_e or other.y_b<=self.y_e<=other.y_e\
                   or self.y_b<=other.y_b<=self.y_e or self.y_b<=other.y_e<=self.y_e)
        elif isinstance(other,PointObject):
            return self.x_b<other.x<self.x_e and self.y_b<other.y<self.y_e

class PointObject:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def collide(self,other):
        if isinstance(other,PointObject):
            return (self.x, self.y) == (other.x,other.y)
        elif isinstance(other,RectObject):
            return other.x_b<self.x<other.x_e and other.y_b<self.y<other.y_e

class Player(PointObject):
    def __init__(self,slope,x,y,yvel):
        super().__init__(x,y)
        self.slope = slope
        self.vslope = slope
        self.yvel = yvel
    
    def update_slope(self):
        self.vslope = self.slope

    def draw(self,screen):
        points = [(-5,-5),(5,0),(-5,5)]
        angle = math.atan(self.vslope)
        points  = [(math.cos(angle)*i[0] + math.sin(angle)*i[1], -math.sin(angle)*i[0] + math.cos(angle)*i[1]) for i in points]
        points = [(i[0]+self.x,i[1]+self.y) for i in points]
        pygame.draw.polygon(screen,(0,0,0),points)

class Block(RectObject):
    def __init__(self, x_b, y_b, x_e, y_e, speed):
        super().__init__(x_b, y_b, x_e, y_e)
        self.speed = speed
        self.respawn = True

    def draw(self,screen):
        pygame.draw.rect(screen,(0,0,0),\
            pygame.Rect(self.x_b,self.y_b,self.x_e - self.x_b,self.y_e - self.y_b))