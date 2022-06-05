import thumby

MOUTH_CLOSED_RIGHT = const(0)
MOUTH_OPEN_RIGHT = const(1)
BODY_HOR_RIGHT = const(2)
BODY_HOR_LEFT = const(3)
BODY_VER_UP = const(4)
BODY_VER_DOWN = const(5)
TAIL_RIGHT = const(6)

def startGame():
    # Snake image data is here
    snakeImages = bytearray([
        5,6,6,0,5,6,9,0,6,2,4,6,6,4,2,6,
        0,13,11,0,0,11,13,0,4,4,6,6,6,10,
        12,0,0,12,10,6,6,11,13,6,2,5,2,0,
        6,6,5,0,6,8,12,14,15,13,14,8
    ])
    snake = thumby.Sprite(4, 4, snakeImages)
    startPos = 50 # Start position
    length = 8 # length of the snake segments
    thumby.display.setFPS(2) # Update every 1/2 second

    while True:
        thumby.display.fill(0) # Clear screen
        snake.setFrame(MOUTH_CLOSED_RIGHT)
        snake.x = startPos
        snake.y = 18
        thumby.display.drawSprite(snake)
        snake.setFrame(BODY_HOR_RIGHT)
        for x in range(length):
            snake.x -= 4
            thumby.display.drawSprite(snake)
        snake.setFrame(TAIL_RIGHT)
        snake.x -= 4
        thumby.display.drawSprite(snake)
        thumby.display.update()
        startPos += 1



# Uncomment this code to show the title screen and menu before starting the game:

# import sys
# sys.path.insert(0, "/".join(__file__.split("/")[0:-1]))
# import launch
# launch.mainMenu(startGame)

# Uncomment this code to just immediately start the game:

startGame()
