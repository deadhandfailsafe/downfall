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
            loot = my_map[x][y].loot
            if wall:
                blt.color('terrain')
                blt.printf(x, y, '#')
            elif loot:
                blt.color('loot')
                blt.printf(x, y, '±')
            else:
                blt.color('terrain')
                blt.printf(x, y, '·')

    for obj in box:
        obj.draw()


class Tile:
    def __init__(self, blocked, block_sight=None, room=False):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

        self.room = room
        self.loot = False


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


def create_room(room, mw, mh):
    global my_map
    room_checking = True
    room_check = False
    while room_checking is True:
        for x in range(room.x1 - 1, room.x2 + 1):
            for y in range(room.y1 - 1, room.y2 + 1):
                if my_map[x][y].room is True:
                    room_check = True
        if room_check is False:
            room_checking = False
        elif room_check is True:
            room.x1 += 1
            room.x2 += 1
            room_check = False
        if room.x1 >= mw - 2 or room.x2 >= mw - 2:
            return None

    for x in range(room.x1, room.x2):
        for y in range(room.y1, room.y2):
            if x == room.x1 or x == room.x2 - 1 or \
                    y == room.y1 or y == room.y2 - 1:
                my_map[x][y].blocked = True
                my_map[x][y].block_sight = True
            else:
                my_map[x][y].blocked = False
                my_map[x][y].block_sight = False
            my_map[x][y].room = True
    door_side_xy = random.randint(0, 1)
    door_side = random.randint(0, 1)
    if door_side_xy == 0:
        door_spot_x = random.randint(room.x1 + 1, room.x2 - 2)
        if door_side == 0:
            my_map[door_spot_x][room.y1].blocked = False
            my_map[door_spot_x][room.y1].block_sight = False
        else:
            my_map[door_spot_x][room.y2 - 1].blocked = False
            my_map[door_spot_x][room.y2 - 1].block_sight = False
    else:
        door_spot_y = random.randint(room.y1 + 1, room.y2 - 2)
        if door_side == 0:
            my_map[room.x1][door_spot_y].blocked = False
            my_map[room.x1][door_spot_y].block_sight = False
        else:
            my_map[room.x2 - 1][door_spot_y].blocked = False
            my_map[room.x2 - 1][door_spot_y].block_sight = False
    loot_check = random.randint(1, 3)
    if loot_check == 1:
        loot_placed = False
        loot_place_x = random.randint(room.x1 + 1, room.x2 - 2)
        loot_place_y = random.randint(room.y1 + 1, room.y2 - 2)
        if loot_placed is False:
            my_map[loot_place_x][loot_place_y].loot = True
            loot_placed = True


def room_generator(mw, mh, amount):
    for amt in range(amount):
        x = random.randint(2, mw - 5)
        y = random.randint(2, mh - 5)
        w = random.randint(5, 9)
        h = random.randint(5, 9)
        if x + w >= mw - 4:
            w = (mw - x) - 2
        if y + h >= mh - 4:
            h = (mh - y) - 2
        room = Rect(x, y, w, h)
        create_room(room, mw, mh)


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

    room_generator(width, height, 13)
