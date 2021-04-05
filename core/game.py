"""

"""
import os

from core.game_components.track import Track
from core.game_components.environment import Environment
from core.settings import *
from core.ui.engine import Engine
import keyboard

from random import randint

def prepareTrackSurface(engine: Engine, environment: Environment) -> Engine.Surface:
    """ 
    This function is called once per run, and it prepares the track's surface 
    so that recalculation of each component is not necessary every frame

    """ 
    track = environment.track

    # retrieves the coordinates for all points on the inside and outside edges of the track
    inner_edges = track.getInnerEdges()
    outer_edges = track.getOuterEdges()

    # create empty surfaces that will contain the inside/outside edges
    outer_surface = engine.Surface(SCREEN_SIZE, flag="srcalpha")
    inner_surface = engine.Surface(SCREEN_SIZE, flag="srcalpha")

    # draw the edges to the corresponding surfaces
    engine.renderPolygon((255, 255, 255), outer_edges, outer_surface)
    engine.renderPolygon((0, 0, 0), inner_edges, inner_surface)

    # load the texture that will be applied to the track
    texture = engine.load_image(TRACK_TEXTURE)
    texture = engine.tile_surface(texture)

    # remove the inside surface from the outside to create the track surface and apply the texture to the result
    outer_surface = (outer_surface - inner_surface).apply_texture(texture)

    return outer_surface



def PvAI():
    track = Track(type=TRACK_TYPE)
    engine = Engine(SCREEN_SIZE, (1, 1), checkered=False, imageFolder=os.path.join(os.getcwd(), "assets"))
    environment = Environment(track)
    track_surface = prepareTrackSurface(engine, environment)

    pts = []
    for i in range(100):
        pt = (randint(-200, 200) + TRACK_ORIGIN[0], randint(-200, 200) + TRACK_ORIGIN[1])
        pts.append(pt)

    while not keyboard.is_pressed('esc'):
        for step in range(1, SMOOTHNESS + 1):
            if engine.shouldRun():
                engine.clearScreen()
                engine.renderScene(_renderEnvironment, environment, track_surface, pts)
                engine.updateScreen()

    engine.exit()


    
def _renderEnvironment(engine: Engine, environment: Environment, track_surface: Engine.Surface, pts: list) -> None:
    """ 
    Contains all the instructions for the engine to render 
    the environment to the screen

    """
    engine.tileImageAsBackground(BACKGROUND)
    engine.renderSurface(track_surface)


    for pt in pts:
        if environment.trackContains(pt):
            engine.renderCircle(pt, 10, (0, 255, 0))
        else:
            engine.renderCircle(pt, 10, (255, 0, 0))
   # pt = (400, 400)







