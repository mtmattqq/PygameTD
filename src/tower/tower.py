import pygame
from typing import Any
import os
from src.tile import TILE_SIZE
import math
from src.button import button

def do_nothing():
    return

def show_text(screen, text='', x=0, y=0, color=(0, 0, 0), size=0):
    font = pygame.font.Font(os.path.join(
        os.getcwd(), 'AppData', 'unifont.ttf'), size)
    text = font.render(text, True, color)
    textRect = text.get_rect()
    textRect.topleft = (x-10, y-20)
    screen.blit(text, textRect)

class tower(pygame.sprite.Sprite):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        width=TILE_SIZE, height=TILE_SIZE,
        pictures=[''],
        damage=0, reload=0,
        range=0, bullet_speed=0,
        volume=100
    ):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.location = self.pos*TILE_SIZE + \
            pygame.Vector2(TILE_SIZE/2, TILE_SIZE/2)
        self.height = height
        self.width = width
        self.placed = False
        self.selected = False
        self.damage = damage
        self.reload = reload
        self.range = range
        self.bullet_speed = bullet_speed
        self.time_to_fire = 0
        self.volume = volume
        self.images = []
        for picture in pictures:
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(), 'AppData', picture)).convert_alpha(), (width, height)))
        self.state = 0
        self.deconstruct_button = button(
            "decontruct", pygame.Vector2(805, 490), [0, 0, 0],
            32, 32, ['decontruct_button.png']
        )
        self.explode_sound = None

    def detect_mouse(self, pos=pygame.Vector2(0, 0)):
        self_pos = self.pos*TILE_SIZE
        if (
            pos.x < self_pos.x+self.width and
            pos.x > self_pos.x and
            pos.y < self_pos.y+self.height and
            pos.y > self_pos.y
        ):
            return True
        return False

    def action_onclick(self):
        self.selected = True

    def click(self, pos=pygame.Vector2(0, 0)):
        if (self.detect(pos)):
            return self.action_onclick()
        else:
            self.selected = False

    def place(self, pos=pygame.Vector2(0, 0)):
        self.pos = pos
        self.placed = True

    def aim_first(self, enemys=[], boss=None):
        first_enemy = None
        for enemy in enemys:
            if (
                (first_enemy == None or
                 enemy.progress > first_enemy.progress) and
                self.location.distance_to(enemy.location) < self.range
            ):
                first_enemy = enemy
        if boss != None:
            for enemy in boss.generated_unit:
                if (
                    (first_enemy == None or
                     enemy.progress > first_enemy.progress) and
                    self.location.distance_to(enemy.location) < self.range
                ):
                    first_enemy = enemy
            if (
                (first_enemy == None or
                 boss.progress > first_enemy.progress) and
                self.location.distance_to(boss.location) < self.range
            ):
                first_enemy = boss
        # print((first_enemy.pos - self.location))
        if first_enemy == None:
            return False

        relation = first_enemy.location - self.location
        self.angle = math.atan2(relation.y, relation.x)
        self.angle = -math.degrees(self.angle)
        return True

    def shoot(self, enemys=[], boss=None):
        ret = self.aim_first(enemys, boss)
        if self.time_to_fire <= 0 and ret:
            if self.target == 'first':
                if self.shoot_first(enemys, boss) != None:
                    self.time_to_fire += 1000.0/self.reload
                    self.fire_sound.play()
        return ret

    def display_bullets(self, screen):
        for bullet in self.bullets:
            bullet.display(screen)

    def display(self, screen):
        screen.blit(
            self.images[self.state],
            (self.pos*TILE_SIZE)
        )
        barrel = pygame.transform.rotozoom(self.images[1], self.angle, 1)
        rotated_rect = barrel.get_rect(center=(self.pos*TILE_SIZE))
        dw = rotated_rect.width - self.images[0].get_rect().width
        dw /= 2
        rotated_rect.centerx -= dw
        rotated_rect.centery -= dw
        screen.blit(
            barrel,
            rotated_rect.center
        )

    def display_info(self, screen):
        self.deconstruct_button.display(screen)
    
    def update(self, delta_time, enemys=[], boss=None):
        self.update_time_to_fire(delta_time)
        self.shoot(enemys, boss)
        for bullet in self.bullets:
            bullet.move(delta_time)
            bullet.detect(enemys, boss)
        for bullet in self.bullets:
            if bullet.pierce <= 0:
                self.bullets.remove(bullet)
                return True
        return False

    def update_time_to_fire(self, delta_time=0):
        if self.time_to_fire > 0:
            self.time_to_fire -= delta_time