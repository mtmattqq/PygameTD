from src.tower import *

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