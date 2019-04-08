from bearlibterminal import terminal as blt
import random


class Entity:
    def __init__(self, x, y, char, hue):
        self.x = x
        self.y = y
        self.char = char
        self.hue = hue

    def move(self, dx, dy):
        if not my_map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        blt.color(self.hue)
        blt.printf(self.x, self.y, self.char)

    def clear(self):
        blt.color(self.hue)
        blt.printf(self.x, self.y, ' ')


def render_all(box, map_width, map_height):
    for y in range(map_height):
        for x in range(map_width):
            wall = my_map[x][y].block_sight
            if wall:
                blt.color('terrain')
                blt.printf(x, y, '#')
            else:
                blt.color('terrain')
                blt.printf(x, y, '.')

    for obj in box:
        obj.draw()


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


def create_room(room):
    global my_map
    for x in range(room.x1, room.x2):
        for y in range(room.y1, room.y2):
            if x == room.x1 or x == room.x2 - 1 or \
                    y == room.y1 or y == room.y2 - 1:
                my_map[x][y].blocked = True
                my_map[x][y].block_sight = True
            else:
                my_map[x][y].blocked = False
                my_map[x][y].block_sight = False
    door_side_xy = random.randint(0, 1)
    door_side = random.randint(0, 1)
    if door_side_xy == 0:
        door_spot_x = random.randint(room.x1+1, room.x2-2)
        if door_side == 0:
            my_map[door_spot_x][room.y1].blocked = False
            my_map[door_spot_x][room.y1].block_sight = False
        else:
            my_map[door_spot_x][room.y2-1].blocked = False
            my_map[door_spot_x][room.y2-1].block_sight = False
    else:
        door_spot_y = random.randint(room.y1+1, room.y2-2)
        if door_side == 0:
            my_map[room.x1][door_spot_y].blocked = False
            my_map[room.x1][door_spot_y].block_sight = False
        else:
            my_map[room.x2-1][door_spot_y].blocked = False
            my_map[room.x2-1][door_spot_y].block_sight = False


def make_map(height, width):
    global my_map

    my_map = [[Tile(False)
               for y in range(height)]
              for x in range(width)]

    for x in range(width):
        my_map[x][0].blocked = True
        my_map[x][0].block_sight = True
        my_map[x][height - 1].blocked = True
        my_map[x][height - 1].block_sight = True
    for y in range(height):
        my_map[0][y].blocked = True
        my_map[0][y].block_sight = True
        my_map[width - 1][y].blocked = True
        my_map[width - 1][y].block_sight = True

    room1 = Rect(2, 2, 5, 5)
    room2 = Rect(10, 10, 5, 5)
    room3 = Rect(10, 2, 5, 5)
    create_room(room1)
    create_room(room2)
    create_room(room3)
