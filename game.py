from bearlibterminal import terminal as blt
import entity


terminal_width = 80
terminal_height = 25
map_width = terminal_width
map_height = terminal_height - 2
my_map = []
blt.open()
blt.set("window: size=80x25; font: tileset.png, size=8x12, codepage=437")
blt.set("palette.bg = #5C3C0D")
blt.bkcolor('bg')
blt.set("palette.fg = #F68F37")
blt.set("palette.enemy = #231712")
blt.set("palette.terrain = #AD4E1A")

entity.make_map(map_height, map_width)

player = entity.Entity(terminal_width//2, terminal_height//2, '@', 'fg')
npc = entity.Entity(terminal_width//2 - 5, terminal_height//2, '@', 'enemy')
entity_box = [player, npc]
entity.render_all(entity_box, map_width, map_height)
blt.refresh()

game_state = True


def handle_keys():
    global game_state

    user_input = blt.read()

    if user_input == blt.TK_W:
        player.move(0, -1)
    elif user_input == blt.TK_S:
        player.move(0, 1)
    elif user_input == blt.TK_A:
        player.move(-1, 0)
    elif user_input == blt.TK_D:
        player.move(1, 0)
    elif user_input == blt.TK_Q and \
            blt.check(blt.TK_CONTROL):
        game_state = False


while game_state is True:
    for unit in entity_box:
        entity.Entity.clear(unit)
    handle_keys()
    entity.render_all(entity_box, map_width, map_height)
    blt.refresh()

blt.close()
