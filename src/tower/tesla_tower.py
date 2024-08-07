from src.tower import *

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

    def display(self, screen):
        screen.blit(
            self.images[self.state],
            (self.pos*TILE_SIZE)
        )

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