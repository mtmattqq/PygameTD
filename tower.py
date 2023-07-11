from vec2D import vec2D
import pygame
import os
from tile import TILE_SIZE
import math
import enemy

def do_nothing() :
    return

class tower(pygame.sprite.Sprite) :
    def __init__(
        self, pos = vec2D(0, 0),
        width = TILE_SIZE, hight = TILE_SIZE, 
        pictures = [''],
        damage = 0, reload = 0,
        range = 0, bullet_speed = 0
    ) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.location = self.pos*TILE_SIZE + vec2D(TILE_SIZE/2, TILE_SIZE/2)
        self.hight = hight
        self.width = width
        self.placed = False
        self.selected = False
        self.damage = damage
        self.reload = reload
        self.range = range
        self.bullet_speed = bullet_speed
        self.time_to_fire = 0
        self.images = []
        for picture in pictures :
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(),'AppData',picture)).convert_alpha(), (width,hight)))
        self.state = 0
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos
        
    def detect(self, pos = vec2D(0, 0)) :
        self_pos = self.pos*TILE_SIZE
        if(
            pos.x<self_pos.x+self.width and 
            pos.x>self_pos.x and 
            pos.y<self_pos.y+self.hight and 
            pos.y>self_pos.y
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
        screen.blit(
            self.images[self.state], 
            (self.pos*TILE_SIZE).get_tuple()
        )

class basic_tower(tower) :
    class bullet :
        def __init__(self, velocity = vec2D(0, 0)) :
            self.pierce = 1
            self.pos = vec2D(0, 0)
            self.velocity = velocity

        
    def __init__(
        self, pos = vec2D(0, 0),
        width = TILE_SIZE, hight = TILE_SIZE, 
        pictures = ['basic_tower16.png', 'basic_tower_barrel.png'],
        damage = 1, reload = 3,
        range = 1.5*TILE_SIZE, bullet_speed = 1
    ) :
        
        super().__init__(
            pos, width, hight, 
            pictures,
            damage, reload,
            range, bullet_speed
        )
        self.aim = vec2D(0, 1)
        self.angle = 0
        self.bullets = []
    def display(self, screen):
        super().display(screen)
        barrel = pygame.transform.rotozoom(self.images[1],self.angle, 1)
        rotated_rect = barrel.get_rect(center = (self.pos*TILE_SIZE).get_tuple())
        dw = rotated_rect.width - self.images[0].get_rect().width
        dw /= 2
        rotated_rect.centerx -= dw
        rotated_rect.centery -= dw
        screen.blit(
            barrel, 
            rotated_rect.center
        )

    def aim_first(self, enemys = []) :
        first_enemy = enemys[0]
        for enemy in enemys :
            if enemy.progress > first_enemy.progress :
                first_enemy = enemy
        relation = first_enemy.pos - self.location
        self.angle = math.atan2(relation.y/relation.x)
    
    def shoot_first(self, enemys = []) :
        self.aim_first(enemys)
        bullet = self.bullet()
        bullet.velocity = vec2D(0, 0).set_angle(self.angle, self.bullet_speed)
        self.bullets.append(bullet)
    
    def update_time_to_fire(self, delta_time = 0) :
        self.time_to_fire -= delta_time
        self.time_to_fire = max(0, self.time_to_fire)