"""

"""
from matplotlib import pyplot as plt
import numpy as np
from core.game_components.track_generation.perlin import *
from core.game_components.track_generation.transformations import *
import random
from scipy.interpolate import interp1d

class Track:
    def __init__(self,
            type: str = "default",
            shape: tuple = (30, 10),
            point_density: int = 5,
            theta_offset: float = 50,
            perturbation: callable = lambda i: (i%10) * (10 * np.sin(i)**2)
            ) -> None:
        self.type = type
        self.shape = shape
        self.point_density = point_density
        self.points_per_edge = shape[1] * point_density
        self.radius_offset = 125 + random.randint(-30, 30)
        self.theta_offset = theta_offset
        if self.type == "perlin":
            self.basic_euclidean_edges, self.polar_edges, self.euclidean_edges = self.perlin_track()
        else:
            self.basic_euclidean_edges, self.polar_edges, self.euclidean_edges = self.default_track(perturbation)

        self.lerp = interp1d(self.polar_edges[0].T[1], self.polar_edges[0].T[0])

       # self.plot()

    def getTrackEdges(self) -> np.array:
        """
        Returns the final euclidean form of the generated racetrack

        """
        return self.euclidean_edges

    def getInnerEdges(self) -> np.array:
        """
        Returns the inside edges of the final euclidean track

        """
        return self.euclidean_edges[0]

    def getOuterEdges(self) -> np.array:
        """
        Returns the outside edges of the final euclidean track

        """
        return self.euclidean_edges[1]

    def setFinalEuclidean(self, new_edges: np.array) -> None:
        """
        Replaces the track's euclidean edges with an updated version

        """

        self.euclidean_edges = new_edges

    def default_track(self, perturbation: callable) -> tuple:
        # construct initial euclidean edges
        point_density = self.point_density
        radius_offset = self.radius_offset
        theta_offset = self.theta_offset
        left_basic_edge = np.array([(perturbation(i / point_density), i / point_density) for i in range(self.points_per_edge)])
        right_basic_edge = np.array([(self.shape[0] + perturbation(i / point_density), i / point_density) for i in range(self.points_per_edge)])
        
        left_basic_edge[-1][0] = left_basic_edge[0][0]
        right_basic_edge[-1][0] = right_basic_edge[0][0]

        basic_euclidean_edges = np.array([left_basic_edge, right_basic_edge])

        polar_edges, radii, thetas = to_polar(basic_euclidean_edges, radius_offset, theta_offset)
       
        euclidean_edges = to_euclidean(polar_edges, radii, thetas)

        return (basic_euclidean_edges, polar_edges, euclidean_edges)



    def perlin_track(self, octaves: int = 5, amplitude: int = 85, smoothing_factor: int = 30) -> tuple:
        amplitude = amplitude + random.randint(-5, 5)
        density = self.point_density 
        radius_offset = self.radius_offset
        theta_offset = 0
        width = self.shape[0]  
        left = get_perlin_line(density, density * self.shape[1], octaves=octaves, amplitude=amplitude)
        left = smooth(left, self.shape[1], density * smoothing_factor)
        right = np.array(list(map(lambda pt: (pt[0] + width, pt[1]), left)))

        left[-1][0] = left[0][0]
        right[-1][0] = right[0][0]
        basic_euclidean_edges = np.array([left, right])

        polar_edges, radii, thetas = to_polar(basic_euclidean_edges, radius_offset, theta_offset)
        print(polar_edges)
        euclidean_edges = to_euclidean(polar_edges, radii, thetas)

        return (basic_euclidean_edges, polar_edges, euclidean_edges)

    def contains(self, pt: tuple) -> bool:
        r, theta = revert_to_polar(pt)
        #theta = theta * 
        #r = r - self.radius_offset

        try:
            left_r = self.lerp(theta)
            #print("Radius at", theta, ":", left_r, "-", left_r + self.shape[0])
            #right_r = r + self.shape[0]
            right_r = left_r + self.shape[0]
            #if (r >= left_r):
            if (r >= left_r and r <= right_r):
                return True
            else:
                return False
        except ValueError as e:
            return False



        
    def plot(self) -> None:
        """
        Plots and renders graphs to screen
        """
        plt.style.use("dark_background")
    
        plt.figure()
        for edge in self.basic_euclidean_edges:
            plt.plot(*list(zip(*edge)), c="red")

        plt.xlabel("x")
        plt.ylabel("y")

        plt.grid(ls="--", alpha=0.25)
        plt.title("Basic Euclidean")

        plt.figure()
        for edge in self.polar_edges:
            plt.plot(*list(zip(*edge)), c="green")
            
        plt.xlabel("r")
        plt.ylabel("theta")
            
        plt.grid(ls="--", alpha=0.25)
        plt.title("Polar")

        plt.figure()
        for edge in self.euclidean_edges:
            plt.plot(*list(zip(*edge)), c="cyan")
           
        plt.grid(ls="--", alpha=0.25)
        plt.title("Euclidean - " + self.type) 

        plt.xlabel("x")
        plt.ylabel("y")

        plt.figure()
        thetas = np.linspace(0, np.pi * 2, 100)
        rs = np.zeros(100,)
        for i in range(thetas.shape[0]):
            rs[i] = self.lerp(thetas[i])
        plt.plot(rs, thetas, c="green")

        plt.grid(ls="--", alpha=0.25)
        plt.title("Polar Interpolated") 

        plt.xlabel("x")
        plt.ylabel("y")
        
        plt.show()
       
if __name__ == "__main__":      
    track = Track(type="perlin")
    track.plot() 
           