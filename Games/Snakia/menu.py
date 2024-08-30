import states
import game
from math import floor

selection = 0


def init(wrapper, ch_state):
    global w, change_state, scene, scroll_bar_handle, scroll_bar_top_line, scroll_bar_bottom_line
    w = wrapper
    change_state = ch_state

    # Create a fresh scene to put our menu in
    scene = w.Scene()

    # Select button
    scene.add(w.Sprite(w.load_image("images/select.bmp"), 28, 7, [50, 78]))

    # Scroll bar
    scroll_bar_handle = w.Sprite(
        w.load_image("images/scrollBarHandle.bmp"), 3, 7, [102, 60]
    )
    scroll_bar_top_line = w.Sprite(w.load_image("images/line.bmp"), 1, 21, [102, 39])
    scroll_bar_bottom_line = w.Sprite(w.load_image("images/line.bmp"), 1, 10, [102, 67])

    scene.add(scroll_bar_handle)
    scene.add(scroll_bar_top_line)
    scene.add(scroll_bar_bottom_line)

    set_scrollbar_position(selection, 3)

    return scene


def update(keys):
    global selection

    if w.Key.MENU in keys:
        if game.is_playing():
            return change_state(states.PLAYING_GAME)
        else:
            return w.exit()
    elif w.Key.UP in keys:
        if selection > 0:
            selection -= 1
            set_scrollbar_position(selection, 3)
    elif w.Key.DOWN in keys:
        if selection < 2:
            selection += 1
            set_scrollbar_position(selection, 3)
    elif w.Key.A in keys:
        # New game
        game.reset()
        return change_state(states.PLAYING_GAME)

    return 30


def set_scrollbar_position(item, length):
    global scroll_bar_handle, scroll_bar_top_line, scroll_bar_bottom_line

    handle_height = 7
    x_position = 102
    y_start = 39
    y_end = 77
    y_position = y_start + floor(
        item / (length - 1) * (y_end - y_start - handle_height)
    )

    scroll_bar_handle.set_position([x_position, y_position])
    scroll_bar_top_line.set_dimensions([1, y_position - y_start])
    scroll_bar_bottom_line.set_position([x_position, y_position + handle_height])
    scroll_bar_bottom_line.set_dimensions([1, y_end - (y_position + handle_height)])
