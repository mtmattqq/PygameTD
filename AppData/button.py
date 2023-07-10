import vec2D as vec
import pygame
import os

def __init__(self,pos=(0,0),picture=''):
        pygame.sprite.Sprite.__init__(self)
        # 要改成相對路徑(finished by excellent77)
        self.image=pygame.image.load(os.path.join(os.getcwd(),picture))
        # self.image=pygame.transform.scale(self.image,(20,20))
        self.rect=self.image.get_rect()
        self.rect.center=pos

class Button(pygame.sprite.Sprite) :
    def __init__(
            self, text = "click me", pos = vec.vec2D(0, 0),
            color = [0,0,0], hight = 0, width = 0, 
            picture = '') :
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.pos = pos
        self.color = color
        self.hight = hight
        self.width = width
        self.image = pygame.image.load(
            os.path.join(os.getcwd(),picture))
        self.image = pygame.transform.scale(self.image,(width,hight))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
    def detect(self, pos = vec.vec2D(0, 0)) :
        if(     pos.x<self.pos.x+self.width and 
                pos.x>self.pos.x and pos.y<self.hight and 
                pos.y>self.pos.y) :
            return True
        return False