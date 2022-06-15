import thumby

MOUTH_CLOSED_RIGHT = const(0)
MOUTH_OPEN_RIGHT = const(1)
BODY_HOR_RIGHT = const(2)
BODY_HOR_LEFT = const(3)
BODY_VER_UP = const(4)
BODY_VER_DOWN = const(5)
TAIL_RIGHT = const(6)
APPLE = const(10)

def drawSnake(stamp, snake):
    thumby.display.fill(0) # Clear screen
    stamp.setFrame(APPLE)
    for i in range(len(snake)):
        pos = snake[i]
        stamp.x = pos[0]
        stamp.y = pos[1]
        thumby.display.drawSprite(stamp)
    thumby.display.update()

def moveSnake(snake, dX, dY):
    # Shift all snake parts one position
    for i in range(len(snake) - 1):
        snake[i] = snake[i+1]
    # Move snake head horizontally by increasing X
    head = snake[len(snake) - 1].copy()
    head[0] += dX
    head[1] += dY
    snake[len(snake) - 1] = head
    return snake

def startGame():
    # Snake image data is here
    snakeImages = bytearray([
        5,6,6,0,5,6,9,0,6,2,4,6,6,4,2,6,
        0,13,11,0,0,11,13,0,4,4,6,6,6,10,
        12,0,0,12,10,6,6,11,13,6,2,5,2,0,
        6,6,5,0,6,8,12,14,15,13,14,8
    ])
    snakeStamp = thumby.Sprite(4, 4, snakeImages)
    thumby.display.setFPS(2) # Update every 1/2 second

    dX = 4
    dY = 0

    snake = [
        [22, 30], # Tail end
        [22, 26], # Body section
        [22, 22], # Body section
        [22, 18], # Body section
        [26, 18], # Body section
        [26, 14]  # Head
    ]

    while True:
        drawSnake(snakeStamp, snake)
        snake = moveSnake(snake, dX, dY)

        if thumby.buttonU.justPressed():
            dY = -4
            dX = 0
        elif thumby.buttonD.justPressed():
            dY = 4
            dX = 0
        elif thumby.buttonR.justPressed():
            dX = 4
            dY = 0
        elif thumby.buttonL.justPressed():
            dX = -4
            dY = 0



# Uncomment this code to show the title screen and menu before starting the game:

# import sys
# sys.path.insert(0, "/".join(__file__.split("/")[0:-1]))
# import launch
# launch.mainMenu(startGame)

# Uncomment this code to just immediately start the game:

startGame()
