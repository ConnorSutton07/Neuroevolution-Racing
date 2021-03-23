"""
Generates the racing environment.

"""

import numpy as np
import math
from random import randint, sample, random, gauss
from scipy import interpolate
from scipy.spatial import ConvexHull
from math import atan2, sqrt
from core.constants import * 
import pygame

class Track:
    def __init__(self, 
                 width: int = WIDTH, 
                 height: int = HEIGHT) -> None:
        self.width = width
        self.height = height
        self.radius = TRACK_WIDTH // 2

        self.track_color = TRACK_COLOR
        self.point_count = randint(MIN_POINTS, MAX_POINTS)
        self.original_points = self.GetOriginalPoints()
        self.hull = self.GetHull()
        self.track_points = self.GenerateTrackPoints(self.hull, self.original_points)
        self.shaped_points = self.GetShapedPoints(self.track_points)
        self.smoothed_points = self.GetSmoothedPoints(self.track_points)

    def GenerateTrackPoints(self, hull: ConvexHull, points: list) -> list:
        track_points = get_track_points(hull, points)
        return track_points

    def GetShapedPoints(self, points: list) -> list:
        return shape_track(points)

    def GetSmoothedPoints(self, points: list) -> list:
        return smooth_track(points)

    def GetOriginalPoints(self) -> list:
        """
        Generates a list of points that will be used to construct
        a convex polygon.

        """
        xs = sample(range(OFFSET[0], self.width + OFFSET[0]), self.point_count)
        ys = sample(range(OFFSET[1], self.height + OFFSET[1]), self.point_count)
        return list(zip(xs, ys))
    
    def GetHull(self) -> ConvexHull:
        """
        returns a Hull object (convex polygon) based on random distribution of points

        """
        return ConvexHull(self.original_points)

    
    def Draw(self, surface: pygame.Surface, debug: bool = False) -> None:
        radius = self.radius
        segment_dims = (radius * 2, radius * 2)
        for point in self.smoothed_points:
            blit_pos = (point[0] - radius, point[1] - radius)
            track_segment = pygame.Surface(segment_dims, pygame.SRCALPHA)
            pygame.draw.circle(track_segment, self.track_color, (radius, radius), radius)
            surface.blit(track_segment, blit_pos)
        if debug:
            self.DrawPoints(surface, self.original_points, color=LINE_COLOR)
            self.DrawHull(surface, width=3)
            #self.DrawPoints(surface, self.track_points, color=BLACK, radius=5)
            #self.DrawPoints(surface, self.shaped_points, color=WHITE, radius=10)

    
    def DrawPoints(self, surface: pygame.Surface, points: list, color: tuple = BLACK, radius: int = 10) -> None:
        for p in points:
            #print(p)
            pygame.draw.circle(surface, color, (p[0], p[1]), radius)

    def DrawHull(self, surface: pygame.Surface, color: tuple = LINE_COLOR, width: int = 1) -> None:
        hull = self.hull
        points = self.original_points
        for i in range(len(hull.vertices) - 1):
            pygame.draw.line(surface, color, points[hull.vertices[i]], points[hull.vertices[i+1]], width=width)
            # close polygon
            if i == len(hull.vertices) - 2:
                pygame.draw.line(surface, color, points[hull.vertices[0]], points[hull.vertices[-1]], width=width)

    #def DrawStartingGrid()



def get_track_points(hull: ConvexHull, points: np.array) -> np.array:
    """ 
    Retrieves the original points from the random set
    that are used in the hull
    
    """
    return np.array([points[hull.vertices[i]] for i in range(len(hull.vertices))])

def make_rand_vector(dimensions: int) -> list:
    """
    Creates a unit vector of N dimensions in Gaussian distribution with
    mu = 0 and sigma = 1

    """
    vec = [gauss(0, 1) for i in range(dimensions)]
    mag = sqrt(sum(x**2 for x in vec))
    return [(x / mag) for x in vec]


