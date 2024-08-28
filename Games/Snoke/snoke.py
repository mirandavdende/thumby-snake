# How big is one piece?
STEP_SIZE = 4


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
    global w, snake, direction, background
    w = wrapper

    # Background
    background = w.Square(0, 0, 128, 128, [151, 198, 6])

    # Where is our spritesheet?
    spritesheet = w.load_image("images/spritesheet.bmp")

    # Initial snake
    snake = [
        # Sprite, coming from, going to, ate something
        [
            w.Sprite(spritesheet, STEP_SIZE, STEP_SIZE, [24, 32]),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
        [
            w.Sprite(spritesheet, STEP_SIZE, STEP_SIZE, [28, 32]),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
        [
            w.Sprite(spritesheet, STEP_SIZE, STEP_SIZE, [32, 32]),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
        [
            w.Sprite(spritesheet, STEP_SIZE, STEP_SIZE, [36, 32]),
            Dir.LEFT,
            Dir.RIGHT,
            False,
        ],
    ]

    # Initial direction
    direction = Dir.RIGHT


def update(keys):
    global w, snake, direction

    if w.Key.UP in keys:
        direction = Dir.UP
    if w.Key.DOWN in keys:
        direction = Dir.DOWN
    if w.Key.LEFT in keys:
        direction = Dir.LEFT
    if w.Key.RIGHT in keys:
        direction = Dir.RIGHT

    snake = moveSnake(snake, direction, w.screenHeight, w.screenWidth)
    showCorrectFrames(snake)

    return 10  # Frame rate, increase to speed up


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

    # Wrap snake around screen
    if position[0] < 0:
        position[0] = width - STEP_SIZE
    if position[0] > width - STEP_SIZE:
        position[0] = 0
    if position[1] < 0:
        position[1] = height - STEP_SIZE
    if position[1] > height - STEP_SIZE:
        position[1] = 0

    head[0].setPosition(position)

    # Link second segment up with head direction
    snake[len(snake) - 2][2] = head[2]

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
