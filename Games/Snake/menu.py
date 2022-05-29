import thumby

scrollBarHandle = thumby.Sprite(3, 7, bytearray([65,65,62]), 68)
selectText = thumby.Sprite(28, 7, bytearray([70,79,121,49,0,56,124,84,92,88,0,127,127,0,56,124,84,92,88,0,56,124,68,68,0,63,127,68]), 22, 33)

# Draw a list type menu with the following structure:
# [
#   [ width, height, pointer to function, bitmap ],
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
            menu[selected][2]()
        while selected > scrollPos + 2:
            scrollPos += 1
        while selected < scrollPos:
            scrollPos -= 1

def drawListTypeMenu(menu, start, end, selected):
    thumby.display.fill(0)
    y = 1
    for i in range(start, end + 1):
        if i == selected:
            thumby.display.drawFilledRectangle(0, y - 1, 65, 10, 1)
            inverted = bytearray(len(menu[i][3]))
            for j in range(len(inverted)):
                inverted[j] = menu[i][3][j] ^ 0xFF
            thumby.display.blit(inverted, 2, y, menu[i][0], menu[i][1], -1, 0, 0)
        else:
            thumby.display.blit(menu[i][3], 2, y, menu[i][0], menu[i][1], -1, 0, 0)
        y += menu[i][1] + 2

    drawScrollBar(selected, len(menu))
    thumby.display.drawSprite(selectText)
    thumby.display.update()

# Draw a settings type menu with the following structure:
# [
#   [ width, height, pointer to current option function, bitmap,
#     [
#       [ width, height, pointer to set option function, bitmap ],
#       ...
#     ]
#   ],
#   ...
# ]
def settingsType(menu):
    selected = 0
    while True:
        option = menu[selected][2]()
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
            numOptions = len(menu[selected][4])
            nextOption = (option + 1) % numOptions
            menu[selected][4][nextOption][2]()

def drawSettingsTypeMenu(menu, selected, option):
    thumby.display.fill(0)
    thumby.display.blit(menu[selected][3], 2, 1, menu[selected][0], menu[selected][1], -1, 0, 0)
    currentOption = menu[selected][4][option]
    thumby.display.blit(currentOption[3], 65 - currentOption[0], 29 - currentOption[1], currentOption[0], currentOption[1], -1, 0, 0)
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

def optionsMenu():
    settingsType([
        [
            40, 8, getControlSetting, bytearray([62,127,65,65,65,0,56,124,68,124,56,0,124,124,4,124,120,0,63,127,68,0,124,124,8,12,0,56,124,68,124,56,0,127,127,0,88,92,116,52]),
            [
                [ 23, 8, selectControlDpad, bytearray([127,65,65,65,62,0,16,16,0,252,36,36,24,0,32,84,84,120,0,56,68,68,127]) ],
                [ 48, 17, selectControlSnake, bytearray([0,0,0,0,0,0,0,0,127,64,64,64,0,56,84,84,24,0,126,5,0,63,68,0,0,0,32,84,84,120,0,124,4,4,120,0,56,68,68,127,0,0,0,126,17,17,17,126,144,168,168,72,0,126,136,0,112,168,168,48,0,112,168,168,48,0,248,16,24,0,0,0,144,168,168,72,0,248,8,8,240,0,64,168,168,240,0,254,32,80,136,0,112,168,168,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) ],
                [ 57, 17, selectControlDiagonal, bytearray([0,0,0,0,0,0,127,64,64,64,0,56,84,84,24,0,126,5,0,63,68,0,0,0,20,20,20,0,0,0,60,64,64,60,0,252,36,36,24,0,112,28,7,0,1,127,0,56,84,84,24,0,126,5,0,63,68,252,34,34,34,252,0,0,0,40,40,40,0,0,0,112,136,136,254,0,112,136,136,112,0,120,128,96,128,120,0,248,8,8,240,0,224,56,14,0,248,16,24,0,250,0,48,72,72,248,0,254,8,8,240,0,126,136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0]) ]
            ]
        ]
    ])

def quitGame():
    print("Exiting game")

listType([
    # New Game
    [ 49, 8, startGame, bytearray([127,126,12,24,63,127,0,56,124,84,92,88,0,28,124,96,56,96,124,28,0,0,0,62,127,65,121,120,0,32,116,84,124,120,0,124,124,4,124,124,4,124,120,0,56,124,84,92,88]) ],
    # Options
    [ 36, 8, optionsMenu, bytearray([62,127,65,65,127,62,0,252,252,36,60,24,0,63,127,68,0,125,125,0,56,124,68,124,56,0,124,124,4,124,120,0,88,92,116,52]) ],
    # Quit
    [ 19, 8, quitGame, bytearray([62,127,65,97,255,190,0,60,124,64,124,124,0,125,125,0,63,127,68]) ]
])
