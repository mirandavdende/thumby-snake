import engine_main
import engine
from engine_nodes import (
    Rectangle2DNode,
    CameraNode,
    Sprite2DNode,
)
from engine_math import Vector2, Vector3
from engine_draw import Color
from engine_resources import TextureResource, WaveSoundResource
import engine_io

from math import floor


class Key:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    A = 4
    B = 5
    MENU = 6
    SHOULDER_LEFT = 7
    SHOULDER_RIGHT = 8


class Sprite(Sprite2DNode):
    def __init__(self, spritesheet, width, height, position):
        super().__init__(self)
        self.transparent_color = Color(1, 0, 1)
        self.texture = spritesheet
        self.frame_count_x = spritesheet.width // width
        self.frame_count_y = spritesheet.height // height
        self.frame_current_x = 0
        self.frame_current_y = 0
        self.width = width
        self.height = height
        self.loop = False
        self.playing = False
        self.layer = 1
        self.setPosition(position)

    def setFrame(self, index):
        self.frame_current_x = index

    def show(self):
        self.opacity = 1

    def hide(self):
        self.opacity = 0

    def setPosition(self, position):
        self.real_position = position
        self.position = Vector2(
            position[0] + (self.width // 2), position[1] + (self.height // 2)
        )

    def getPosition(self):
        return [self.real_position[0], self.real_position[1]]

    def destroy(self):
        self.mark_destroy()


class Square(Rectangle2DNode):
    def __init__(self, x, y, width, height, color):
        super().__init__(
            Vector2(x + width // 2, y + height // 2),
            width,
            height,
            color_from_rgb(color[0], color[1], color[2]),
        )


class Scene(Rectangle2DNode):
    def __init__(self):
        super().__init__(Vector2(0, 0), screenWidth, screenHeight)

    def add(self, node):
        self.add_child(node)

    def show(self):
        self.opacity = 1
        for i in range(self.get_child_count()):
            self.get_child(i).opacity = 1

    def hide(self):
        self.opacity = 0
        for i in range(self.get_child_count()):
            self.get_child(i).opacity = 0

    def remove_children(self):
        for i in range(self.get_child_count()):
            self.remove_child(self.get_child(i))


def color_from_rgb(r, g, b):
    return Color(((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3))


def load_image(file):
    return TextureResource(file)


def load_sound(file):
    return WaveSoundResource(file)


def exit():
    engine.reset()


def run(
    system,
    init_func,
    update_func,
    framerate=60,
    width=128,
    height=128,
    spritescale=1.0,
    windowscale=1,
    title="Thumby Pygame Wrapper",
):
    global screenWidth, screenHeight
    screenWidth = width
    screenHeight = height

    engine.fps_limit(framerate)
    cam = CameraNode(Vector3(64, 64, 0))
    init_func(system)

    while True:
        if not engine.tick():
            continue

        keys = []
        if engine_io.A.is_just_pressed:
            keys.append(Key.A)
        if engine_io.B.is_just_pressed:
            keys.append(Key.B)
        if engine_io.UP.is_just_pressed:
            keys.append(Key.UP)
        if engine_io.DOWN.is_just_pressed:
            keys.append(Key.DOWN)
        if engine_io.LEFT.is_just_pressed:
            keys.append(Key.LEFT)
        if engine_io.RIGHT.is_just_pressed:
            keys.append(Key.RIGHT)
        if engine_io.MENU.is_just_pressed:
            keys.append(Key.MENU)
        if engine_io.LB.is_just_pressed:
            keys.append(Key.SHOULDER_LEFT)
        if engine_io.RB.is_just_pressed:
            keys.append(Key.SHOULDER_RIGHT)

        new_rate = update_func(keys)
        engine.fps_limit(new_rate or framerate)
