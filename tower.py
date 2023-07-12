from typing import Any
from vec2D import vec2D
from vec2D import dis
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
        width = TILE_SIZE, height = TILE_SIZE, 
        pictures = [''],
        damage = 0, reload = 0,
        range = 0, bullet_speed = 0
    ) :
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.location = self.pos*TILE_SIZE + vec2D(TILE_SIZE/2, TILE_SIZE/2)
        self.height = height
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
                os.path.join(os.getcwd(),'AppData',picture)).convert_alpha(), (width,height)))
        self.state = 0
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos
        
    def detect(self, pos = vec2D(0, 0)) :
        self_pos = self.pos*TILE_SIZE
        if(
            pos.x<self_pos.x+self.width and 
            pos.x>self_pos.x and 
            pos.y<self_pos.y+self.height and 
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
        def __init__(self, pos = vec2D(0, 0), velocity = vec2D(0, 0), images = []) :
            self.pierce = 1
            self.pos = pos
            self.velocity = velocity
            self.images = images
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = TILE_SIZE
            self.rect.height = TILE_SIZE
            self.rect.center = self.pos.get_tuple()
            self.state = 0
            self.size = TILE_SIZE/8
        def move(self, delta_time) :
            self.pos += self.velocity * (delta_time/1000.0)
        def display(self, screen) :
            self.rect.center = self.pos.get_tuple()
            screen.blit(
                self.images[self.state], 
                self.rect
            )
        def detect(self, enemys = []) :
            for enemy in enemys :
                if dis(enemy.pos, self.pos) < self.size :
                    a=0
        
    def __init__(
        self, pos = vec2D(0, 0)
    ) :
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['basic_tower16.png', 'basic_tower_barrel.png', 'basic_tower_bullet.png']
        damage = 1
        reload = 3
        range = 1.5*TILE_SIZE
        bullet_speed = 4*TILE_SIZE
        super().__init__(
            pos, width, height, 
            pictures,
            damage, reload,
            range, bullet_speed
        )
        self.aim = vec2D(0, 1)
        self.angle = 0
        self.bullets = []
        self.target = 'first'
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

        for bullet in self.bullets :
            bullet.display(screen)

    def aim_first(self, enemys = []) :
        first_enemy = None
        for enemy in enemys :
            if(
                (first_enemy == None or
                enemy.progress > first_enemy.progress) and
                dis(self.location, enemy.pos) < self.range
            ) :
                first_enemy = enemy
        # print((first_enemy.pos - self.location).get_tuple())
        if first_enemy == None :
            return False
        
        relation = first_enemy.pos - self.location
        self.angle = math.atan2(relation.y, relation.x)
        self.angle = -math.degrees(self.angle)
        return True
    
    def shoot_first(self, enemys = []) :
        if not self.aim_first(enemys) : 
            return False
        bullet = self.bullet(self.location.copy(), vec2D(0, 0), [self.images[2]])
        bullet.velocity.set_angle(self.angle, self.bullet_speed)
        print(bullet.velocity.get_tuple())
        self.bullets.append(bullet)
        return True
    
    def update_time_to_fire(self, delta_time = 0) :
        if self.time_to_fire > 0 :
            self.time_to_fire -= delta_time

    def shoot(self, enemys = []) :
        if self.target == 'first' :
            if self.time_to_fire <= 0 :
                if self.shoot_first(enemys) :
                    self.time_to_fire += 1000.0/self.reload
            else :
                self.aim_first(enemys)
    def update(self, delta_time, enemys = []) :
        self.update_time_to_fire(delta_time)
        for bullet in self.bullets :
            bullet.move(delta_time)
            bullet.detect(enemys)