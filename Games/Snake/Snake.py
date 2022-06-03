import sys
sys.path.insert(0, "/".join(__file__.split("/")[0:-1]))
import menu
import thumby

def waitForKey():
    while not (thumby.buttonA.pressed() or thumby.buttonB.pressed() or thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonL.pressed() or thumby.buttonR.pressed()):
        pass
    while (thumby.buttonA.pressed() or thumby.buttonB.pressed() or thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonL.pressed() or thumby.buttonR.pressed()):
        pass

# Show title screen

titleScreen = bytearray([
    224,56,12,6,131,193,193,225,161,191,254,2,2,2,2,14,120,248,15,1,1,225,127,30,2,3,193,1,3,30,126,195,1,1,7,60,24,14,3,193,35,31,1,97,113,81,209,31,248,12,116,116,54,58,250,250,27,29,157,129,195,3,253,253,193,195,238,232,232,200,24,240,
    231,44,40,56,24,24,8,0,128,192,65,97,94,64,126,28,48,32,32,96,224,159,128,192,112,19,25,248,192,64,64,99,126,96,160,160,56,32,163,103,127,112,64,64,230,34,35,49,17,31,2,2,255,0,63,159,128,192,127,0,127,64,79,79,97,48,60,32,39,39,48,31,
    3,6,4,4,6,2,3,1,1,0,192,112,152,72,44,84,36,86,162,82,43,21,169,213,73,85,201,181,184,169,42,169,168,191,217,90,41,152,239,251,107,37,175,142,33,87,36,140,152,176,160,160,161,97,65,193,128,192,64,64,192,128,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,252,134,43,85,169,84,168,86,167,17,72,212,200,20,201,23,136,147,42,146,6,254,59,157,200,231,115,57,156,206,103,243,25,228,242,249,28,110,151,115,211,129,149,169,149,129,165,131,191,190,129,68,146,51,6,29,249,195,13,179,206,120,0,0,0,0,
    0,0,0,0,0,0,0,1,1,3,2,6,12,25,50,37,106,84,75,82,74,99,55,39,54,30,115,204,159,191,179,112,118,111,105,104,104,89,83,86,93,75,103,126,124,184,194,86,86,86,86,86,86,86,86,66,84,66,68,96,200,144,128,159,207,96,63,0,0,0,0,0
])

title = thumby.Sprite(72, 40, titleScreen)
thumby.display.drawSprite(title)
thumby.display.update()
waitForKey()

# Show the menu

newGameSprite = thumby.Sprite(49, 8, bytearray([127,126,12,24,63,127,0,56,124,84,92,88,0,28,124,96,56,96,124,28,0,0,0,62,127,65,121,120,0,32,116,84,124,120,0,124,124,4,124,124,4,124,120,0,56,124,84,92,88]))
optionsSprite = thumby.Sprite(36, 8, bytearray([62,127,65,65,127,62,0,252,252,36,60,24,0,63,127,68,0,125,125,0,56,124,68,124,56,0,124,124,4,124,120,0,88,92,116,52]))
quitSprite    = thumby.Sprite(19,8, bytearray([62,127,65,97,255,190,0,60,124,64,124,124,0,125,125,0,63,127,68]))

controlsSprite        = thumby.Sprite(40, 8, bytearray([62,127,65,65,65,0,56,124,68,124,56,0,124,124,4,124,120,0,63,127,68,0,124,124,8,12,0,56,124,68,124,56,0,127,127,0,88,92,116,52]))
controlDPadSprite     = thumby.Sprite(23, 8, bytearray([127,65,65,65,62,0,16,16,0,252,36,36,24,0,32,84,84,120,0,56,68,68,127]))
controlSnakeSprite    = thumby.Sprite(48, 17, bytearray([0,0,0,0,0,0,0,0,127,64,64,64,0,56,84,84,24,0,126,5,0,63,68,0,0,0,32,84,84,120,0,124,4,4,120,0,56,68,68,127,0,0,0,126,17,17,17,126,144,168,168,72,0,126,136,0,112,168,168,48,0,112,168,168,48,0,248,16,24,0,0,0,144,168,168,72,0,248,8,8,240,0,64,168,168,240,0,254,32,80,136,0,112,168,168,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
controlDiagonalSprite = thumby.Sprite(57, 17, bytearray([0,0,0,0,0,0,127,64,64,64,0,56,84,84,24,0,126,5,0,63,68,0,0,0,20,20,20,0,0,0,60,64,64,60,0,252,36,36,24,0,112,28,7,0,1,127,0,56,84,84,24,0,126,5,0,63,68,252,34,34,34,252,0,0,0,40,40,40,0,0,0,112,136,136,254,0,112,136,136,112,0,120,128,96,128,120,0,248,8,8,240,0,224,56,14,0,248,16,24,0,250,0,48,72,72,248,0,254,8,8,240,0,126,136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]))

settings = {
    "controls": 0
}

def quitGame():
    thumby.reset()

def getControlSetting():
    global settings
    return settings["controls"]

def setControlSetting(value):
    global settings
    settings["controls"] = value

def optionsMenu():
    menu.SettingsMenu([
        menu.Setting(controlsSprite, getControlSetting, [
            menu.Item(controlDPadSprite,     setControlSetting),
            menu.Item(controlSnakeSprite,    setControlSetting),
            menu.Item(controlDiagonalSprite, setControlSetting)
        ])
    ]).start()


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


while True:
    menu.ListMenu([
        menu.Item(newGameSprite, startGame),
        menu.Item(optionsSprite, optionsMenu),
        menu.Item(quitSprite,    quitGame)
    ]).start()
