from src.tower import *

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