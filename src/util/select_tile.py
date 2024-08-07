def select_tile(
    mouse_pos,
    tower_info,
    towers,
    map_info,
    show_tower_info,
    selected_tile,
    selected_tower
):
    tile_pos = [int(mouse_pos.y // 64), int(mouse_pos.x // 64)]
    show_buy_tower = False

    if (
        tile_pos[0] < 9 and
        tile_pos[1] < 12 and
        map_info[tile_pos[0]][tile_pos[1]] != 1 and
        map_info[tile_pos[0]][tile_pos[1]] != 2 and
        map_info[tile_pos[0]][tile_pos[1]] != 3
    ):
        selected_tile = tile_pos
        if tower_info[tile_pos[0], tile_pos[1]] == 0:
            show_buy_tower = True
            show_tower_info = False
        else:
            show_buy_tower = False
            show_tower_info = True

    for tow in towers:
        if tow.detect_mouse(mouse_pos):
            selected_tower = tow
    return (selected_tile, show_buy_tower, show_tower_info, selected_tower)