"""illustrt

"""
from core.game_components.track import Track
from core.game_components.racecar import Racecar
from core.settings import *
import numpy as np

class Environment:
    def __init__(self, track: Track) -> None:
        self.track = track
        start_point, start_d = self.prepareTrack()
        self.car = Racecar(controller_type = "player", 
                           initial_pos = start_point,
                           initial_direction = start_d,
                           initial_dist = -self.track.getTheta(self.scale(start_point)))

    def step(self) -> None:
        """ 
        Moves game state a time step forward

        """
        pt = self.scale(self.car.p)
        c0 = self.track.getTheta(pt)
        self.car.step(None, (pt in self.track), (2 * np.pi) - c0)

    def getCar(self) -> Racecar:
        return self.car

    def prepareTrack(self) -> tuple:
        """ 
        Scales the track to the proper size and moves it to
        the center of the map based on variables in Settings

        Also finds the starting point of the track and 
        the initial angle of the track to send to the 
        cars.

        """
        inner_edges = self.track.getInnerEdges()
        outer_edges = self.track.getOuterEdges()

        inner_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), inner_edges))
        outer_edges = list(map(lambda x: (x[0] * TRACK_SCALE + TRACK_ORIGIN[0], x[1] * TRACK_SCALE + TRACK_ORIGIN[1]), outer_edges))

        inner_start_point = inner_edges[2]
        outer_start_point = outer_edges[2]

        x = inner_edges[0][0] - inner_edges[2][0]
        y = inner_edges[0][1] - inner_edges[2][1]

        starting_d = np.array([x / np.sqrt(x**2 + y**2), y / np.sqrt(x**2 + y**2)])
        starting_point = np.array([(inner_start_point[0] + outer_start_point[0]) / 2, (inner_start_point[1] + outer_start_point[1]) / 2])

        self.track.setFinalEuclidean(np.array([inner_edges, outer_edges]))
        return starting_point, starting_d

    def trackContains(self, pt: tuple) -> bool:
        """ 
        Determines whether a given point resides inside the track

        """ 
        return self.scale(pt) in self.track

    def scale(self, pt: tuple) -> tuple:
        """ 
        Shifts and scales the given point to 
        be centered at the origin of the track.

        """ 
        return ((pt[0] - TRACK_ORIGIN[0]) / TRACK_SCALE, (pt[1] - TRACK_ORIGIN[1]) / TRACK_SCALE)


