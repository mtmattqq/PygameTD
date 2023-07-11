from vec2D import vec2D
import pygame
import os

def do_nothing() :
    return

class tower(pygame.sprite.Sprite) :
    def __init__(
        self, pos = vec2D(0, 0),
        width = 0, hight = 0, 
        pictures = [''],
        damage = 0, reload = 0
    ) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.hight = hight
        self.width = width
        self.placed = False
        self.selected = False
        self.images = []
        for picture in pictures :
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(),'AppData',picture)).convert_alpha(), (width,hight)))
        self.state = 0
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos
        
    def detect(self, pos = vec2D(0, 0)) :
        if(
            pos.x<self.pos.x+self.width and 
            pos.x>self.pos.x and 
            pos.y<self.pos.y+self.hight and 
            pos.y>self.pos.y
        ) :
            return True
        return False
    
    def action_onclick(self) :
        self.selected = True

    def click(self, pos = vec2D(0, 0)) :
        if(self.detect(pos)) :
            return self.action_onclick()
        else :
            self.selected = False

    def place(self, pos = vec2D(0, 0)) :
        self.pos = pos
        self.placed = True

    def display(self, screen) :
        screen.blit(self.images[self.state], self.pos.get_tuple())

class basic_tower(tower) :
    def __init__() :
        tower.__init__()