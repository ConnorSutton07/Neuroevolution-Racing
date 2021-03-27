"""

"""

from matplotlib import pyplot as plt
import numpy as np

class Track:
    def __init__(self,
            shape: tuple = (20, 10),
            point_density: int = 5,
            radius_offset: float = 10,
            theta_offset: float = 50,
            perturbation: callable = lambda i: (i%10) * (10 * np.sin(i)**2)
            ) -> None:
        self.shape = shape
        self.point_density = point_density
        self.points_per_edge = shape[1] * point_density
        
        # construct initial euclidean edges
        left_basic_edge = np.array([(perturbation(i / point_density), i / point_density) for i in range(self.points_per_edge)])
        right_basic_edge = np.array([(self.shape[0] + perturbation(i / point_density), i / point_density) for i in range(self.points_per_edge)])
        
        left_basic_edge[-1][0] = left_basic_edge[0][0]
        right_basic_edge[-1][0] = right_basic_edge[0][0]

        self.basic_euclidean_edges = np.array([left_basic_edge, right_basic_edge])

        # construct euclidean -> polar edges
        left_basic_x, left_basic_y = left_basic_edge[:,0], left_basic_edge[:,1]
        right_basic_x, right_basic_y = right_basic_edge[:,0], right_basic_edge[:,1]
        
        left_r = left_basic_x + radius_offset
        right_r = right_basic_x + radius_offset
        
        left_basic_y_min, left_basic_y_max = left_basic_y.min(), left_basic_y.max()
        right_basic_y_min, right_basic_y_max = right_basic_y.min(), right_basic_y.max()
        
        left_theta = (left_basic_y - left_basic_y_min) / (left_basic_y_max - left_basic_y_min) * 2 * np.pi + theta_offset
        right_theta = (right_basic_y - right_basic_y_min) / (right_basic_y_max - right_basic_y_min) * 2 * np.pi + theta_offset
        
        self.polar_edges = np.array([np.stack([left_r, left_theta], axis=1), np.stack([right_r, right_theta], axis=1)])
        
        # construct final transformed polar -> euclidean edges
        left_x, left_y = left_r * np.cos(left_theta), left_r * np.sin(left_theta)
        right_x, right_y = right_r * np.cos(right_theta), right_r * np.sin(right_theta)
        
        self.euclidean_edges = np.array([np.stack([left_x, left_y], axis=1), np.stack([right_x, right_y], axis=1)])
        
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
        plt.title("Euclidean") 

        plt.xlabel("x")
        plt.ylabel("y")
        
        plt.show()
       
if __name__ == "__main__":      
    track = Track()
    track.plot() 
           