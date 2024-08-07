import pygame
import os
from src.tile import TILE_SIZE
import src.enemy as enemy
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
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos
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


class basic_enemy(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'basic_enemy16.png',
            'hit_bar_red.png',
            'hit_bar_green.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size

    def copy(self):
        ret = basic_enemy()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        self.images[2] = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            self.images[2],
            hit_bar_rect
        )


class evil_eye(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'evil_eye16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png',
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )
        self.size = size
        self.regenerate_shield_rate = 250

    def copy(self):
        ret = evil_eye()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit and self.shield == self.max_shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar_green = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size/2)
        )

        hit_bar_rect.centery += 9

        screen.blit(
            hit_bar_green,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar_blue = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size/2)
        )

        hit_bar_rect.centery -= TILE_SIZE/32

        screen.blit(
            hit_bar_blue,
            hit_bar_rect
        )


class high_armor(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'high_armor16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png',
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )
        self.size = size
        self.regenerate_shield_rate = 500

    def copy(self):
        ret = high_armor()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit and self.shield == self.max_shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar_green = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size/2)
        )

        hit_bar_rect.centery += 9

        screen.blit(
            hit_bar_green,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar_blue = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size/2)
        )

        hit_bar_rect.centery -= TILE_SIZE/32

        screen.blit(
            hit_bar_blue,
            hit_bar_rect
        )


class angry_basic(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'angry_basic16.png',
            'hit_bar_red.png',
            'hit_bar_green.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size

    def copy(self):
        ret = angry_basic()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        self.images[2] = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            self.images[2],
            hit_bar_rect
        )


class chaos_eye(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'chaos_eye16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png',
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )
        self.size = size
        self.regenerate_shield_rate = 200

    def copy(self):
        ret = chaos_eye()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit and self.shield == self.max_shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar_green = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size/2)
        )

        hit_bar_rect.centery += 9

        screen.blit(
            hit_bar_green,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar_blue = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size/2)
        )

        hit_bar_rect.centery -= TILE_SIZE/32

        screen.blit(
            hit_bar_blue,
            hit_bar_rect
        )


class super_shield(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'super_shield16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png',
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )
        self.size = size
        self.regenerate_shield_rate = 200

    def copy(self):
        ret = super_shield()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit and self.shield == self.max_shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar_green = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size/2)
        )

        hit_bar_rect.centery += 9

        screen.blit(
            hit_bar_green,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar_blue = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size/2)
        )

        hit_bar_rect.centery -= TILE_SIZE/32

        screen.blit(
            hit_bar_blue,
            hit_bar_rect
        )


class shielded_basic(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'shielded_basic16.png',
            'hit_bar_red.png',
            'hit_bar_green.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size

    def copy(self):
        ret = shielded_basic()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        self.images[2] = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            self.images[2],
            hit_bar_rect
        )


class storm_eye(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'storm_eye16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png',
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )
        self.size = size
        self.regenerate_shield_rate = 200

    def copy(self):
        ret = storm_eye()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit and self.shield == self.max_shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar_green = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size/2)
        )

        hit_bar_rect.centery += 9

        screen.blit(
            hit_bar_green,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar_blue = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size/2)
        )

        hit_bar_rect.centery -= TILE_SIZE/32

        screen.blit(
            hit_bar_blue,
            hit_bar_rect
        )

    def update(self, delta_time):
        ret = super().update(delta_time)
        self.regenerate_shield_time /= 5
        return ret


class ultra_shield(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/2
        width = TILE_SIZE/2
        height = TILE_SIZE/2
        pictures = [
            'ultra_shield16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png',
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )
        self.size = size
        self.regenerate_shield_rate = 1000

    def copy(self):
        ret = ultra_shield()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit and self.shield == self.max_shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar_green = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size/2)
        )

        hit_bar_rect.centery += 9

        screen.blit(
            hit_bar_green,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar_blue = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size/2)
        )

        hit_bar_rect.centery -= TILE_SIZE/32

        screen.blit(
            hit_bar_blue,
            hit_bar_rect
        )


