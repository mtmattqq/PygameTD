import pygame
import os


def do_nothing():
    return True

# For class button, the pos is the position on screen


class button:
    def __init__(
        self, text="click me", pos=pygame.vector2(0, 0),
        color=[0, 0, 0], width=0, height=0,
        pictures=[''], action_onclick=do_nothing,
        action_highlight=do_nothing
    ):
        # pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.pos = pos
        self.color = color
        self.height = height
        self.width = width
        self.action_onclick = action_onclick
        self.action_highlight = action_highlight
        self.highlight = False
        self.selected = False
        self.images = []
        for picture in pictures:
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(), 'AppData', picture)).convert_alpha(), (width, height)))
        self.state = 0
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos

    def detect(self, pos=pygame.vector2(0, 0)):
        if (
            pos.x < self.pos.x+self.width and
            pos.x > self.pos.x and
            pos.y < self.pos.y+self.height and
            pos.y > self.pos.y
        ):
            if self.action_highlight != None:
                self.action_highlight()
            self.highlight = True
            return True
        self.highlight = False
        return False

    def click(self, pos=pygame.vector2(0, 0)):
        if (self.detect(pos)):
            return self.action_onclick()

    def display(self, screen):
        screen.blit(self.images[self.state], self.pos.get_tuple())
