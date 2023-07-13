from typing import Any
from vec2D import vec2D
from vec2D import dis
import pygame
import os
from tile import TILE_SIZE
import math
import enemy
from button import button

def do_nothing() :
    return

def show_text(screen, text = '', x = 0, y = 0, color = (0, 0, 0), size = 0) :
    font=pygame.font.SysFont('unifont', size)
    text=font.render(text, True, color)
    textRect=text.get_rect()
    textRect.topleft=(x-10, y-20)
    screen.blit(text, textRect)

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
        self.upgrade_damage = button(
            'damage', vec2D(950, 84), [0, 0, 0], 
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_range = button(
            'range', vec2D(950, 109), [0, 0, 0], 
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_reload = button(
            'reload', vec2D(950, 134), [0, 0, 0], 
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_bullet_speed = button(
            'bullet_speed', vec2D(950, 159), [0, 0, 0], 
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.damage_level = 0
        self.range_level = 0
        self.reload_level = 0
        self.bullet_speed_level = 0
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos
        
    def detect_mouse(self, pos = vec2D(0, 0)) :
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
        def __init__(self, pos = vec2D(0, 0), velocity = vec2D(0, 0), damage = 0, images = []) :
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
            self.damage = damage
        def move(self, delta_time) :
            self.pos += self.velocity * (delta_time/1000.0)
        def display(self, screen) :
            self.rect.center = self.pos.get_tuple()
            screen.blit(
                self.images[self.state], 
                self.rect
            )

        def deal_damage(self, enemy) :
            self.pierce -= 1
            # damage dealing formula hasn't finished
            enemy.hit -= self.damage
            enemy.check_state()
        def detect(self, enemys = []) :
            for enemy in enemys :
                if self.pierce <= 0 :
                    break
                if dis(enemy.pos, self.pos) < (self.size+enemy.size)/2 :
                    self.deal_damage(enemy)
            if(
                self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x > TILE_SIZE*12 or
                self.pos.y > TILE_SIZE*9
            ) :
                self.pierce = 0

    def __init__(
        self, pos = vec2D(0, 0)
    ) :
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['basic_tower16.png', 'basic_tower_barrel.png', 'basic_tower_bullet.png']
        damage = 10
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
    def display_bullets(self, screen) :
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
        bullet = self.bullet(
            self.location.copy(), vec2D(0, 0), 
            self.damage, [self.images[2]]
        )
        bullet.velocity.set_angle(self.angle, self.bullet_speed)
        # print(bullet.velocity.get_tuple())
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
        self.shoot(enemys)
        for bullet in self.bullets :
            bullet.move(delta_time)
            bullet.detect(enemys)
        for bullet in self.bullets :
            if bullet.pierce <= 0 :
                self.bullets.remove(bullet)
        
    def display_info(self, screen, natural_ingot) :
        show_text(
            screen, 
            'Damage : {:.2f}'.format(self.damage), 
            790, 100, [0, 0, 0], 20
        )
        show_text(
            screen, 
            'Range  : {:.5f}'.format(self.range/TILE_SIZE), 
            790, 125, [0, 0, 0], 20
        )
        show_text(
            screen, 
            'Reload : {:.2f}'.format(self.reload), 
            790, 150, [0, 0, 0], 20
        )
        show_text(
            screen, 
            'Bspeed : {:.5f}'.format(self.bullet_speed/TILE_SIZE), 
            790, 175, [0, 0, 0], 20
        )

        show_text(
            screen, 
            'Level', 
            790, 220, [0, 0, 0], 20
        )

        show_text(
            screen, 
            'Damage : {}'.format(self.damage_level), 
            790, 250, [0, 0, 0], 20
        )
        if self.range_level > 1e15 :
            text = 'Range : max'
        else :
            text = 'Range : {}'.format(self.range_level)
        show_text(
            screen, text, 
            790, 275, [0, 0, 0], 20
        )
        if self.reload_level > 1e15 :
            text = 'Reload : max'
        else :
            text = 'Reload : {}'.format(self.reload_level)
        show_text(
            screen, text, 
            790, 300, [0, 0, 0], 20
        )
        if self.bullet_speed_level > 1e15 :
            text = 'Bullet Speed : max'
        else :
            text = 'Bullet Speed : {}'.format(self.bullet_speed_level)
        show_text(
            screen, text, 
            790, 325, [0, 0, 0], 20
        )


        if natural_ingot >= 50 + (self.damage_level+1)*10 :
            self.upgrade_damage.state = 0
        else :
            self.upgrade_damage.state = 1
        self.upgrade_damage.display(screen)
        if natural_ingot >= 50 + (self.range_level+1)*10 :
            self.upgrade_range.state = 0
        else :
            self.upgrade_range.state = 1
        self.upgrade_range.display(screen)
        if natural_ingot >= 50 + (self.reload_level+1)*10 :
            self.upgrade_reload.state = 0
        else :
            self.upgrade_reload.state = 1
        self.upgrade_reload.display(screen)
        if natural_ingot >= 50 + (self.bullet_speed_level+1)*10 :
            self.upgrade_bullet_speed.state = 0
        else :
            self.upgrade_bullet_speed.state = 1
        self.upgrade_bullet_speed.display(screen)
    def upgrade(self, mouse_pos = vec2D(0, 0), natural_ingot = 0) :
        if self.upgrade_damage.click(mouse_pos) :
            if natural_ingot >= 50 + (self.damage_level+1)*10 :
                self.damage_level += 1
                natural_ingot -= 50 + self.damage_level*10
                self.damage += 10.0 * math.sqrt(self.damage_level)
        elif self.upgrade_range.click(mouse_pos) :
            if natural_ingot >= 50 + (self.range_level+1)*10 :
                self.range_level += 1
                natural_ingot -= 50 + self.range_level*10
                self.range += TILE_SIZE/2 * 1/self.range_level
                if self.range > 5 * TILE_SIZE :
                    self.range = 5 * TILE_SIZE
                    self.range_level = 1e20
        elif self.upgrade_reload.click(mouse_pos) :
            if natural_ingot >= 50 + (self.reload_level+1)*10 :
                self.reload_level += 1
                natural_ingot -= 50 + self.reload_level*10
                self.reload += 3 * math.log10(self.reload_level*2)
                if self.reload > 60 :
                    self.reload = 60
                    self.reload_level = 1e20
        elif self.upgrade_bullet_speed.click(mouse_pos) :
            if natural_ingot >= 50 + (self.bullet_speed_level+1)*10 :
                self.bullet_speed_level += 1
                natural_ingot -= 50 + self.bullet_speed_level*10
                self.bullet_speed += TILE_SIZE * 1/self.bullet_speed_level
                if self.bullet_speed > 10 * TILE_SIZE :
                    self.bullet_speed = 10 * TILE_SIZE
                    self.bullet_speed_level = 1e20
        else :
            return [False, natural_ingot]
        return [True, natural_ingot]