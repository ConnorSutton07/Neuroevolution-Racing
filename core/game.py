"""

"""
from core.game_components.track import Track
from core.game_components.environment import Environment
from core.settings import *
from core.ui.engine import Engine


def PvAI():
    track = Track(type=TRACK_TYPE)
    engine = Engine(SCREEN_SIZE, (1, 1), checkered=False)
    environment = Environment(track)

    while True:
        for step in range(1, SMOOTHNESS + 1):
            if engine.shouldRun():
                engine.clearScreen()
                engine.renderScene(_renderEnvironment, environment)
                engine.updateScreen()


    
def _renderEnvironment(engine: Engine, environment: Environment):
    track = environment.track

    engine.tileImageAsBackground("assets/grass.png")
    #inner_edges = track.getInnerEdges()
    #outer_edges = track.getOuterEdges()






