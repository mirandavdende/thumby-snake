# States
MENU_MAIN = 0
MENU_OPTIONS = 1
PLAYING_GAME = 2

# Global state variables
state = MENU_MAIN
gameState = {
    "framerate": 5,
    "snake": None,
    "direction": None,
    "scenes": {MENU_MAIN: None, MENU_OPTIONS: None, PLAYING_GAME: None},
}

# Various sizes
STEP_SIZE = 4
SCREEN_WIDTH = 84
SCREEN_HEIGHT = 48
SCREEN_X = 22
SCREEN_Y = 36


# What directions can we move in?
class Dir:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    def opposite(dir):
        return dir ^ 1


# Indices into the spritesheet for the different images

# Head
HEAD_UP = 0
HEAD_DOWN = 1
HEAD_LEFT = 2
HEAD_RIGHT = 3
OPEN_MOUTH_UP = 4
OPEN_MOUTH_DOWN = 5
OPEN_MOUTH_LEFT = 6
OPEN_MOUTH_RIGHT = 7

# Tail
TAIL_UP = 8
TAIL_DOWN = 9
TAIL_LEFT = 10
TAIL_RIGHT = 11

# Bodyparts
BODY_HOR_RIGHT = 12
BODY_HOR_LEFT = 13
BODY_VER_UP = 14
BODY_VER_DOWN = 15
CORNER_LEFT_UP = 16
CORNER_LEFT_DOWN = 17
CORNER_RIGHT_UP = 18
CORNER_RIGHT_DOWN = 19
FULL_BELLY = 20

# Pickups
STAR = 21
APPLE = 22
MOUSE_LEFT = 23
MOUSE_RIGHT = 24


def init(wrapper):
    global w
    w = wrapper

    # Create the background image with the Nokia Phone as a scene that's always visible
    w.Scene().add(w.Sprite(w.load_image("images/phone.bmp"), 128, 128, [0, 0]))

    init_main_menu()


def update(keys):
    global w, state, gameState

    if state == PLAYING_GAME:
        if w.Key.UP in keys:
            gameState["direction"] = Dir.UP
        if w.Key.DOWN in keys:
            gameState["direction"] = Dir.DOWN
        if w.Key.LEFT in keys:
            gameState["direction"] = Dir.LEFT
        if w.Key.RIGHT in keys:
            gameState["direction"] = Dir.RIGHT
        if w.Key.MENU in keys:
            return change_state(MENU_MAIN)

        gameState["snake"] = moveSnake(
            gameState["snake"], gameState["direction"], w.screenHeight, w.screenWidth
        )

        return gameState["framerate"]

    elif state == MENU_MAIN:
        if w.Key.MENU in keys:
            if gameState["snake"]:
                return change_state(PLAYING_GAME)
            else:
                return w.exit()
        if w.Key.UP in keys:
            # New game
            init_game()
            return change_state(PLAYING_GAME)
        return 30


def change_state(new_state):
    global state, gameState
    state = new_state

    # Show the right scene for the new state
    for i in gameState["scenes"]:
        if gameState["scenes"][i] is not None:
            gameState["scenes"][i].hide()
    if gameState["scenes"][state] is not None:
        gameState["scenes"][state].show()

    # Return the correct framerate
    return gameState["framerate"] if state == PLAYING_GAME else 30


def init_main_menu():
    global w, gameState

    # Create a fresh scene to put our menu in
    scene = w.Scene()
    gameState["scenes"][MENU_MAIN] = scene

    # Select button
    scene.add(w.Sprite(w.load_image("images/select.bmp"), 28, 7, [50, 78]))


