"""

"""
from core.game_components.track import Track
from core.settings import *
import numpy as np

class Environment:
    def __init__(self, track: Track) -> None:
        self.track = track
        self.starting_point = self.prepareTrack()


    def prepareTrack(self) -> None:
        """ 
        Scales the track to the proper size and moves it to
        the center of the map based on variables in Settings

        """
        inner_edges = self.track.getInnerEdges()
        outer_edges = self.track.getOuterEdges()
        inner_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), inner_edges))
        outer_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), outer_edges))

        inner_start_point = inner_edges[0]
        outer_start_point = outer_edges[0]

        starting_point = ((inner_start_point[0] + outer_start_point[0]) / 2, (inner_start_point[1] + outer_start_point[1]) / 2)

        self.track.setFinalEuclidean(np.array([inner_edges, outer_edges]))
        return starting_point

    def trackContains(self, pt: tuple) -> bool:
        """ 
        Determines whether a given point resides inside the track

        """ 
        #print(TRACK_ORIGIN)
        #pt = (pt[0] / TRACK_SCALE - TRACK_ORIGIN[0], pt[1] / TRACK_SCALE - TRACK_ORIGIN[1])
        pt = ((pt[0] - TRACK_ORIGIN[0]) / TRACK_SCALE, (pt[1] - TRACK_ORIGIN[1]) / TRACK_SCALE)
        #pt = (pt[0] / TRACK_SCALE, pt[1] / TRACK_SCALE)
        return self.track.contains(pt)


