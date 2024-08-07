from src.enemy import *

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