def init_game():
    global w, background, gameState

    # Create a fresh scene to put our game in
    scene = w.Scene()
    gameState["scenes"][PLAYING_GAME] = scene

    # Where is our spritesheet?
    spritesheet = w.load_image("images/spritesheet.bmp")

    # Initial snake
    snake_pos = [SCREEN_X + 12, SCREEN_Y + 8]
    gameState["snake"] = [
        # Sprite, coming from, going to, ate something
        [
            w.Sprite(spritesheet, STEP_SIZE, STEP_SIZE, snake_pos),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
        [
            w.Sprite(
                spritesheet,
                STEP_SIZE,
                STEP_SIZE,
                [snake_pos[0] + STEP_SIZE, snake_pos[1]],
            ),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
        [
            w.Sprite(
                spritesheet,
                STEP_SIZE,
                STEP_SIZE,
                [snake_pos[0] + 2 * STEP_SIZE, snake_pos[1]],
            ),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
        [
            w.Sprite(
                spritesheet,
                STEP_SIZE,
                STEP_SIZE,
                [snake_pos[0] + 3 * STEP_SIZE, snake_pos[1]],
            ),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
    ]
    showCorrectFrames(gameState["snake"])
    for segment in gameState["snake"]:
        scene.add(segment[0])

    # Initial direction
    gameState["direction"] = Dir.RIGHT

    # Initial frame rate
    gameState["framerate"] = 5


def moveSnake(snake, direction, width, height):
    # Shift all snake segments one position towards the head
    for i in range(len(snake) - 1):
        snake[i][0].setPosition(snake[i + 1][0].getPosition())
        snake[i][1] = snake[i + 1][1]  # coming from
        snake[i][2] = snake[i + 1][2]  # going to
        snake[i][3] = snake[i + 1][3]  # ate something

    # Move snake head one place in the desired direction
    head = snake[len(snake) - 1]
    position = head[0].getPosition()

    if direction == Dir.UP:
        position[1] -= STEP_SIZE
    if direction == Dir.DOWN:
        position[1] += STEP_SIZE
    if direction == Dir.LEFT:
        position[0] -= STEP_SIZE
    if direction == Dir.RIGHT:
        position[0] += STEP_SIZE

    head[2] = direction  # going to
    head[1] = Dir.opposite(direction)  # coming from

    # Wrap snake around virtual screen
    if position[0] < SCREEN_X:
        position[0] = SCREEN_X + SCREEN_WIDTH - STEP_SIZE
    if position[0] > SCREEN_X + SCREEN_WIDTH - STEP_SIZE:
        position[0] = SCREEN_X
    if position[1] < SCREEN_Y:
        position[1] = SCREEN_Y + SCREEN_HEIGHT - STEP_SIZE
    if position[1] > SCREEN_Y + SCREEN_HEIGHT - STEP_SIZE:
        position[1] = SCREEN_Y

    head[0].setPosition(position)

    # Link second segment up with head direction
    snake[len(snake) - 2][2] = head[2]

    showCorrectFrames(snake)
    return snake


def showCorrectFrames(snake):
    for i in range(len(snake)):
        sprite = snake[i][0]
        coming_from = snake[i][1]
        going_to = snake[i][2]
        eating = snake[i][3]

        # All of the code below is just to select the right bitmap to show in
        # this spot.

        # Are we a regular body part?
        if (
            coming_from == Dir.LEFT
            and going_to == Dir.UP
            or coming_from == Dir.UP
            and going_to == Dir.LEFT
        ):
            sprite.setFrame(CORNER_LEFT_UP)
        if (
            coming_from == Dir.LEFT
            and going_to == Dir.DOWN
            or coming_from == Dir.DOWN
            and going_to == Dir.LEFT
        ):
            sprite.setFrame(CORNER_LEFT_DOWN)
        if (
            coming_from == Dir.RIGHT
            and going_to == Dir.UP
            or coming_from == Dir.UP
            and going_to == Dir.RIGHT
        ):
            sprite.setFrame(CORNER_RIGHT_UP)
        if (
            coming_from == Dir.RIGHT
            and going_to == Dir.DOWN
            or coming_from == Dir.DOWN
            and going_to == Dir.RIGHT
        ):
            sprite.setFrame(CORNER_RIGHT_DOWN)
        if coming_from == Dir.UP and going_to == Dir.DOWN:
            sprite.setFrame(BODY_VER_DOWN)
        if coming_from == Dir.DOWN and going_to == Dir.UP:
            sprite.setFrame(BODY_VER_UP)
        if coming_from == Dir.LEFT and going_to == Dir.RIGHT:
            sprite.setFrame(BODY_HOR_RIGHT)
        if coming_from == Dir.RIGHT and going_to == Dir.LEFT:
            sprite.setFrame(BODY_HOR_LEFT)

        if eating:
            sprite.setFrame(FULL_BELLY)

        # Are we the tail?
        if i == 0:
            if going_to == Dir.UP:
                sprite.setFrame(TAIL_UP)
            if going_to == Dir.DOWN:
                sprite.setFrame(TAIL_DOWN)
            if going_to == Dir.LEFT:
                sprite.setFrame(TAIL_LEFT)
            if going_to == Dir.RIGHT:
                sprite.setFrame(TAIL_RIGHT)

        # Are we the head?
        if i == len(snake) - 1:
            if coming_from == Dir.UP:
                sprite.setFrame(HEAD_DOWN)
            if coming_from == Dir.DOWN:
                sprite.setFrame(HEAD_UP)
            if coming_from == Dir.LEFT:
                sprite.setFrame(HEAD_RIGHT)
            if coming_from == Dir.RIGHT:
                sprite.setFrame(HEAD_LEFT)
