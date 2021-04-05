"""

"""
from core.game_components.track import Track
from core.settings import *
import numpy as np

class Environment:
    def __init__(self, track: Track) -> None:
        self.track = track
        self.prepareTrack()


    def prepareTrack(self) -> None:
        """ 
        Scales the track to the proper size and moves it to
        the center of the map based on variables in Settings

        """
        inner_edges = self.track.getInnerEdges()
        outer_edges = self.track.getOuterEdges()
        inner_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), inner_edges))
        outer_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), outer_edges))

        self.track.setFinalEuclidean(np.array([inner_edges, outer_edges]))


    