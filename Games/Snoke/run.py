import pygameWrapper
from snoke import init, update

pygameWrapper.run(
    pygameWrapper, init, update, framerate=10, title="Snoke", windowscale=3
)
