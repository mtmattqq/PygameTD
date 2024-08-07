from src.enemy import *

class super_shield(enemy):
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
            'super_shield16.png',
            'hit_bar_red.png',
            'hit_bar_green.png',
            'hit_bar_blue.png',
        ]

        super().__init__(
            pos, width, height,
            pictures,
            hit, armor,
            shield, move_speed,
            path
        )
        self.size = size
        self.regenerate_shield_rate = 200

    def copy(self):
        ret = super_shield()
        ret.__init__(
            self.pos, self.hit,
            self.armor, self.shield,
            self.move_speed, self.path
        )
        return ret

    def display(self, screen):
        super().display(screen)
        if self.hit == self.max_hit and self.shield == self.max_shield:
            return
        hit_bar_rect = self.rect.copy()
        hit_bar_rect.centery -= self.size/2
        screen.blit(
            self.images[1],
            hit_bar_rect
        )

        self.hit = max(self.hit, 0)
        hit_bar_green = pygame.transform.scale(
            self.images[2],
            (self.size * (self.hit / self.max_hit), self.size/2)
        )

        hit_bar_rect.centery += 9

        screen.blit(
            hit_bar_green,
            hit_bar_rect
        )

        self.shield = max(self.shield, 0)
        hit_bar_blue = pygame.transform.scale(
            self.images[3],
            (self.size * (self.shield / self.max_shield), self.size/2)
        )

        hit_bar_rect.centery -= TILE_SIZE/32

        screen.blit(
            hit_bar_blue,
            hit_bar_rect
        )