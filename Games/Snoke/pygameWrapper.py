#!/usr/bin/env python

import os
import pygame as pg
from math import floor

main_dir = os.path.split(os.path.abspath(__file__))[0]


# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


class Key:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    A = 4
    B = 5


entities = []


class Sprite(pg.sprite.Sprite):
    def __init__(self, spritesheet, width, height, position):
        global entities
        pg.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.image = pg.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.setFrame(0)
        self.visible = True
        self.setPosition(position)
        entities.append(self)

    def setFrame(self, index):
        rect = pg.Rect((index * self.rect.width, 0, self.rect.width, self.rect.height))
        self.image.blit(self.spritesheet, (0, 0), rect)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def setPosition(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def getPosition(self):
        return [self.rect.x, self.rect.y]

    def destroy(self):
        global entities
        entities.remove(self)

    def _draw(self):
        if not self.visible:
            return
        global display
        display.blit(self.image, self.rect)


class Square:
    def __init__(self, x, y, width, height, color):
        global entities
        self.color = color
        self.rect = pg.Rect(x, y, width, height)
        entities.append(self)

    def _draw(self):
        global display
        pg.draw.rect(display, self.color, self.rect)


def load_image(file):
    file = os.path.join(main_dir, file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def load_sound(file):
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print(f"Warning, unable to load, {file}")
    return None


def run(
    system,
    init_func,
    update_func,
    framerate=60,
    width=128,
    height=128,
    spritescale=1.0,
    windowscale=4,
    title="Thumby Pygame Wrapper",
):
    global display, screenWidth, screenHeight
    screenWidth = width
    screenHeight = height

    pg.init()

    windowSize = pg.Rect(0, 0, floor(width * windowscale), floor(height * windowscale))
    gameScreenSize = pg.Rect(0, 0, width, height)

    winStyle = 0
    bestdepth = pg.display.mode_ok(windowSize.size, winStyle, 32)
    screen = pg.display.set_mode(windowSize.size, winStyle, bestdepth)
    display = pg.Surface(gameScreenSize.size)
    display.fill((0, 0, 0))

    pg.display.set_caption(title)
    clock = pg.time.Clock()
    init_func(system)

    while 1:
        keys = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return pg.quit()
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_ESCAPE:
                        return pg.quit()
                    case pg.K_UP:
                        keys.append(Key.UP)
                    case pg.K_DOWN:
                        keys.append(Key.DOWN)
                    case pg.K_LEFT:
                        keys.append(Key.LEFT)
                    case pg.K_RIGHT:
                        keys.append(Key.RIGHT)
                    case pg.K_SPACE:
                        keys.append(Key.A)
                    case pg.K_LCTRL | pg.K_RCTRL:
                        keys.append(Key.B)

        newRate = update_func(keys)

        for entity in entities:
            entity._draw()
        screen.blit(pg.transform.scale(display, screen.get_rect().size), (0, 0))
        pg.display.flip()
        clock.tick(newRate or framerate)