class basic_boss(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/1.2
        width = TILE_SIZE/1.2
        height = TILE_SIZE/1.2
        pictures = [
            'angry_basic16.png',
            'hit_bar_red.png',
            'hit_bar_green.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size
        self.relative_pos = pygame.Vector2(0, 0)
        self.location = self.pos
        self.generate_time = 0
        self.generate_rate = 1500
        self.generated_unit = []
        self.dead = False

    def copy(self):
        ret = basic_boss()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        for en in self.generated_unit:
            en.display(screen)
        if self.hit <= 0:
            self.hit = 0
            return
        super().display(screen)
        if self.hit == self.max_hit:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

    def generate(self):
        for i in range(4):
            nen = angry_basic(self.pos.copy(), self.max_hit /
                              600, 0, 0, 90, self.path)
            nen.progress = self.progress
            self.generated_unit.append(nen)

    def update(self, delta_time):
        ret = super().update(delta_time)
        if self.generate_time > 0:
            self.generate_time -= delta_time
        else:
            self.generate()
            self.generate_time += self.generate_rate
        if self.hit <= 0 and len(self.generated_unit) <= 0:
            self.dead = True
        return ret


class eye_boss(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/1.2
        width = TILE_SIZE/1.2
        height = TILE_SIZE/1.2
        pictures = [
            'chaos_eye16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.regenerate_shield_rate = 250
        self.size = size
        self.relative_pos = pygame.Vector2(0, 0)
        self.location = self.pos
        self.generate_time = 0
        self.generate_rate = 0
        self.generated_unit = []
        self.dead = False

    def copy(self):
        ret = eye_boss()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        if self.hit <= 0:
            self.hit = 0
            return
        super().display(screen)
        if self.hit == self.max_hit and self.max_shield == self.shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

    def update(self, delta_time):
        ret = super().update(delta_time)
        if self.hit <= 0:
            self.dead = True
        return ret


class high_armor_boss(enemy):
    class armor_shield(enemy):
        def __init__(
            self, pos=pygame.Vector2(0, 0),
            hit=0, armor=0,
            shield=0, move_speed=0,
            path=[]
        ):
            size = TILE_SIZE/0.8
            width = TILE_SIZE/0.8
            height = TILE_SIZE/0.8
            pictures = [
                'high_armor_boss_shield.png'
            ]

            super().__init__(
                pos, width, height,
                pictures,
                hit, armor,
                shield, move_speed,
                path
            )

            self.size = size
            self.anti_pierce = 100
            self.relative_pos = pygame.Vector2(0, 0)
            self.location = self.pos

    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/1.2
        width = TILE_SIZE/1.2
        height = TILE_SIZE/1.2
        pictures = [
            'hyper_shield.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size
        self.relative_pos = pygame.Vector2(0, 0)
        self.location = self.pos
        self.generate_time = 0
        self.generate_rate = 800
        self.generated_unit = []
        self.dead = False

    def copy(self):
        ret = high_armor_boss()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        for en in self.generated_unit:
            en.display(screen)
        if self.hit <= 0:
            self.hit = 0
            return
        super().display(screen)
        if self.hit == self.max_hit and self.max_shield == self.shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

    def generate(self):
        nen = self.armor_shield(self.pos.copy(), 30, 30,
                                30, self.move_speed, self.path)
        nen.progress = self.progress
        self.generated_unit.append(nen)

    def update(self, delta_time):
        ret = super().update(delta_time)
        if self.generate_time > 0:
            self.generate_time -= delta_time
        else:
            self.generate()
            self.generate_time += self.generate_rate
        if self.hit <= 0:
            self.dead = True
        return ret


class shielded_basic_boss(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/1.2
        width = TILE_SIZE/1.2
        height = TILE_SIZE/1.2
        pictures = [
            'shielded_basic16.png',
            'hit_bar_red.png',
            'hit_bar_green.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size
        self.relative_pos = pygame.Vector2(0, 0)
        self.location = self.pos
        self.generate_time = 0
        self.generate_rate = 750
        self.generated_unit = []
        self.dead = False

    def copy(self):
        ret = shielded_basic_boss()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        for en in self.generated_unit:
            en.display(screen)
        if self.hit <= 0:
            self.hit = 0
            return
        super().display(screen)
        if self.hit == self.max_hit:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

    def generate(self):
        for i in range(6):
            nen = shielded_basic(
                self.pos.copy(), self.max_hit / 600, 0, 0, 90, self.path)
            nen.progress = self.progress
            self.generated_unit.append(nen)

    def update(self, delta_time):
        ret = super().update(delta_time)
        if self.generate_time > 0:
            self.generate_time -= delta_time
        else:
            self.generate()
            self.generate_time += self.generate_rate
        if self.hit <= 0 and len(self.generated_unit) <= 0:
            self.dead = True
        return ret


class storm_eye_boss(enemy):
    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/1.2
        width = TILE_SIZE/1.2
        height = TILE_SIZE/1.2
        pictures = [
            'storm_eye16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.regenerate_shield_rate = 250
        self.size = size
        self.relative_pos = pygame.Vector2(0, 0)
        self.location = self.pos
        self.generate_time = 0
        self.generate_rate = 0
        self.generated_unit = []
        self.dead = False

    def copy(self):
        ret = storm_eye_boss()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        if self.hit <= 0:
            self.hit = 0
            return
        super().display(screen)
        if self.hit == self.max_hit and self.max_shield == self.shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

    def update(self, delta_time):
        ret = super().update(delta_time)
        if self.hit <= 0:
            self.dead = True
        return ret


class ultra_high_armor_boss(enemy):
    class armor_shield(enemy):
        def __init__(
            self, pos=pygame.Vector2(0, 0),
            hit=0, armor=0,
            shield=0, move_speed=0,
            path=[]
        ):
            size = TILE_SIZE/0.8
            width = TILE_SIZE/0.8
            height = TILE_SIZE/0.8
            pictures = [
                'high_armor_boss_shield.png'
            ]

            super().__init__(
                pos, width, height,
                pictures,
                hit, armor,
                shield, move_speed,
                path
            )

            self.size = size
            self.anti_pierce = 100
            self.relative_pos = pygame.Vector2(0, 0)
            self.location = self.pos

    def __init__(
        self, pos=pygame.Vector2(0, 0),
        hit=0, armor=0,
        shield=0, move_speed=0,
        path=[]
    ):
        size = TILE_SIZE/1.2
        width = TILE_SIZE/1.2
        height = TILE_SIZE/1.2
        pictures = [
            'ultra_shield16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png'
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )

        self.size = size
        self.relative_pos = pygame.Vector2(0, 0)
        self.location = self.pos
        self.generate_time = 0
        self.generate_rate = 200
        self.generated_unit = []
        self.dead = False

    def copy(self):
        ret = ultra_high_armor_boss()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        for en in self.generated_unit:
            en.display(screen)
        if self.hit <= 0:
            self.hit = 0
            return
        super().display(screen)
        if self.hit == self.max_hit and self.max_shield == self.shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size)
        )

        screen.blit(
            hit_bar,
            hit_bar_rect
        )

    def generate(self):
        nen = self.armor_shield(self.pos.copy(), 30, 30,
                                30, self.move_speed, self.path)
        nen.progress = self.progress
        self.generated_unit.append(nen)

    def update(self, delta_time):
        ret = super().update(delta_time)
        if self.generate_time > 0:
            self.generate_time -= delta_time
        else:
            self.generate()
            self.generate_time += self.generate_rate
        if self.hit <= 0:
            self.dead = True
        return ret
