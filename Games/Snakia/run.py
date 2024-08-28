import wrapper_pygame
from snakia import init, update

wrapper_pygame.run(
    wrapper_pygame, init, update, framerate=10, title="Snakia", windowscale=3
)
