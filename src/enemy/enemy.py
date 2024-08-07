import pygame
import os
from src.tile import TILE_SIZE
from src.enemy import *
import random

class enemy:
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        width=0, height=0,
        pictures=[''],
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        # pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.relative_pos = pygame.Vector2(
            random.randint(-15, 15), random.randint(-15, 15))
        self.location = pos + self.relative_pos
        self.height = height
        self.width = width
        self.hit = hit
        self.max_hit = hit
        self.armor = armor
        self.shield = shield
        self.max_shield = shield
        self.regenerate_shield_time = 0
        self.regenerate_shield_rate = 1000
        self.move_speed = move_speed
        self.velocity = pygame.Vector2(0, 0)
        self.progress = 0
        self.alive = True
        self.path = path
        self.anti_pierce = 1
        self.max_progress = len(path)
        self.images = []
        self.pictures = pictures
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.rect.width = width
        self.rect.height = height
        self.rect.center = self.pos
        for picture in pictures:
            self.images.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(), 'AppData', picture)).convert_alpha(), (width, height)))
        self.state = 0
        self.is_slowed = 0

    def copy(self):
        ret = enemy(
            self.pos, self.width,
            self.height, self.pictures,
            self.hit, self.armor,
            self.shield, self.move_speed,
            self.path
        )
        return ret

    def detect(self, pos=pygame.Vector2(0, 0)):
        self_pos = self.pos*TILE_SIZE
        if (
            pos.x < self_pos.x+self.width and
            pos.x > self_pos.x and
            pos.y < self_pos.y+self.height and
            pos.y > self_pos.y
        ):
            return True
        return False

    def display(self, screen):
        self.rect.center = self.location
        screen.blit(
            self.images[self.state],
            self.rect
        )

    def check_state(self):
        if self.hit <= 0:
            self.alive = False
        return self.alive

    def move(self, delta_time):
        if self.progress >= self.max_progress-1:
            # deal damage to player's main tower
            self.alive = False
            return True
        self.velocity = self.path[self.progress + 1] - self.pos
        self.velocity = self.velocity.normalize() * self.move_speed if self.velocity.length() != 0 else pygame.Vector2(0, 0)
        # print(self.velocity)
        if (
            (self.path[self.progress + 1] - self.pos).distance_to(pygame.Vector2(0, 0)) <=
            (self.velocity * (delta_time/1000)).distance_to(pygame.Vector2(0, 0))
        ):
            self.pos = self.path[self.progress + 1].copy()
            self.progress += 1
        else:
            self.pos += self.velocity * (delta_time/1000)
        self.location = self.pos + self.relative_pos
        return False

    def update(self, delta_time):
        if self.regenerate_shield_time > 0:
            self.regenerate_shield_time -= delta_time
        if self.regenerate_shield_time <= 0 and self.shield < self.max_shield:
            self.shield = min(self.shield + 0.1 *
                              self.max_shield, self.max_shield)
            self.regenerate_shield_time += self.regenerate_shield_rate
        return self.move(delta_time)