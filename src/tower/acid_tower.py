from src.tower import *

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