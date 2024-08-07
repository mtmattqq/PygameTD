from src.tower import *

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

    def update(self, delta_time, enemys=[], boss=None):
        if super().update(delta_time, enemys, boss):
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