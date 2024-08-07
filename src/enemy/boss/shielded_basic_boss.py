from src.enemy import *

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