import thumby

scrollBarHandle = thumby.Sprite(3, 7, bytearray([65,65,62]), 68)
selectText = thumby.Sprite(28, 7, bytearray([70,79,121,49,0,56,124,84,92,88,0,127,127,0,56,124,84,92,88,0,56,124,68,68,0,63,127,68]), 22, 33)

class Menu:

    def __init__(self, menu):
        self.menu = menu

    def _waitForNewKeyPress(self):
        while thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonA.pressed() or thumby.buttonB.pressed():
            pass
        while not (thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonA.pressed() or thumby.buttonB.pressed()):
            pass

    def _drawScrollBar(self, pos, total):
        disp = thumby.display.display.buffer
        for offset in range(68, 213, 72):
            disp[offset] = 0xFF
        disp[284] = 0b00111111
        if total > 1:
            scrollBarHandle.y = pos / (total - 1) * 23
        else:
            scrollBarHandle.y = 0
        thumby.display.drawSprite(scrollBarHandle)

class ListMenu(Menu):

    def start(self):
        selected = 0
        scrollPos = 0
        diff = 2 if len(self.menu) >= 2 else len(self.menu)
        while True:
            self._drawListTypeMenu(scrollPos, scrollPos + diff, selected)
            self._waitForNewKeyPress()
            if thumby.buttonB.pressed():
                return
            if thumby.buttonU.pressed():
                selected -= 1
                if selected < 0:
                    selected = len(self.menu) - 1
            if thumby.buttonD.pressed():
                selected += 1
                if selected == len(self.menu):
                    selected = 0
            if thumby.buttonA.pressed():
                self.menu[selected].function()
            while selected > scrollPos + 2:
                scrollPos += 1
            while selected < scrollPos:
                scrollPos -= 1

    def _drawListTypeMenu(self, start, end, selected):
        thumby.display.fill(0)
        y = 1
        for i in range(start, end + 1):
            sprite = self.menu[i].sprite
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

        self._drawScrollBar(selected, len(self.menu))
        thumby.display.drawSprite(selectText)
        thumby.display.update()

class SettingsMenu(Menu):

    def start(self):
        selected = 0
        while True:
            option = self.menu[selected].function()
            self._drawSettingsTypeMenu(selected, option)
            self._waitForNewKeyPress()
            if thumby.buttonB.pressed():
                return
            if thumby.buttonU.pressed():
                selected -= 1
                if selected < 0:
                    selected = len(self.menu) - 1
            if thumby.buttonD.pressed():
                selected += 1
                if selected == len(self.menu):
                    selected = 0
            if thumby.buttonA.pressed():
                numOptions = len(self.menu[selected].options)
                nextOption = (option + 1) % numOptions
                self.menu[selected].options[nextOption].function(nextOption)

    def _drawSettingsTypeMenu(self, selected, option):
        thumby.display.fill(0)

        setting = self.menu[selected].sprite
        setting.x = 2
        setting.y = 1
        thumby.display.drawSprite(setting)

        value = self.menu[selected].options[option].sprite
        value.x = 65 - value.width
        value.y = 29 - value.height
        thumby.display.drawSprite(value)

        self._drawScrollBar(selected, len(self.menu))
        thumby.display.drawSprite(selectText)
        thumby.display.update()

class Item:
    def __init__(self, sprite, function):
        self.sprite = sprite
        self.function = function

class Setting:
    def __init__(self, sprite, function, options):
        self.sprite = sprite
        self.function = function
        self.options = options
