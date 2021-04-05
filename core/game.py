"""

"""
import os

from core.game_components.track import Track
from core.game_components.environment import Environment
from core.settings import *
from core.ui.engine import Engine
import keyboard

def PvAI():
    track = Track(type=TRACK_TYPE)
    engine = Engine(SCREEN_SIZE, (1, 1), checkered=False, imageFolder=os.path.join(os.getcwd(), "assets"))
    environment = Environment(track)

    while not keyboard.is_pressed('esc'):
        for step in range(1, SMOOTHNESS + 1):
            if engine.shouldRun():
                engine.clearScreen()
                engine.renderScene(_renderEnvironment, environment)
                engine.updateScreen()

    engine.exit()


    
def _renderEnvironment(engine: Engine, environment: Environment):
    track = environment.track

    engine.tileImageAsBackground("grass.png")
    #texture = engine.Image("texture2.png")
    texture = engine.load_image("texture2.png")
    texture = engine.tile_surface(texture)
    inner_edges = track.getInnerEdges()
    outer_edges = track.getOuterEdges()

    inner_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), inner_edges))
    outer_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), outer_edges))

    outer_surface = engine.Surface(SCREEN_SIZE, flag="srcalpha")
    inner_surface = engine.Surface(SCREEN_SIZE, flag="srcalpha")


    engine.renderPolygon((255, 255, 255), outer_edges, outer_surface)
    engine.renderPolygon((0, 0, 0), inner_edges, inner_surface)

    outer_surface = (outer_surface - inner_surface).apply_texture(texture)
    engine.renderSurface(outer_surface.surface)






