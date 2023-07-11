from vec2D import vec2D
import pygame
import os

def do_nothing() :
    return

class button(pygame.sprite.Sprite) :
    def __init__(
            self, text = "click me", pos = vec2D(0, 0),
            color = [0,0,0], hight = 0, width = 0, 
            pictures = [''], action_onclick = do_nothing(), 
            action_highlight = do_nothing()) :
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.pos = pos
        self.color = color
        self.hight = hight
        self.width = width
        self.action_onclick = action_onclick
        self.action_highlight = action_highlight
        self.highlight = False
        self.selected = False
        self.images = []
        for picture in pictures :
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(),'AppData',picture)), (width,hight)))
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
            if self.action_highlight != None:
                self.action_highlight()
            self.highlight = True
            return True
        self.highlight = False
        return False
    
    def click(self, pos = vec2D(0, 0)) :
        if(self.detect(pos)) :
            return self.action_onclick()

    def display(self, screen) :
        screen.blit(self.images[self.state], self.pos.get_tuple())