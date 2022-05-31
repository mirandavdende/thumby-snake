import thumby

scrollBarHandle = thumby.Sprite(3, 7, bytearray([65,65,62]), 68)
selectText = thumby.Sprite(28, 7, bytearray([70,79,121,49,0,56,124,84,92,88,0,127,127,0,56,124,84,92,88,0,56,124,68,68,0,63,127,68]), 22, 33)

# Draw a list type menu with the following structure:
# [
#   [ sprite, pointer to function ],
#   ...
# ]
def listType(menu):
    selected = 0
    scrollPos = 0
    diff = 2 if len(menu) >= 2 else len(menu)
    while True:
        drawListTypeMenu(menu, scrollPos, scrollPos + diff, selected)
        waitForNewKeyPress()
        if thumby.buttonB.pressed():
            return
        if thumby.buttonU.pressed():
            selected -= 1
            if selected < 0:
                selected = len(menu) - 1
        if thumby.buttonD.pressed():
            selected += 1
            if selected == len(menu):
                selected = 0
        if thumby.buttonA.pressed():
            menu[selected][1]()
        while selected > scrollPos + 2:
            scrollPos += 1
        while selected < scrollPos:
            scrollPos -= 1

def drawListTypeMenu(menu, start, end, selected):
    thumby.display.fill(0)
    y = 1
    for i in range(start, end + 1):
        sprite = menu[i][0]
        if i == selected:
            thumby.display.drawFilledRectangle(0, y - 1, 65, 10, 1)
            inverted = bytearray(sprite.bitmapByteCount)
            for j in range(sprite.bitmapByteCount):
                inverted[j] = sprite.bitmap[j] ^ 0xFF
            thumby.display.blit(inverted, 2, y, sprite.width, sprite.height, -1, 0, 0)
        else:
            sprite.x = 2
            sprite.y = y
            thumby.display.drawSprite(sprite)
        y += sprite.height + 2

    drawScrollBar(selected, len(menu))
    thumby.display.drawSprite(selectText)
    thumby.display.update()

# Draw a settings type menu with the following structure:
# [
#   [ sprite, pointer to current option function,
#     [
#       [ sprite, pointer to set option function ],
#       ...
#     ]
#   ],
#   ...
# ]
def settingsType(menu):
    selected = 0
    while True:
        option = menu[selected][1]()
        drawSettingsTypeMenu(menu, selected, option)
        waitForNewKeyPress()
        if thumby.buttonB.pressed():
            return
        if thumby.buttonU.pressed():
            selected -= 1
            if selected < 0:
                selected = len(menu) - 1
        if thumby.buttonD.pressed():
            selected += 1
            if selected == len(menu):
                selected = 0
        if thumby.buttonA.pressed():
            numOptions = len(menu[selected][2])
            nextOption = (option + 1) % numOptions
            menu[selected][2][nextOption][1]()

def drawSettingsTypeMenu(menu, selected, option):
    thumby.display.fill(0)

    setting = menu[selected][0]
    setting.x = 2
    setting.y = 1
    thumby.display.drawSprite(setting)

    value = menu[selected][2][option][0]
    value.x = 65 - value.width
    value.y = 29 - value.height
    thumby.display.drawSprite(value)

    drawScrollBar(selected, len(menu))
    thumby.display.drawSprite(selectText)
    thumby.display.update()

# Generic helper functions

def waitForNewKeyPress():
    while thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonA.pressed() or thumby.buttonB.pressed():
        pass
    while not (thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonA.pressed() or thumby.buttonB.pressed()):
        pass

def drawScrollBar(pos, total):
    disp = thumby.display.display.buffer
    for offset in range(68, 213, 72):
        disp[offset] = 0xFF
    disp[284] = 0b00111111
    if total > 1:
        scrollBarHandle.y = pos / (total - 1) * 23
    else:
        scrollBarHandle.y = 0
    thumby.display.drawSprite(scrollBarHandle)







def startGame():
    print("Starting new game!")

def quitGame():
    print("Exiting game")

controlSetting = 0

def getControlSetting():
    global controlSetting
    return controlSetting

def selectControlDpad():
    global controlSetting
    controlSetting = 0

def selectControlSnake():
    global controlSetting
    controlSetting = 1

def selectControlDiagonal():
    global controlSetting
    controlSetting = 2

controlsSprite        = thumby.Sprite(40, 8, bytearray([62,127,65,65,65,0,56,124,68,124,56,0,124,124,4,124,120,0,63,127,68,0,124,124,8,12,0,56,124,68,124,56,0,127,127,0,88,92,116,52]))
controlDPadSprite     = thumby.Sprite(23, 8, bytearray([127,65,65,65,62,0,16,16,0,252,36,36,24,0,32,84,84,120,0,56,68,68,127]))
controlSnakeSprite    = thumby.Sprite(48, 17, bytearray([0,0,0,0,0,0,0,0,127,64,64,64,0,56,84,84,24,0,126,5,0,63,68,0,0,0,32,84,84,120,0,124,4,4,120,0,56,68,68,127,0,0,0,126,17,17,17,126,144,168,168,72,0,126,136,0,112,168,168,48,0,112,168,168,48,0,248,16,24,0,0,0,144,168,168,72,0,248,8,8,240,0,64,168,168,240,0,254,32,80,136,0,112,168,168,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
controlDiagonalSprite = thumby.Sprite(57, 17, bytearray([0,0,0,0,0,0,127,64,64,64,0,56,84,84,24,0,126,5,0,63,68,0,0,0,20,20,20,0,0,0,60,64,64,60,0,252,36,36,24,0,112,28,7,0,1,127,0,56,84,84,24,0,126,5,0,63,68,252,34,34,34,252,0,0,0,40,40,40,0,0,0,112,136,136,254,0,112,136,136,112,0,120,128,96,128,120,0,248,8,8,240,0,224,56,14,0,248,16,24,0,250,0,48,72,72,248,0,254,8,8,240,0,126,136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]))

def optionsMenu():
    settingsType([
        [
            controlsSprite, getControlSetting,
            [
                [ controlDPadSprite,     selectControlDpad     ],
                [ controlSnakeSprite,    selectControlSnake    ],
                [ controlDiagonalSprite, selectControlDiagonal ]
            ]
        ]
    ])

newGameSprite = thumby.Sprite(49, 8, bytearray([127,126,12,24,63,127,0,56,124,84,92,88,0,28,124,96,56,96,124,28,0,0,0,62,127,65,121,120,0,32,116,84,124,120,0,124,124,4,124,124,4,124,120,0,56,124,84,92,88]))
optionsSprite = thumby.Sprite(36, 8, bytearray([62,127,65,65,127,62,0,252,252,36,60,24,0,63,127,68,0,125,125,0,56,124,68,124,56,0,124,124,4,124,120,0,88,92,116,52]))
quitSprite    = thumby.Sprite(19,8, bytearray([62,127,65,97,255,190,0,60,124,64,124,124,0,125,125,0,63,127,68]))

listType([
    [ newGameSprite, startGame   ],
    [ optionsSprite, optionsMenu ],
    [ quitSprite,    quitGame    ]
])
