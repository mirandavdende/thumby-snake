import states
import menu
import game

# Global state variables
state = states.MENU_MAIN
scenes = {states.MENU_MAIN: None, states.MENU_OPTIONS: None, states.PLAYING_GAME: None}


def init(wrapper):
    global w
    w = wrapper

    # Create the background image with the Nokia Phone as a scene that's always visible
    w.Scene().add(w.Sprite(w.load_image("images/phone.bmp"), 128, 128, [0, 0]))

    scenes[states.MENU_MAIN] = menu.init(w, change_state)
    scenes[states.PLAYING_GAME] = game.init(w, change_state)
    change_state(states.MENU_MAIN)


def update(keys):
    if state == states.PLAYING_GAME:
        return game.update(keys)
    elif state == states.MENU_MAIN:
        return menu.update(keys)


def change_state(new_state):
    global state
    state = new_state

    # Show the right scene for the new state
    for i in scenes:
        if scenes[i] is not None:
            scenes[i].hide()
    if scenes[state] is not None:
        scenes[state].show()

    # Return the correct framerate
    return game.get_framerate() if state == states.PLAYING_GAME else 30
