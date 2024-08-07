from src.variables import *
import src.tile as tile
from src.vec2D import transform

def find_path(map=[[]]):
    m = len(map)
    n = len(map[0])

    def in_boarder(r, c):
        return (
            r >= 0 and c >= 0 and
            r < m and c < n
        )
    enemy_source = None
    main_tower = None
    for i in range(m):
        for j in range(n):
            if map[i][j] == 1:
                main_tower = [i, j]
            elif map[i][j] == 2:
                enemy_source = [i, j]
    if enemy_source == None or main_tower == None:
        return None
    isv = []
    for i in range(m):
        line = []
        for j in range(n):
            line.append(False)
        isv.append(line)

    path = []

    def dfs(pos_now=[]):
        isv[pos_now[0]][pos_now[1]] = True
        for d in MOVEMENT:
            next_stap = [pos_now[0] + d[0], pos_now[1] + d[1]]
            if (
                in_boarder(next_stap[0], next_stap[1]) and
                (map[next_stap[0]][next_stap[1]] == 3 or
                 map[next_stap[0]][next_stap[1]] == 1) and
                not isv[next_stap[0]][next_stap[1]]
            ):
                path.append(
                    transform(pygame.Vector2(pos_now[1], pos_now[0]), tile.TILE_SIZE))
                if map[next_stap[0]][next_stap[1]] == 1 or dfs(next_stap):
                    return True
                path.pop()
                break
        return False
    if dfs(enemy_source):
        path.append(
            transform(pygame.Vector2(main_tower[1], main_tower[0]), tile.TILE_SIZE))
        return path
    else:
        return None