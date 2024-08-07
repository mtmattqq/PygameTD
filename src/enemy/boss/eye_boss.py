from src.enemy import *

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