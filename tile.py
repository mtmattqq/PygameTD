import pygame
import numpy as np
import os

TILE_SIZE=64

class tileset:
    def __init__(self, file, size=(TILE_SIZE, TILE_SIZE), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()
    
    def __init__(self, tiles = [], width = 0, hight = 0) :
        self.tiles = []
        for tile in tiles :
            self.tiles.append(pygame.transform.scale(pygame.image.load(
                os.path.join(os.getcwd(),'AppData',tile)).convert_alpha(), (width,hight)))

    def load(self):
        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'
    
class tilemap:
    def __init__(self, tileset, size=(0, 0), rect=None):
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)

        h, w = self.size
        self.image = pygame.Surface((TILE_SIZE*w, TILE_SIZE*h))
        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                tile = self.tileset.tiles[self.map[i, j]]
                self.image.blit(tile, (j*TILE_SIZE, i*TILE_SIZE))

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)
        # print(self.map)
        # print(self.map.shape)
        self.render()

    def set_random(self):
        n = len(self.tileset.tiles)
        self.map = np.random.randint(n, size=self.size)
        print(self.map)
        self.render()

    def load(self, map_info = [[]]) :
        m, n = self.map.shape
        for i in range(m):
            for j in range(n):
                self.map[i, j] = map_info[i][j]

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'
