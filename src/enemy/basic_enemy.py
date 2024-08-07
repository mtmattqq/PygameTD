from src.enemy import *

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