import thumby

def startGame():
    # Snake image data is here
    snakeImages = bytearray([
        5,6,6,0,5,6,9,0,6,2,4,6,6,4,2,6,
        0,13,11,0,0,11,13,0,4,4,6,6,6,10,
        12,0,0,12,10,6,6,11,13,6,2,5,2,0,
        6,6,5,0,6,8,12,14,15,13,14,8
    ])
    snake = thumby.Sprite(4, 4, snakeImages)

    # Update every second
    thumby.display.setFPS(1)

    while(True):
        snake.x += 1
        snake.y += 1
        thumby.display.fill(0)
        thumby.display.drawSprite(snake)
        snake.setFrame(snake.currentFrame+1)
        thumby.display.update()


# Uncomment this code to show the title screen and menu before starting the game:

# import sys
# sys.path.insert(0, "/".join(__file__.split("/")[0:-1]))
# import launch
# launch.mainMenu(startGame)

# Uncomment this code to just immediately start the game:

startGame()