def shape_track(track_points: np.array, 
                difficulty: float = DIFFICULTY,
                max_displacement: int = MAX_DISPLACEMENT,
                margin: int = MARGIN) -> list:

    """
    Creates a fleshed-out track based on the general shape
    defined by the vertices of the Convex Hull

    """

    track_set = [[0, 0] for i in range(len(track_points) * 2)]
    for i in range(len(track_points)):
        disp = math.pow(random(), difficulty) * max_displacement
        disp_vec = [disp * i for i in make_rand_vector(2)] 
        track_set[i * 2] = np.ndarray.tolist(track_points[i])
        track_set[i * 2 + 1][0] = int((track_points[i][0] + track_points[(i + 1) % len(track_points)][0]) / 2 + disp_vec[0])
        track_set[i * 2 + 1][1] = int((track_points[i][1] + track_points[(i + 1) % len(track_points)][1]) / 2 + disp_vec[1])
    #for i in range(3):
    #    track_set = fix_angles(track_set)
    #    track_set = push_points_apart(track_set)

    final_set = []
    for point in track_set:
        if point[0] < margin:
            point[0] = margin + gauss(margin / 10, 1)
        elif point[0] > WIDTH - margin:
            point[0] = WIDTH - margin - gauss(margin / 10, 1)
        if (point[1]) < margin:
            point[1] = margin - gauss(margin / 10, 1)
        elif point[1] > HEIGHT - margin:
            point[1] = HEIGHT - margin - gauss(margin / 10, 1)
        final_set.append(point)
    return final_set


def fix_angles(points: list, max_angle: int = MAX_ANGLE) -> list:

    """
    Goes through the newly-created points that define the track and 
    ensures that there no angles between points past a threshold
    defined by max_angle.

    """
    prev_point = len(points) - 1
    for i in range(len(points)):
        next_point = (i + 1) % len(points)
        px = points[i][0] - points[prev_point][0]
        py = points[i][1] - points[prev_point][1]
        p_dist = sqrt(px**2 + py**2)
        px /= p_dist
        py /= p_dist 
        nx = points[next_point][0] - points[i][0]
        ny = points[next_point][1] - points[i][1]
        n_dist = sqrt(nx**2 + ny**2)
        nx /= n_dist
        ny /= n_dist 
        a = atan2(px * ny - py * nx, px * nx + py * ny)
        if (abs(math.degrees(a)) <= max_angle):
            continue
        diff = math.radians(max_angle * math.copysign(1,a)) - a
        c = math.cos(diff)
        s = math.sin(diff)
        new_x = (nx * c - ny * s) * n_dist
        new_y = (nx * s + ny * c) * n_dist
        points[next_point][0] = int(points[i][0] + new_x)
        points[next_point][1] = int(points[i][1] + new_y)
        prev_point = i
    return points

def push_points_apart(points: list, min_dist: int = MIN_DISTANCE) -> list:

    """ 
    Enforces that all points defining the skeleton of the track
    are at a given minimum distance apart.

    """
    dst2 = min_dist**2
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p_dist = sqrt((points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2)
            if p_dist < min_dist:
                dx = points[j][0] - points[i][0];  
                dy = points[j][1] - points[i][1];  
                dl = math.sqrt(dx*dx + dy*dy);  
                dx /= dl;  
                dy /= dl;  
                dif = dst2 - dl;  
                dx *= dif;  
                dy *= dif;  
                points[j][0] = int(points[j][0] + dx);  
                points[j][1] = int(points[j][1] + dy);  
                points[i][0] = int(points[i][0] - dx);  
                points[i][1] = int(points[i][1] - dy);  
    return points


def smooth_track(track_points: list) -> list:
    x = np.array([p[0] for p in track_points])
    y = np.array([p[1] for p in track_points])

    # append starting x, y coordinates
    x = np.r_[x, x[0]]
    y = np.r_[y, y[0]]

    # fit splines to x=f(u) and y=g(u), treating both as periodic
    tck, u = interpolate.splprep([x, y], s=0, per=True)

    # evaluate the spline fits for points 
    xi, yi = interpolate.splev(np.linspace(0, 1, SPLINE_POINTS), tck)
    return [(int(xi[i]), int(yi[i])) for i in range(len(xi))]
