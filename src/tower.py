from typing import Any
import pygame
import os
from src.tile import TILE_SIZE
import math
import src.enemy as enemy
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
        # self.image = self.images[self.state]
        # self.rect = self.image.get_rect()
        # self.rect.topleft = pos

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

    def display(self, screen):
        screen.blit(
            self.images[self.state],
            (self.pos*TILE_SIZE)
        )

    def display_info(self, screen):
        self.deconstruct_button.display(screen)


class basic_tower(tower):
    class bullet:
        def __init__(self, pos=pygame.Vector2(0, 0), velocity=pygame.Vector2(0, 0), damage=0, images=[]):
            self.pierce = 1
            self.pos = pos
            self.velocity = velocity
            self.images = images
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = TILE_SIZE
            self.rect.height = TILE_SIZE
            self.rect.center = self.pos
            self.state = 0
            self.size = TILE_SIZE/8
            self.damage = damage

        def move(self, delta_time):
            self.pos += self.velocity * (delta_time/1000.0)

        def display(self, screen):
            self.rect.center = self.pos
            screen.blit(
                self.images[self.state],
                self.rect
            )

        def deal_damage(self, enemy):

            # damage dealing formula hasn't finished
            if enemy.shield > 0:
                enemy.shield = max(0, enemy.shield - self.damage)
                self.pierce -= enemy.anti_pierce
                return
            if self.pierce >= enemy.anti_pierce:
                enemy.hit -= max(self.damage/20,
                                 (1 - 19*enemy.armor/400) * self.damage)
            enemy.check_state()
            self.pierce -= enemy.anti_pierce

        def detect(self, enemys=[], boss=None):
            for enemy in enemys:
                if self.pierce <= 0:
                    return
                if enemy.location.distance_to(self.pos) < (self.size+enemy.size)/2:
                    self.deal_damage(enemy)
            if boss != None:
                if self.pierce <= 0:
                    return
                if boss.location.distance_to(self.pos) < (self.size+boss.size)/2:
                    self.deal_damage(boss)
                for enemy in boss.generated_unit:
                    if self.pierce <= 0:
                        return
                    if enemy.location.distance_to(self.pos) < (self.size+enemy.size)/2:
                        self.deal_damage(enemy)
            if (
                self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x > TILE_SIZE*12 or
                self.pos.y > TILE_SIZE*9
            ):
                self.pierce = 0

    def __init__(
        self, pos=pygame.Vector2(0, 0), volume=100
    ):
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['basic_tower16.png',
                    'basic_tower_barrel.png', 'basic_tower_bullet.png']
        damage = 10
        reload = 3
        range = 1.5*TILE_SIZE
        bullet_speed = 4*TILE_SIZE
        super().__init__(
            pos, width, height,
            pictures,
            damage, reload,
            range, bullet_speed,
            volume
        )
        self.aim = pygame.Vector2(0, 1)
        self.angle = 0
        self.bullets = []
        self.target = 'first'
        self.upgrade_damage = button(
            'damage', pygame.Vector2(1000, 84), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_range = button(
            'range', pygame.Vector2(1000, 109), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_reload = button(
            'reload', pygame.Vector2(1000, 134), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_bullet_speed = button(
            'bullet_speed', pygame.Vector2(1000, 159), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.damage_level = 0
        self.range_level = 0
        self.reload_level = 0
        self.bullet_speed_level = 0
        self.fire_sound = pygame.mixer.Sound(
            os.path.join(os.getcwd(), 'AppData', 'basic_tower_fire.wav')
        )
        self.fire_sound.set_volume(self.volume / 100)

    def display(self, screen):
        super().display(screen)
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

    def display_bullets(self, screen):
        for bullet in self.bullets:
            bullet.display(screen)

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
        if first_enemy == None:
            return False

        relation = first_enemy.location - self.location
        self.angle = math.atan2(relation.y, relation.x)
        self.angle = -math.degrees(self.angle)
        return True

    def shoot_first(self, enemys=[], boss=None):
        if not self.aim_first(enemys, boss):
            return False
        bullet = self.bullet(
            self.location.copy(), pygame.Vector2(0, 0),
            self.damage, [self.images[2]]
        )
        bullet.velocity.from_polar([self.bullet_speed, -self.angle])
        # print(bullet.velocity)
        self.bullets.append(bullet)
        return True

    def update_time_to_fire(self, delta_time=0):
        if self.time_to_fire > 0:
            self.time_to_fire -= delta_time

    def shoot(self, enemys=[], boss=None):
        if self.time_to_fire <= 0:
            if self.target == 'first':
                if self.shoot_first(enemys, boss):
                    self.time_to_fire += 1000.0/self.reload
                    self.fire_sound.play()
        else:
            self.aim_first(enemys, boss)

    def update(self, delta_time, enemys=[], boss=None):
        self.update_time_to_fire(delta_time)
        self.shoot(enemys, boss)
        for bullet in self.bullets:
            bullet.move(delta_time)
            bullet.detect(enemys, boss)
        for bullet in self.bullets:
            if bullet.pierce <= 0:
                self.bullets.remove(bullet)

    def display_info(self, screen, natural_ingot):
        super().display_info(screen)
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
        if self.range_level > 1e15:
            text = 'Range : max'
        else:
            text = 'Range : {}'.format(self.range_level)
        show_text(
            screen, text,
            790, 275, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(self.reload_level)
        show_text(
            screen, text,
            790, 300, [0, 0, 0], 20
        )
        if self.bullet_speed_level > 1e15:
            text = 'Bullet Speed : max'
        else:
            text = 'Bullet Speed : {}'.format(self.bullet_speed_level)
        show_text(
            screen, text,
            790, 325, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Cost',
            790, 370, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Damage : {}'.format(50 + 10*(self.damage_level+1)),
            790, 400, [0, 0, 0], 20
        )
        if self.range_level > 1e15:
            text = 'Range : max'
        else:
            text = 'Range : {}'.format(50 + 10*(self.range_level+1))
        show_text(
            screen, text,
            790, 425, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(50 + 10*(self.reload_level+1))
        show_text(
            screen, text,
            790, 450, [0, 0, 0], 20
        )
        if self.bullet_speed_level > 1e15:
            text = 'Bullet Speed : max'
        else:
            text = 'Bullet Speed : {}'.format(
                50 + 10*(self.bullet_speed_level+1))
        show_text(
            screen, text,
            790, 475, [0, 0, 0], 20
        )

        if natural_ingot >= 50 + (self.damage_level+1)*10:
            self.upgrade_damage.state = 0
        else:
            self.upgrade_damage.state = 1
        self.upgrade_damage.display(screen)
        if natural_ingot >= 50 + (self.range_level+1)*10:
            self.upgrade_range.state = 0
        else:
            self.upgrade_range.state = 1
        self.upgrade_range.display(screen)
        if natural_ingot >= 50 + (self.reload_level+1)*10:
            self.upgrade_reload.state = 0
        else:
            self.upgrade_reload.state = 1
        self.upgrade_reload.display(screen)
        if natural_ingot >= 50 + (self.bullet_speed_level+1)*10:
            self.upgrade_bullet_speed.state = 0
        else:
            self.upgrade_bullet_speed.state = 1
        self.upgrade_bullet_speed.display(screen)

    def upgrade(self, mouse_pos=pygame.Vector2(0, 0), natural_ingot=0):
        if self.upgrade_damage.click(mouse_pos):
            if natural_ingot >= 50 + (self.damage_level+1)*10:
                self.damage_level += 1
                natural_ingot -= 50 + self.damage_level*10
                self.damage += 10.0 * math.sqrt(self.damage_level)
        elif self.upgrade_range.click(mouse_pos):
            if natural_ingot >= 50 + (self.range_level+1)*10:
                self.range_level += 1
                natural_ingot -= 50 + self.range_level*10
                self.range += TILE_SIZE/2 * 1/self.range_level
                if self.range > 5 * TILE_SIZE:
                    self.range = 5 * TILE_SIZE
                    self.range_level = 1e20
        elif self.upgrade_reload.click(mouse_pos):
            if natural_ingot >= 50 + (self.reload_level+1)*10:
                self.reload_level += 1
                natural_ingot -= 50 + self.reload_level*10
                self.reload += 3 * 1/self.reload_level
                if self.reload > 60:
                    self.reload = 60
                    self.reload_level = 1e20
        elif self.upgrade_bullet_speed.click(mouse_pos):
            if natural_ingot >= 50 + (self.bullet_speed_level+1)*10:
                self.bullet_speed_level += 1
                natural_ingot -= 50 + self.bullet_speed_level*10
                self.bullet_speed += TILE_SIZE * 1/self.bullet_speed_level
                if self.bullet_speed > 10 * TILE_SIZE:
                    self.bullet_speed = 10 * TILE_SIZE
                    self.bullet_speed_level = 1e20
        else:
            return [False, natural_ingot]
        return [True, natural_ingot]


class sniper_tower(tower):
    class bullet:
        def __init__(
                self, pos=pygame.Vector2(0, 0),
                velocity=pygame.Vector2(0, 0),
                damage=0, hardness=0,
                pierce=0, images=[]
        ):
            self.pierce = pierce
            self.pos = pos
            self.velocity = velocity
            self.images = images
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = TILE_SIZE/2
            self.rect.height = TILE_SIZE/2
            self.rect.center = self.pos
            self.state = 0
            self.size = TILE_SIZE/2
            self.damage = damage
            self.hardness = hardness

        def move(self, delta_time):
            self.pos += self.velocity * (delta_time/1000.0)

        def display(self, screen):
            self.rect.center = self.pos
            screen.blit(
                self.images[self.state],
                self.rect
            )

        def deal_damage(self, enemy):
            self.pierce -= enemy.anti_pierce
            # damage dealing formula hasn't finished
            if enemy.shield > 0:
                enemy.shield = max(0, enemy.shield - self.damage)
                return
            enemy.hit -= max(self.damage/20,
                             (1 - 19*enemy.armor/400) * self.damage)
            enemy.armor -= self.hardness
            enemy.check_state()

        def detect(self, enemys=[], boss=None):
            for enemy in enemys:
                if self.pierce <= 0:
                    break
                if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                    self.deal_damage(enemy)
            if boss != None:
                if self.pierce <= 0:
                    return
                if self.pos.distance_to(boss.location) < (self.size+boss.size)/2:
                    self.deal_damage(boss)
                for enemy in boss.generated_unit:
                    if self.pierce <= 0:
                        return
                    if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                        self.deal_damage(enemy)
            if (
                self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x > TILE_SIZE*12 or
                self.pos.y > TILE_SIZE*9
            ):
                self.pierce = 0

    def __init__(
        self, pos=pygame.Vector2(0, 0), volume=100
    ):
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['sniper_tower16.png',
                    'sniper_tower_barrel.png', 'sniper_tower_bullet.png']
        damage = 50
        reload = 0.5
        range = 8*TILE_SIZE
        bullet_speed = 12*TILE_SIZE

        super().__init__(
            pos, width, height,
            pictures,
            damage, reload,
            range, bullet_speed,
            volume
        )
        self.images[2] = pygame.transform.scale(
            self.images[2], [TILE_SIZE/2, TILE_SIZE/2])
        self.aim = pygame.Vector2(0, 1)
        self.angle = 0
        self.bullets = []
        self.target = 'first'
        self.pierce = 2
        self.hardness = 1
        self.fire_sound = pygame.mixer.Sound(
            os.path.join(os.getcwd(), 'AppData', 'sniper_tower_fire.wav')
        )
        self.volume = volume
        self.fire_sound.set_volume(self.volume / 100)

        self.upgrade_damage = button(
            'damage', pygame.Vector2(1000, 84), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_hardness = button(
            'hardness', pygame.Vector2(1000, 109), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_reload = button(
            'reload', pygame.Vector2(1000, 134), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_pierce = button(
            'bullet_speed', pygame.Vector2(1000, 159), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.damage_level = 0
        self.hardness_level = 0
        self.reload_level = 0
        self.pierce_level = 0

    def display(self, screen):
        super().display(screen)
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

    def display_bullets(self, screen):
        for bullet in self.bullets:
            bullet.display(screen)

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

    def shoot_first(self, enemys=[], boss=None):
        if not self.aim_first(enemys, boss):
            return False
        bullet = self.bullet(
            self.location.copy(), pygame.Vector2(0, 0),
            self.damage, self.hardness,
            self.pierce, [self.images[2]]
        )
        bullet.velocity.from_polar([self.bullet_speed, -self.angle])
        # print(bullet.velocity)
        self.bullets.append(bullet)
        return True

    def update_time_to_fire(self, delta_time=0):
        if self.time_to_fire > 0:
            self.time_to_fire -= delta_time

    def shoot(self, enemys=[], boss=None):
        if self.time_to_fire <= 0:
            if self.target == 'first':
                if self.shoot_first(enemys, boss):
                    self.time_to_fire += 1000.0/self.reload
                    self.fire_sound.play()

        else:
            self.aim_first(enemys, boss)

    def update(self, delta_time, enemys=[], boss=None):
        self.update_time_to_fire(delta_time)
        self.shoot(enemys, boss)
        for bullet in self.bullets:
            bullet.move(delta_time)
            bullet.detect(enemys, boss)
        for bullet in self.bullets:
            if bullet.pierce <= 0:
                self.bullets.remove(bullet)

    def display_info(self, screen, natural_ingot):
        super().display_info(screen)
        show_text(
            screen,
            'Damage   : {:.2f}'.format(self.damage),
            790, 100, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Hardness : {:.5f}'.format(self.hardness),
            790, 125, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Reload   : {:.2f}'.format(self.reload),
            790, 150, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Pierce   : {}'.format(self.pierce),
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
        if self.hardness_level > 1e15:
            text = 'Hardness : max'
        else:
            text = 'Hardness : {}'.format(self.hardness_level)
        show_text(
            screen, text,
            790, 275, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(self.reload_level)
        show_text(
            screen, text,
            790, 300, [0, 0, 0], 20
        )
        if self.pierce_level > 1e15:
            text = 'Pierce : max'
        else:
            text = 'Pierce : {}'.format(self.pierce_level)
        show_text(
            screen, text,
            790, 325, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Cost',
            790, 370, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Damage : {}'.format(50 + 50*(self.damage_level+1)),
            790, 400, [0, 0, 0], 20
        )
        if self.hardness_level > 1e15:
            text = 'Hardness : max'
        else:
            text = 'Hardness : {}'.format(50 + 50*(self.hardness_level+1))
        show_text(
            screen, text,
            790, 425, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(50 + 50*(self.reload_level+1))
        show_text(
            screen, text,
            790, 450, [0, 0, 0], 20
        )
        if self.pierce_level > 1e15:
            text = 'Pierce : max'
        else:
            text = 'Pierce : {}'.format(100 * (2**(self.pierce_level+1)))
        show_text(
            screen, text,
            790, 475, [0, 0, 0], 20
        )

        if natural_ingot >= 50 + (self.damage_level+1)*50:
            self.upgrade_damage.state = 0
        else:
            self.upgrade_damage.state = 1
        self.upgrade_damage.display(screen)
        if natural_ingot >= 50 + (self.hardness_level+1)*50:
            self.upgrade_hardness.state = 0
        else:
            self.upgrade_hardness.state = 1
        self.upgrade_hardness.display(screen)
        if natural_ingot >= 50 + (self.reload_level+1)*50:
            self.upgrade_reload.state = 0
        else:
            self.upgrade_reload.state = 1
        self.upgrade_reload.display(screen)
        if (not self.pierce_level > 1e15) and natural_ingot >= 100 * (2 ** (self.pierce_level+1)):
            self.upgrade_pierce.state = 0
        else:
            self.upgrade_pierce.state = 1
        self.upgrade_pierce.display(screen)

    def upgrade(self, mouse_pos=pygame.Vector2(0, 0), natural_ingot=0):
        if self.upgrade_damage.click(mouse_pos):
            if natural_ingot >= 50 + (self.damage_level+1)*50:
                self.damage_level += 1
                natural_ingot -= 50 + self.damage_level*50
                self.damage += 50.0 * math.sqrt(self.damage_level)
        elif self.upgrade_hardness.click(mouse_pos):
            if natural_ingot >= 50 + (self.hardness_level+1)*50:
                self.hardness_level += 1
                natural_ingot -= 50 + self.hardness_level*50
                self.hardness += 3 * 1/self.hardness_level
                if self.hardness >= 20:
                    self.hardness = 20
                    self.hardness_level = 1e20
        elif self.upgrade_reload.click(mouse_pos):
            if natural_ingot >= 50 + (self.reload_level+1)*50:
                self.reload_level += 1
                natural_ingot -= 50 + self.reload_level*10
                self.reload += 0.2 * math.log10(self.reload_level*2)
                if self.reload >= 5:
                    self.reload = 5
                    self.reload_level = 1e20
        elif self.upgrade_pierce.click(mouse_pos):
            if (
                self.pierce_level < 1e15 and
                natural_ingot >= 100 * (2**(self.pierce_level+1))
            ):
                self.pierce_level += 1
                natural_ingot -= 100 * (2**self.pierce_level)
                self.pierce += 1
                if self.pierce >= 10:
                    self.pierce = 10
                    self.pierce_level = 1e20
        else:
            return [False, natural_ingot]
        return [True, natural_ingot]


class cannon_tower(tower):
    class bullet:
        def __init__(
            self, pos=pygame.Vector2(0, 0),
            velocity=pygame.Vector2(0, 0),
            damage=0, explode_range=0,
            images=[]
        ):
            self.pierce = 1
            self.pos = pos
            self.velocity = velocity
            self.images = images
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = TILE_SIZE/2
            self.rect.height = TILE_SIZE/2
            self.rect.center = self.pos
            self.state = 0
            self.size = TILE_SIZE/2
            self.damage = damage
            self.explode_range = explode_range

        def move(self, delta_time):
            self.pos += self.velocity * (delta_time/1000.0)

        def display(self, screen):
            self.rect.center = self.pos
            screen.blit(
                self.images[self.state],
                self.rect
            )

        def deal_damage(self, enemy):
            # damage dealing formula hasn't finished
            if enemy.shield > 0:
                enemy.shield = max(0, enemy.shield - self.damage)
            if self.pierce >= enemy.anti_pierce:
                armor = enemy.armor + math.log10(max(1, enemy.shield))
                enemy.hit -= max(self.damage/20,
                                 (1 - 19*armor/400) * self.damage)
            enemy.check_state()

        def detect(self, enemys=[], boss=None):
            crush = False
            if self.pierce <= 0:
                return crush
            for enemy in enemys:
                if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                    crush = True

            if boss != None:
                if self.pos.distance_to(boss.location) < (self.size+boss.size)/2:
                    crush = True
                for enemy in boss.generated_unit:
                    if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                        crush = True

            if crush:
                for enemy in enemys:
                    if self.pos.distance_to(enemy.location) < (self.explode_range+enemy.size)/2:
                        self.deal_damage(enemy)
                if boss != None:
                    if self.pos.distance_to(boss.location) < (self.explode_range+boss.size)/2:
                        crush = True
                        self.deal_damage(boss)
                    for enemy in boss.generated_unit:
                        if self.pos.distance_to(enemy.location) < (self.explode_range+enemy.size)/2:
                            self.deal_damage(enemy)
                self.pierce -= 1
            if (
                self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x > TILE_SIZE*12 or
                self.pos.y > TILE_SIZE*9
            ):
                self.pierce = 0
            return False

    def __init__(
        self, pos=pygame.Vector2(0, 0), volume=100
    ):
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['cannon_tower16.png',
                    'cannon_tower_barrel.png', 'cannon_tower_bullet.png']
        damage = 100
        reload = 1
        range = 2*TILE_SIZE
        bullet_speed = 2*TILE_SIZE
        super().__init__(
            pos, width, height,
            pictures,
            damage, reload,
            range, bullet_speed,
            volume
        )
        self.images[2] = pygame.transform.scale(
            self.images[2], [TILE_SIZE/2, TILE_SIZE/2])
        self.aim = pygame.Vector2(0, 1)
        self.angle = 0
        self.bullets = []
        self.target = 'first'
        self.explode_range = 1 * TILE_SIZE
        self.upgrade_damage = button(
            'damage', pygame.Vector2(1000, 84), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_explode_range = button(
            'range', pygame.Vector2(1000, 109), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_reload = button(
            'reload', pygame.Vector2(1000, 134), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_bullet_speed = button(
            'bullet_speed', pygame.Vector2(1000, 159), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.damage_level = 0
        self.explode_range_level = 0
        self.reload_level = 0
        self.bullet_speed_level = 0
        self.fire_sound = pygame.mixer.Sound(
            os.path.join(os.getcwd(), 'AppData', 'cannon_tower_fire.wav')
        )
        self.fire_sound.set_volume(self.volume / 100)
        self.explode_sound = pygame.mixer.Sound(
            os.path.join(os.getcwd(), 'AppData', 'cannon_tower_explode.wav')
        )
        self.explode_sound.set_volume(self.volume / 100)

    def display(self, screen):
        super().display(screen)
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

    def display_bullets(self, screen):
        for bullet in self.bullets:
            bullet.display(screen)

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
        if first_enemy == None:
            return False

        relation = first_enemy.pos - self.location
        self.angle = math.atan2(relation.y, relation.x)
        self.angle = -math.degrees(self.angle)
        return True

    def shoot_first(self, enemys=[], boss=None):
        if not self.aim_first(enemys, boss):
            return False
        bullet = self.bullet(
            self.location.copy(), pygame.Vector2(0, 0),
            self.damage, self.explode_range,
            [self.images[2]]
        )
        bullet.velocity.from_polar([self.bullet_speed, -self.angle])
        # print(bullet.velocity)
        self.bullets.append(bullet)
        return True

    def update_time_to_fire(self, delta_time=0):
        if self.time_to_fire > 0:
            self.time_to_fire -= delta_time

    def shoot(self, enemys=[], boss=None):
        if self.time_to_fire <= 0:
            if self.target == 'first':
                if self.shoot_first(enemys, boss):
                    self.time_to_fire += 1000.0/self.reload
                    self.fire_sound.play()

        else:
            self.aim_first(enemys, boss)

    def update(self, delta_time, enemys=[], boss=None):
        self.update_time_to_fire(delta_time)
        self.shoot(enemys, boss)
        for bullet in self.bullets:
            bullet.move(delta_time)
            bullet.detect(enemys, boss)
        for bullet in self.bullets:
            if bullet.pierce <= 0:
                self.bullets.remove(bullet)
                self.explode_sound.play()

    def display_info(self, screen, natural_ingot):
        super().display_info(screen)
        show_text(
            screen,
            'Damage : {:.2f}'.format(self.damage),
            790, 100, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Explode Range : {:.4f}'.format(self.explode_range/TILE_SIZE),
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
        if self.explode_range_level > 1e15:
            text = 'Explode Range : max'
        else:
            text = 'Explode Range : {}'.format(self.explode_range_level)
        show_text(
            screen, text,
            790, 275, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(self.reload_level)
        show_text(
            screen, text,
            790, 300, [0, 0, 0], 20
        )
        if self.bullet_speed_level > 1e15:
            text = 'Bullet Speed : max'
        else:
            text = 'Bullet Speed : {}'.format(self.bullet_speed_level)
        show_text(
            screen, text,
            790, 325, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Cost',
            790, 370, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Damage : {}'.format(100 + 100*(self.damage_level+1)),
            790, 400, [0, 0, 0], 20
        )
        if self.explode_range_level > 1e15:
            text = 'Explode Range : max'
        else:
            text = 'Explode Range : {}'.format(
                100 + 100*self.explode_range_level)
        show_text(
            screen, text,
            790, 425, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(100 + 100*(self.reload_level+1))
        show_text(
            screen, text,
            790, 450, [0, 0, 0], 20
        )
        if self.bullet_speed_level > 1e15:
            text = 'Bullet Speed : max'
        else:
            text = 'Bullet Speed : {}'.format(
                100 + 100*(self.bullet_speed_level+1))
        show_text(
            screen, text,
            790, 475, [0, 0, 0], 20
        )

        if natural_ingot >= 100 + (self.damage_level+1)*100:
            self.upgrade_damage.state = 0
        else:
            self.upgrade_damage.state = 1
        self.upgrade_damage.display(screen)
        if natural_ingot >= 100 + (self.explode_range_level+1)*100:
            self.upgrade_explode_range.state = 0
        else:
            self.upgrade_explode_range.state = 1
        self.upgrade_explode_range.display(screen)
        if natural_ingot >= 100 + (self.reload_level+1)*100:
            self.upgrade_reload.state = 0
        else:
            self.upgrade_reload.state = 1
        self.upgrade_reload.display(screen)
        if natural_ingot >= 100 + (self.bullet_speed_level+1)*100:
            self.upgrade_bullet_speed.state = 0
        else:
            self.upgrade_bullet_speed.state = 1
        self.upgrade_bullet_speed.display(screen)

    def upgrade(self, mouse_pos=pygame.Vector2(0, 0), natural_ingot=0):
        if self.upgrade_damage.click(mouse_pos):
            if natural_ingot >= 100 + (self.damage_level+1)*100:
                self.damage_level += 1
                natural_ingot -= 100 + self.damage_level*100
                self.damage += 100.0 * math.sqrt(self.damage_level)
        elif self.upgrade_explode_range.click(mouse_pos):
            if natural_ingot >= 100 + (self.explode_range_level+1)*100:
                self.explode_range_level += 1
                natural_ingot -= 100 + self.explode_range_level*100
                self.explode_range += TILE_SIZE/3 * 1/self.explode_range_level
                if self.explode_range > 3 * TILE_SIZE:
                    self.explode_range = 3 * TILE_SIZE
                    self.explode_range_level = 1e20
        elif self.upgrade_reload.click(mouse_pos):
            if natural_ingot >= 100 + (self.reload_level+1)*100:
                self.reload_level += 1
                natural_ingot -= 100 + self.reload_level*100
                self.reload += 0.5 * math.log10(self.reload_level*2)
                if self.reload >= 10:
                    self.reload = 10
                    self.reload_level = 1e20
        elif self.upgrade_bullet_speed.click(mouse_pos):
            if natural_ingot >= 100 + (self.bullet_speed_level+1)*100:
                self.bullet_speed_level += 1
                natural_ingot -= 100 + self.bullet_speed_level*100
                self.bullet_speed += TILE_SIZE/3 * 1/self.bullet_speed_level
                if self.bullet_speed >= 4 * TILE_SIZE:
                    self.bullet_speed = 4 * TILE_SIZE
                    self.bullet_speed_level = 1e20
        else:
            return [False, natural_ingot]
        return [True, natural_ingot]


class tesla_tower(tower):
    class bullet:
        def __init__(
            self, pos=pygame.Vector2(0, 0),
            interference_time=0,
            damage=0, explode_range=0,
            images=[]
        ):
            self.pierce = 1
            self.pos = pos
            self.images = images
            self.rect = self.images[0].get_rect()
            self.rect.center = self.pos
            self.state = 0
            self.size = explode_range
            self.damage = damage
            self.explode_range = explode_range
            self.interference_time = interference_time
            self.decay_time = 200

        def display(self, screen):
            self.rect.center = self.pos
            screen.blit(
                self.images[self.state],
                self.rect
            )

        def deal_damage(self, enemy):
            enemy.regenerate_shield_time += self.interference_time
            if enemy.shield > 0:
                enemy.shield = max(0, enemy.shield - self.damage * 8)
                return
            if enemy.anti_pierce < 10:
                enemy.hit -= max(self.damage/5,
                                 (1 - 19*enemy.armor/400) * self.damage)
            enemy.check_state()

        def detect(self, enemys=[], boss=None):
            if self.pierce <= 0:
                return True

            for enemy in enemys:
                if self.pos.distance_to(enemy.location) < (self.explode_range+enemy.size)/2:
                    self.deal_damage(enemy)
            if boss != None:
                if self.pos.distance_to(boss.location) < (self.explode_range+boss.size)/2:
                    self.deal_damage(boss)
                for enemy in boss.generated_unit:
                    if self.pos.distance_to(enemy.location) < (self.explode_range+enemy.size)/2:
                        self.deal_damage(enemy)

            self.pierce -= 1
            if (
                self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x > TILE_SIZE*12 or
                self.pos.y > TILE_SIZE*9
            ):
                self.pierce = 0
            return False

    def __init__(
        self, pos=pygame.Vector2(0, 0), volume=100
    ):
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['tesla_tower16.png', 'tesla_tower_bullet.png']
        damage = 40
        reload = 2
        range = 2*TILE_SIZE
        bullet_speed = 0
        super().__init__(
            pos, width, height,
            pictures,
            damage, reload,
            range, bullet_speed,
            volume
        )
        self.images[1] = pygame.transform.scale(
            self.images[1], [self.range * 2, self.range * 2])
        self.bullets = []

        self.upgrade_damage = button(
            'damage', pygame.Vector2(1000, 84), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_range = button(
            'range', pygame.Vector2(1000, 109), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_reload = button(
            'reload', pygame.Vector2(1000, 134), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_interference = button(
            'Interference', pygame.Vector2(1000, 159), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.damage_level = 0
        self.range_level = 0
        self.reload_level = 0
        self.interference_level = 0
        self.interference = 1000
        self.fire_sound = pygame.mixer.Sound(
            os.path.join(os.getcwd(), 'AppData', 'tesla_tower_fire.wav')
        )
        self.fire_sound.set_volume(self.volume / 100)

    def display_bullets(self, screen):
        for bullet in self.bullets:
            bullet.display(screen)

    def aim_first(self, enemys=[], boss=None):
        for enemy in enemys:
            if (self.location.distance_to(enemy.location) < self.range):
                return True
        if boss != None:
            for enemy in boss.generated_unit:
                if (self.location.distance_to(enemy.location) < self.range):
                    return True
            if (self.location.distance_to(boss.location) < self.range):
                return True
        return False

    def shoot_first(self, enemys=[], boss=None):
        if not self.aim_first(enemys, boss):
            return False
        bullet = self.bullet(
            self.location.copy(),
            self.interference,
            self.damage, self.range * 2,
            [self.images[1]]
        )
        self.bullets.append(bullet)
        return True

    def update_time_to_fire(self, delta_time=0):
        if self.time_to_fire > 0:
            self.time_to_fire -= delta_time

    def shoot(self, enemys=[], boss=None):
        if self.time_to_fire <= 0:
            if self.shoot_first(enemys, boss):
                self.time_to_fire += 1000.0/self.reload
                self.fire_sound.play()

    def update(self, delta_time, enemys=[], boss=None):
        self.update_time_to_fire(delta_time)
        self.shoot(enemys, boss)
        for bullet in self.bullets:
            if bullet.pierce > 0:
                bullet.detect(enemys, boss)
        for bullet in self.bullets:
            bullet.decay_time -= delta_time
            if bullet.decay_time <= 0:
                self.bullets.remove(bullet)

    def display_info(self, screen, natural_ingot):
        super().display_info(screen)
        show_text(
            screen,
            'Damage : {:.2f}'.format(self.damage),
            790, 100, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Range : {:.4f}'.format(self.range/TILE_SIZE),
            790, 125, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Reload : {:.2f}'.format(self.reload),
            790, 150, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Interference : {:.5f}'.format(self.interference / 1000),
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
        if self.range_level > 1e15:
            text = 'Range : max'
        else:
            text = 'Range : {}'.format(self.range_level)
        show_text(
            screen, text,
            790, 275, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(self.reload_level)
        show_text(
            screen, text,
            790, 300, [0, 0, 0], 20
        )
        if self.interference_level > 1e15:
            text = 'Interference : max'
        else:
            text = 'Interference : {}'.format(self.interference_level)
        show_text(
            screen, text,
            790, 325, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Cost',
            790, 370, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Damage : {}'.format(100 + 100*(self.damage_level+1)),
            790, 400, [0, 0, 0], 20
        )
        if self.range_level > 1e15:
            text = 'Range : max'
        else:
            text = 'Range : {}'.format(100 + 100*self.range_level)
        show_text(
            screen, text,
            790, 425, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(100 + 100*(self.reload_level+1))
        show_text(
            screen, text,
            790, 450, [0, 0, 0], 20
        )
        if self.interference_level > 1e15:
            text = 'Interference : max'
        else:
            text = 'Interference : {}'.format(
                100 + 100*(self.interference_level+1))
        show_text(
            screen, text,
            790, 475, [0, 0, 0], 20
        )

        if natural_ingot >= 100 + (self.damage_level+1)*100:
            self.upgrade_damage.state = 0
        else:
            self.upgrade_damage.state = 1
        self.upgrade_damage.display(screen)
        if natural_ingot >= 100 + (self.range_level+1)*100:
            self.upgrade_range.state = 0
        else:
            self.upgrade_range.state = 1
        self.upgrade_range.display(screen)
        if natural_ingot >= 100 + (self.reload_level+1)*100:
            self.upgrade_reload.state = 0
        else:
            self.upgrade_reload.state = 1
        self.upgrade_reload.display(screen)
        if natural_ingot >= 100 + (self.interference_level+1)*100:
            self.upgrade_interference.state = 0
        else:
            self.upgrade_interference.state = 1
        self.upgrade_interference.display(screen)

    def upgrade(self, mouse_pos=pygame.Vector2(0, 0), natural_ingot=0):
        if self.upgrade_damage.click(mouse_pos):
            if natural_ingot >= 100 + (self.damage_level+1)*100:
                self.damage_level += 1
                natural_ingot -= 100 + self.damage_level*100
                self.damage += 20.0 * math.sqrt(self.damage_level)
        elif self.upgrade_range.click(mouse_pos):
            if natural_ingot >= 100 + (self.range_level+1)*100:
                self.range_level += 1
                natural_ingot -= 100 + self.range_level*100
                self.range += TILE_SIZE/2 * 1/self.range_level
                self.images[1] = pygame.transform.scale(
                    self.images[1], [self.range * 2, self.range * 2])
                if self.range > 5 * TILE_SIZE:
                    self.range = 5 * TILE_SIZE
                    self.range_level = 1e20
        elif self.upgrade_reload.click(mouse_pos):
            if natural_ingot >= 100 + (self.reload_level+1)*100:
                self.reload_level += 1
                natural_ingot -= 100 + self.reload_level*100
                self.reload += 0.3 * math.log10(self.reload_level*2)
                if self.reload >= 6:
                    self.reload = 6
                    self.reload_level = 1e20
        elif self.upgrade_interference.click(mouse_pos):
            if natural_ingot >= 100 + (self.interference_level+1)*100:
                self.interference_level += 1
                natural_ingot -= 100 + self.interference_level*100
                self.interference += 500 * 1/self.interference_level
                if self.interference >= 10000:
                    self.interference = 10000
                    self.interference_level = 1e20
        else:
            return [False, natural_ingot]
        return [True, natural_ingot]


class acid_tower(tower):
    class bullet:
        def __init__(
                self, pos=pygame.Vector2(0, 0),
                velocity=pygame.Vector2(0, 0),
                damage=0, hardness=0,
                pierce=0, images=[]
        ):
            self.pierce = pierce
            self.pos = pos
            self.velocity = velocity
            self.images = images
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = TILE_SIZE/2
            self.rect.height = TILE_SIZE/2
            self.rect.center = self.pos
            self.state = 0
            self.size = TILE_SIZE
            self.damage = damage
            self.hardness = hardness

        def move(self, delta_time):
            self.pos += self.velocity * (delta_time/1000.0)

        def display(self, screen):
            self.rect.center = self.pos
            screen.blit(
                self.images[self.state],
                self.rect
            )

        def deal_damage(self, enemy):
            self.pierce -= 1
            move = (enemy.pos - self.pos)
            move = move.normalize() if move.length() != 0 else pygame.Vector2(0, 0)

            if enemy.shield > 0:
                enemy.shield = max(0, enemy.shield - self.damage)
                return
            enemy.armor -= self.hardness
            enemy.hit = max(0, enemy.hit - self.damage * 2)
            enemy.check_state()

        def detect(self, enemys=[], boss=None):
            for enemy in enemys:
                if self.pierce <= 0:
                    break
                if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                    enemy.progress = max(0, enemy.progress - 1)
                    self.deal_damage(enemy)
            if boss != None:
                if self.pierce <= 0:
                    return
                if self.pos.distance_to(boss.location) < (self.size+boss.size)/2:
                    self.deal_damage(boss)
                for enemy in boss.generated_unit:
                    if self.pierce <= 0:
                        return
                    if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                        self.deal_damage(enemy)
            if (
                self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x > TILE_SIZE*12 or
                self.pos.y > TILE_SIZE*9
            ):
                self.pierce = 0

    def __init__(
        self, pos=pygame.Vector2(0, 0), volume=100
    ):
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['acid_tower16.png', 'acid_bullet.png']
        damage = 0
        reload = 0.33
        range = 3*TILE_SIZE
        bullet_speed = 4*TILE_SIZE

        super().__init__(
            pos, width, height,
            pictures,
            damage, reload,
            range, bullet_speed,
            volume
        )
        self.images[1] = pygame.transform.scale(
            self.images[1], [TILE_SIZE / 2, TILE_SIZE / 2])
        self.aim = pygame.Vector2(0, 1)
        self.angle = 0
        self.bullets = []
        self.target = 'first'
        self.pierce = 1
        self.hardness = 1
        self.fire_sound = pygame.mixer.Sound(
            os.path.join(os.getcwd(), 'AppData', 'sniper_tower_fire.wav')
        )
        self.volume = volume
        self.fire_sound.set_volume(self.volume / 100)

        self.acid = 10
        self.upgrade_acid = button(
            'damage', pygame.Vector2(1000, 84), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_hardness = button(
            'hardness', pygame.Vector2(1000, 109), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_reload = button(
            'reload', pygame.Vector2(1000, 134), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_pierce = button(
            'bullet_speed', pygame.Vector2(1000, 159), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.acid_level = 0
        self.hardness_level = 0
        self.reload_level = 0
        self.pierce_level = 0

    def display_bullets(self, screen):
        for bullet in self.bullets:
            bullet.display(screen)

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

    def shoot_first(self, enemys=[], boss=None):
        if not self.aim_first(enemys, boss):
            return False
        bullet = self.bullet(
            self.location.copy(), pygame.Vector2(0, 0),
            self.acid, self.hardness * math.sqrt(self.acid),
            self.pierce, [self.images[1]]
        )
        bullet.velocity.from_polar([self.bullet_speed, -self.angle])
        # print(bullet.velocity)
        self.bullets.append(bullet)
        return True

    def update_time_to_fire(self, delta_time=0):
        if self.time_to_fire > 0:
            self.time_to_fire -= delta_time

    def shoot(self, enemys=[], boss=None):
        if self.time_to_fire <= 0:
            if self.target == 'first':
                if self.shoot_first(enemys, boss):
                    self.time_to_fire += 1000.0/self.reload
                    self.fire_sound.play()

        else:
            self.aim_first(enemys, boss)

    def update(self, delta_time, enemys=[], boss=None):
        self.update_time_to_fire(delta_time)
        self.shoot(enemys, boss)
        for bullet in self.bullets:
            bullet.move(delta_time)
            bullet.detect(enemys, boss)
        for bullet in self.bullets:
            if bullet.pierce <= 0:
                self.bullets.remove(bullet)

    def display_info(self, screen, natural_ingot):
        super().display_info(screen)
        show_text(
            screen,
            'Acid   : {:.2f}'.format(self.acid),
            790, 100, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Hardness : {:.5f}'.format(self.hardness),
            790, 125, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Reload   : {:.2f}'.format(self.reload),
            790, 150, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Pierce   : {}'.format(self.pierce),
            790, 175, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Level',
            790, 220, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Acid : {}'.format(self.acid_level),
            790, 250, [0, 0, 0], 20
        )
        if self.hardness_level > 1e15:
            text = 'Hardness : max'
        else:
            text = 'Hardness : {}'.format(self.hardness_level)
        show_text(
            screen, text,
            790, 275, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(self.reload_level)
        show_text(
            screen, text,
            790, 300, [0, 0, 0], 20
        )
        if self.pierce_level > 1e15:
            text = 'Pierce : max'
        else:
            text = 'Pierce : {}'.format(self.pierce_level)
        show_text(
            screen, text,
            790, 325, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Cost',
            790, 370, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Acid : {}'.format(50 + 50*(self.acid_level+1)),
            790, 400, [0, 0, 0], 20
        )
        if self.hardness_level > 1e15:
            text = 'Hardness : max'
        else:
            text = 'Hardness : {}'.format(50 + 50*(self.hardness_level+1))
        show_text(
            screen, text,
            790, 425, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(50 + 50*(self.reload_level+1))
        show_text(
            screen, text,
            790, 450, [0, 0, 0], 20
        )
        if self.pierce_level > 1e15:
            text = 'Pierce : max'
        else:
            text = 'Pierce : {}'.format(100 * (2**(self.pierce_level+1)))
        show_text(
            screen, text,
            790, 475, [0, 0, 0], 20
        )

        if natural_ingot >= 50 + (self.acid_level+1)*50:
            self.upgrade_acid.state = 0
        else:
            self.upgrade_acid.state = 1
        self.upgrade_acid.display(screen)
        if natural_ingot >= 50 + (self.hardness_level+1)*50:
            self.upgrade_hardness.state = 0
        else:
            self.upgrade_hardness.state = 1
        self.upgrade_hardness.display(screen)
        if natural_ingot >= 50 + (self.reload_level+1)*50:
            self.upgrade_reload.state = 0
        else:
            self.upgrade_reload.state = 1
        self.upgrade_reload.display(screen)
        if (not self.pierce_level > 1e15) and natural_ingot >= 100 * (2 ** (self.pierce_level+1)):
            self.upgrade_pierce.state = 0
        else:
            self.upgrade_pierce.state = 1
        self.upgrade_pierce.display(screen)

    def upgrade(self, mouse_pos=pygame.Vector2(0, 0), natural_ingot=0):
        if self.upgrade_acid.click(mouse_pos):
            if natural_ingot >= 50 + (self.acid_level+1)*50:
                self.acid_level += 1
                natural_ingot -= 50 + self.acid_level*50
                self.acid += 10.0 * (math.log10(self.acid_level) + 1)
        elif self.upgrade_hardness.click(mouse_pos):
            if natural_ingot >= 50 + (self.hardness_level+1)*50:
                self.hardness_level += 1
                natural_ingot -= 50 + self.hardness_level*50
                self.hardness += 3 * 1/self.hardness_level
                if self.hardness >= 20:
                    self.hardness = 20
                    self.hardness_level = 1e20
        elif self.upgrade_reload.click(mouse_pos):
            if natural_ingot >= 50 + (self.reload_level+1)*50:
                self.reload_level += 1
                natural_ingot -= 50 + self.reload_level*10
                self.reload += 0.05 * math.log10(self.reload_level*2)
                if self.reload >= 2:
                    self.reload = 2
                    self.reload_level = 1e20
        elif self.upgrade_pierce.click(mouse_pos):
            if (
                self.pierce_level < 1e15 and
                natural_ingot >= 100 * (2**(self.pierce_level+1))
            ):
                self.pierce_level += 1
                natural_ingot -= 100 * (2**self.pierce_level)
                self.pierce += 1
                if self.pierce >= 5:
                    self.pierce = 5
                    self.pierce_level = 1e20
        else:
            return [False, natural_ingot]
        return [True, natural_ingot]


class spread_tower(tower):
    class bullet:
        def __init__(
            self, pos=pygame.Vector2(0, 0),
            velocity=pygame.Vector2(0, 0),
            damage=0, layer=0,
            slow_rate=1, images=[]
        ):
            self.pierce = 1
            self.pos = pos
            self.velocity = velocity
            self.images = images
            self.rect = pygame.Rect(0, 0, 0, 0)
            self.rect.width = TILE_SIZE
            self.rect.height = TILE_SIZE
            self.rect.center = self.pos
            self.state = 0
            self.size = TILE_SIZE
            self.damage = damage
            self.layer = layer
            self.split_time = 1000
            self.slow_rate = slow_rate
            self.decay_time = 5000

        def move(self, delta_time):
            self.pos += self.velocity * (delta_time/1000.0)

        def display(self, screen):
            image = pygame.transform.rotozoom(
                self.images[self.state],
                math.degrees(-math.atan2(self.velocity.y, self.velocity.x)),
                1
            )
            self.rect.center = self.pos
            dw = image.get_rect().width - self.rect.width
            dw /= 2
            self.rect.centerx -= dw
            self.rect.centery -= dw
            screen.blit(
                image,
                self.rect
            )

        def deal_damage(self, enemy):
            self.pierce -= 1
            # damage dealing formula hasn't finished
            if enemy.is_slowed <= 1:
                enemy.move_speed *= self.slow_rate
                enemy.is_slowed += 1
            if enemy.shield > 0:
                enemy.shield = max(0, enemy.shield - self.damage)
            enemy.hit -= max(self.damage/20,
                             (1 - 19*enemy.armor/400) * self.damage)
            enemy.check_state()

        def detect(self, enemys=[], boss=None):
            for enemy in enemys:
                if self.pierce <= 0:
                    return
                if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                    self.deal_damage(enemy)
            if boss != None:
                if self.pierce <= 0:
                    return
                if self.pos.distance_to(boss.location) < (self.size+boss.size)/2:
                    self.deal_damage(boss)
                for enemy in boss.generated_unit:
                    if self.pierce <= 0:
                        return
                    if self.pos.distance_to(enemy.location) < (self.size+enemy.size)/2:
                        self.deal_damage(enemy)
            if (
                self.pos.x < 0 or
                self.pos.y < 0 or
                self.pos.x > TILE_SIZE*12 or
                self.pos.y > TILE_SIZE*9
            ):
                self.pierce = 0

    def __init__(
        self, pos=pygame.Vector2(0, 0), volume=100
    ):
        width = TILE_SIZE
        height = TILE_SIZE
        pictures = ['spread_tower.png', 'spread_tower_bullet.png']
        damage = 10000
        reload = 0.66
        range = 20*TILE_SIZE
        bullet_speed = 2*TILE_SIZE
        super().__init__(
            pos, width, height,
            pictures,
            damage, reload,
            range, bullet_speed,
            volume
        )
        self.aim = pygame.Vector2(0, 1)
        self.angle = 0
        self.bullets = []
        self.target = 'first'
        self.upgrade_damage = button(
            'damage', pygame.Vector2(1000, 84), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_freeze_rate = button(
            'freeze_rate', pygame.Vector2(1000, 109), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_reload = button(
            'reload', pygame.Vector2(1000, 134), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.upgrade_layer = button(
            'layer', pygame.Vector2(1000, 159), [0, 0, 0],
            TILE_SIZE/4, TILE_SIZE/4, ['can_upgrade.png', 'cannot_upgrade.png']
        )
        self.damage_level = 0
        self.freeze_rate_level = 0
        self.reload_level = 0
        self.layer_level = 0
        self.layer = 1
        self.freeze_rate = 10
        self.fire_sound = pygame.mixer.Sound(
            os.path.join(os.getcwd(), 'AppData', 'basic_tower_fire.wav')
        )
        self.fire_sound.set_volume(self.volume / 100)

    def display(self, screen):
        super().display(screen)
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

    def display_bullets(self, screen):
        for bullet in self.bullets:
            bullet.display(screen)

    def aim_first(self, enemys=[], boss=None):
        first_enemy = None
        for enemy in enemys:
            if (
                (first_enemy == None or
                 enemy.progress > first_enemy.progress)
            ):
                first_enemy = enemy
        if boss != None:
            for enemy in boss.generated_unit:
                if (
                    (first_enemy == None or
                     enemy.progress > first_enemy.progress)
                ):
                    first_enemy = enemy
            if (
                (first_enemy == None or
                 boss.progress > first_enemy.progress)
            ):
                first_enemy = boss
        if first_enemy == None:
            return None

        relation = first_enemy.location - self.location
        self.angle = math.atan2(relation.y, relation.x)
        self.angle = -math.degrees(self.angle)
        return first_enemy

    def shoot_first(self, enemys=[], boss=None):
        ret = self.aim_first(enemys, boss)
        if ret == None:
            return None
        bullet = self.bullet(
            self.location.copy(), pygame.Vector2(0, 0),
            self.damage, self.layer,
            1 - self.freeze_rate / 100, [self.images[1]]
        )
        bullet.velocity.from_polar([self.bullet_speed, -self.angle])

        # print(bullet.velocity)
        self.bullets.append(bullet)
        return ret

    def update_time_to_fire(self, delta_time=0):
        if self.time_to_fire > 0:
            self.time_to_fire -= delta_time

    def shoot(self, enemys=[], boss=None):
        ret = self.aim_first(enemys, boss)
        if self.time_to_fire <= 0:
            if self.target == 'first':
                if self.shoot_first(enemys, boss) != None:
                    self.time_to_fire += 1000.0/self.reload
                    self.fire_sound.play()
        return ret

    def update(self, delta_time, enemys=[], boss=None):
        self.update_time_to_fire(delta_time)
        en = self.shoot(enemys, boss)
        for bullet in self.bullets:
            bullet.move(delta_time)
            if bullet.decay_time > 0:
                bullet.decay_time = max(0, bullet.decay_time - delta_time)
            if bullet.split_time > 0:
                bullet.split_time = max(0, bullet.split_time - delta_time)
            if bullet.split_time == 0 and bullet.layer > 0:
                bullet.split_time = -1
                bullet.layer -= 1

                nb = self.bullet(
                    bullet.pos.copy(), bullet.velocity.copy(),
                    self.damage, bullet.layer,
                    1 - self.freeze_rate / 100, [self.images[1]]
                )
                angle = -math.atan2(nb.velocity.y, nb.velocity.x)
                angle = math.degrees(angle)
                nb.velocity.from_polar([nb.velocity.length(), -(angle + 10)])
                self.bullets.append(nb)
                nb2 = self.bullet(
                    bullet.pos.copy(), bullet.velocity.copy(),
                    self.damage, bullet.layer,
                    1 - self.freeze_rate / 100, [self.images[1]]
                )
                nb2.velocity.from_polar([nb.velocity.length(), -(angle - 10)])
                self.bullets.append(nb2)
            if en != None:
                speed = bullet.velocity.length()
                acceleration = en.location - bullet.pos
                # print(acceleration)
                acceleration = acceleration.normalize() * (100 * (delta_time / 1000)
                                                           ) if acceleration.length() != 0 else pygame.Vector2(0, 0)
                bullet.velocity += acceleration
                bullet.velocity = bullet.velocity.normalize() * (speed)
            bullet.detect(enemys, boss)
        for bullet in self.bullets:
            if bullet.pierce <= 0 and bullet.layer > 0:
                bullet.layer -= 1
                nb = self.bullet(
                    bullet.pos.copy(), bullet.velocity.copy(),
                    self.damage, bullet.layer,
                    1 - self.freeze_rate / 100, [self.images[1]]
                )
                angle = math.atan2(nb.velocity.y, nb.velocity.x)
                angle = math.degrees(angle)
                nb.velocity.from_polar([nb.velocity.length(), -(angle + 10)])
                self.bullets.append(nb)
                nb2 = self.bullet(
                    bullet.pos.copy(), bullet.velocity.copy(),
                    self.damage, bullet.layer,
                    1 - self.freeze_rate / 100, [self.images[1]]
                )
                nb2.velocity.from_polar([nb.velocity.length(), -(angle - 10)])
                self.bullets.append(nb2)

                self.bullets.remove(bullet)
            elif bullet.pierce <= 0 or bullet.decay_time <= 0:
                self.bullets.remove(bullet)

    def display_info(self, screen, natural_ingot):
        super().display_info(screen)
        show_text(
            screen,
            'Damage : {:.2f}'.format(self.damage),
            790, 100, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Freeze Rate  : {:.5f}%'.format(self.freeze_rate),
            790, 125, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Reload : {:.2f}'.format(self.reload),
            790, 150, [0, 0, 0], 20
        )
        show_text(
            screen,
            'Layer : {}'.format(self.layer),
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
        if self.freeze_rate_level > 1e15:
            text = 'Freeze Rate : max'
        else:
            text = 'Freeze Rate : {}'.format(self.freeze_rate_level)
        show_text(
            screen, text,
            790, 275, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(self.reload_level)
        show_text(
            screen, text,
            790, 300, [0, 0, 0], 20
        )
        if self.layer_level > 1e15:
            text = 'Layer : max'
        else:
            text = 'Layer : {}'.format(self.layer_level)
        show_text(
            screen, text,
            790, 325, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Cost',
            790, 370, [0, 0, 0], 20
        )

        show_text(
            screen,
            'Damage : {}'.format(5000 + (self.damage_level+1)*1000),
            790, 400, [0, 0, 0], 20
        )
        if self.freeze_rate_level > 1e15:
            text = 'Freeze Rate : max'
        else:
            text = 'Freeze Rate : {}'.format(
                500 + (self.freeze_rate_level+1)*100)
        show_text(
            screen, text,
            790, 425, [0, 0, 0], 20
        )
        if self.reload_level > 1e15:
            text = 'Reload : max'
        else:
            text = 'Reload : {}'.format(500 + (self.reload_level+1)*100)
        show_text(
            screen, text,
            790, 450, [0, 0, 0], 20
        )
        if self.layer_level > 1e15:
            text = 'Layer : max'
        else:
            text = 'Layer : {}'.format(100 * ((self.layer_level+1)**5))
        show_text(
            screen, text,
            790, 475, [0, 0, 0], 20
        )

        if natural_ingot >= 5000 + (self.damage_level+1)*1000:
            self.upgrade_damage.state = 0
        else:
            self.upgrade_damage.state = 1
        self.upgrade_damage.display(screen)
        if natural_ingot >= 500 + (self.freeze_rate_level+1)*100:
            self.upgrade_freeze_rate.state = 0
        else:
            self.upgrade_freeze_rate.state = 1
        self.upgrade_freeze_rate.display(screen)
        if natural_ingot >= 500 + (self.reload_level+1)*100:
            self.upgrade_reload.state = 0
        else:
            self.upgrade_reload.state = 1
        self.upgrade_reload.display(screen)
        if self.layer_level < 1e15 and natural_ingot >= 100 * ((self.layer_level+1)**5):
            self.upgrade_layer.state = 0
        else:
            self.upgrade_layer.state = 1
        self.upgrade_layer.display(screen)

    def upgrade(self, mouse_pos=pygame.Vector2(0, 0), natural_ingot=0):
        if self.upgrade_damage.click(mouse_pos):
            if natural_ingot >= 5000 + (self.damage_level+1)*1000:
                self.damage_level += 1
                natural_ingot -= 5000 + self.damage_level*1000
                self.damage += 500.0 * math.sqrt(self.damage_level)
        elif self.upgrade_freeze_rate.click(mouse_pos):
            if natural_ingot >= 500 + (self.freeze_rate_level+1)*100:
                self.freeze_rate_level += 1
                natural_ingot -= 500 + self.freeze_rate_level*100
                self.freeze_rate += 8 * 1/self.freeze_rate_level
                if self.freeze_rate >= 30:
                    self.freeze_rate = 30
                    self.freeze_rate_level = 1e20
        elif self.upgrade_reload.click(mouse_pos):
            if natural_ingot >= 500 + (self.reload_level+1)*100:
                self.reload_level += 1
                natural_ingot -= 500 + self.reload_level*100
                self.reload += 0.66 * 1/self.reload_level
                if self.reload >= 2.5:
                    self.reload = 2.5
                    self.reload_level = 1e20
        elif self.upgrade_layer.click(mouse_pos):
            if self.layer_level < 1e15 and natural_ingot >= 100 * ((self.layer_level+1)**5):
                self.layer_level += 1
                natural_ingot -= 100 * (self.layer_level**5)
                self.layer += 1
                if self.layer >= 5:
                    self.layer = 5
                    self.layer_level = 1e20
        else:
            return [False, natural_ingot]
        return [True, natural_ingot]
