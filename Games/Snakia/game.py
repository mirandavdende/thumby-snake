import states

# Internal game state
snake = None
direction = None
framerate = 5

# Various constants
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


def init(wrapper, ch_state):
    global w, change_state, scene, spritesheet
    change_state = ch_state
    w = wrapper

    # Create a fresh scene to put our game in
    scene = w.Scene()

    # Where is our spritesheet?
    spritesheet = w.load_image("images/spritesheet.bmp")

    # Reset to a new game
    reset()

    return scene


def update(keys):
    global snake, direction

    if w.Key.UP in keys:
        direction = Dir.UP
    if w.Key.DOWN in keys:
        direction = Dir.DOWN
    if w.Key.LEFT in keys:
        direction = Dir.LEFT
    if w.Key.RIGHT in keys:
        direction = Dir.RIGHT
    if w.Key.MENU in keys:
        return change_state(states.MENU_MAIN)

    snake = move_snake(snake, direction)

    return framerate


def reset():
    global snake, direction, framerate

    # Remove any old sprites from the scene
    scene.remove_children()

    # Initial snake
    snake_pos = [SCREEN_X + 12, SCREEN_Y + 8]
    snake = [
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

    # Select all the right images for the segements of the snake
    show_correct_frames(snake)

    # Add the sprites that make up the snake to the scene
    for segment in snake:
        scene.add(segment[0])

    # Initial direction
    direction = Dir.RIGHT

    # Initial frame rate
    framerate = 5


def is_playing():
    return snake is not None


def get_framerate():
    return framerate


def move_snake(snake, direction):
    # Shift all snake segments one position towards the head
    for i in range(len(snake) - 1):
        snake[i][0].set_position(snake[i + 1][0].get_position())
        snake[i][1] = snake[i + 1][1]  # coming from
        snake[i][2] = snake[i + 1][2]  # going to
        snake[i][3] = snake[i + 1][3]  # ate something

    # Move snake head one place in the desired direction
    head = snake[len(snake) - 1]
    position = head[0].get_position()

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

    head[0].set_position(position)

    # Link second segment up with head direction
    snake[len(snake) - 2][2] = head[2]

    show_correct_frames(snake)
    return snake


def show_correct_frames(snake):
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
            sprite.set_frame(CORNER_LEFT_UP)
        if (
            coming_from == Dir.LEFT
            and going_to == Dir.DOWN
            or coming_from == Dir.DOWN
            and going_to == Dir.LEFT
        ):
            sprite.set_frame(CORNER_LEFT_DOWN)
        if (
            coming_from == Dir.RIGHT
            and going_to == Dir.UP
            or coming_from == Dir.UP
            and going_to == Dir.RIGHT
        ):
            sprite.set_frame(CORNER_RIGHT_UP)
        if (
            coming_from == Dir.RIGHT
            and going_to == Dir.DOWN
            or coming_from == Dir.DOWN
            and going_to == Dir.RIGHT
        ):
            sprite.set_frame(CORNER_RIGHT_DOWN)
        if coming_from == Dir.UP and going_to == Dir.DOWN:
            sprite.set_frame(BODY_VER_DOWN)
        if coming_from == Dir.DOWN and going_to == Dir.UP:
            sprite.set_frame(BODY_VER_UP)
        if coming_from == Dir.LEFT and going_to == Dir.RIGHT:
            sprite.set_frame(BODY_HOR_RIGHT)
        if coming_from == Dir.RIGHT and going_to == Dir.LEFT:
            sprite.set_frame(BODY_HOR_LEFT)

        if eating:
            sprite.set_frame(FULL_BELLY)

        # Are we the tail?
        if i == 0:
            if going_to == Dir.UP:
                sprite.set_frame(TAIL_UP)
            if going_to == Dir.DOWN:
                sprite.set_frame(TAIL_DOWN)
            if going_to == Dir.LEFT:
                sprite.set_frame(TAIL_LEFT)
            if going_to == Dir.RIGHT:
                sprite.set_frame(TAIL_RIGHT)

        # Are we the head?
        if i == len(snake) - 1:
            if coming_from == Dir.UP:
                sprite.set_frame(HEAD_DOWN)
            if coming_from == Dir.DOWN:
                sprite.set_frame(HEAD_UP)
            if coming_from == Dir.LEFT:
                sprite.set_frame(HEAD_RIGHT)
            if coming_from == Dir.RIGHT:
                sprite.set_frame(HEAD_LEFT)
