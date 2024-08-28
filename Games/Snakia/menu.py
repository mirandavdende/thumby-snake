import states
import game


def init(wrapper, ch_state):
    global w, change_state
    w = wrapper
    change_state = ch_state

    # Create a fresh scene to put our menu in
    scene = w.Scene()

    # Select button
    scene.add(w.Sprite(w.load_image("images/select.bmp"), 28, 7, [50, 78]))

    return scene


def update(keys):
    if w.Key.MENU in keys:
        if game.is_playing():
            return change_state(states.PLAYING_GAME)
        else:
            return w.exit()
    elif w.Key.UP in keys:
        # New game
        game.reset()
        return change_state(states.PLAYING_GAME)

    return 30
