import thumby

# Show title screen

titleScreen = bytearray([
    255,63,15,7,131,193,193,224,225,255,255,3,3,3,3,15,127,255,15,1,1,225,127,31,3,3,193,1,3,127,127,227,1,1,7,63,31,15,3,193,3,7,1,97,112,112,241,255,255,15,119,119,55,59,251,251,27,29,157,129,195,1,254,254,192,193,239,239,239,207,31,63,
    248,56,56,57,25,25,9,0,128,192,128,143,192,192,254,252,240,224,224,224,192,131,128,192,240,243,249,248,192,64,96,127,112,96,160,160,48,32,163,103,127,112,64,64,230,226,227,241,241,255,254,254,255,0,63,159,128,192,255,255,255,192,207,207,225,240,252,224,231,231,240,248,
    255,254,252,252,254,254,255,255,255,255,255,127,159,79,47,87,39,87,163,83,43,21,169,213,201,213,201,181,184,169,42,169,168,191,217,90,41,152,239,251,107,37,175,142,33,87,39,143,159,191,191,191,191,127,127,255,255,255,127,127,255,255,255,255,255,255,255,255,255,255,255,255,
    63,63,63,63,127,127,255,135,43,85,169,84,168,86,167,17,72,212,200,20,201,23,136,147,43,147,7,255,59,157,200,231,115,57,156,206,103,243,25,228,242,249,28,110,151,115,211,129,149,169,149,129,165,131,191,190,129,68,146,51,6,29,249,195,13,179,207,255,255,255,255,255,
    0,0,0,0,0,0,0,1,1,3,2,6,12,25,50,37,106,84,75,82,74,99,55,39,54,30,115,204,159,191,179,112,118,111,105,104,104,89,83,86,93,75,103,126,124,184,194,86,86,86,86,86,86,86,86,66,84,66,68,96,200,144,128,159,207,96,63,7,3,1,0,0
])

title = thumby.Sprite(72, 40, titleScreen)
thumby.display.drawSprite(title)
thumby.display.update()

# Wait for user input & fill canvas to black

while not (thumby.buttonA.pressed() or thumby.buttonB.pressed() or thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonL.pressed() or thumby.buttonR.pressed()):
    pass

thumby.display.fill(1)

# Draw snake

snakeImages = bytearray([
    10,9,9,15,10,9,6,15,9,13,11,9,9,11,
    13,9,15,2,4,15,15,4,2,15,11,11,9,9,
    9,5,3,15,15,3,5,9,9,4,2,9,13,10,13,
    15,9,9,10,15,9,7,3,1,0,2,1,7
])

snake = thumby.Sprite(4, 4, snakeImages)
snake.x = 2
snake.y = 2
thumby.display.drawSprite(snake)
thumby.display.update()