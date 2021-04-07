import numpy as np

def to_polar(euclidean_edges: np.array, radius_offset: float, theta_offset: float) -> tuple:
    """
    Requires an array containing left and right euclidean edges as well
    as the radius and theta offsets.
    Returns the polar edges along with the radii of the two lines and their theta values

    """

    left_basic_edge = euclidean_edges[0]
    right_basic_edge = euclidean_edges[1]
    left_basic_x, left_basic_y = left_basic_edge[:,0], left_basic_edge[:,1]
    right_basic_x, right_basic_y = right_basic_edge[:,0], right_basic_edge[:,1]
    
    left_r = left_basic_x + radius_offset
    right_r = right_basic_x + radius_offset
    
    left_basic_y_min, left_basic_y_max = left_basic_y.min(), left_basic_y.max()
    right_basic_y_min, right_basic_y_max = right_basic_y.min(), right_basic_y.max()
    
    left_theta = (left_basic_y - left_basic_y_min) / (left_basic_y_max - left_basic_y_min) * 2 * np.pi + theta_offset
    right_theta = (right_basic_y - right_basic_y_min) / (right_basic_y_max - right_basic_y_min) * 2 * np.pi + theta_offset
    
    polar_edges = np.array([np.stack([left_r, left_theta], axis=1), np.stack([right_r, right_theta], axis=1)])

    radii = [left_r, right_r]
    thetas = [left_theta, right_theta]
    return polar_edges, radii, thetas

def to_euclidean(polar_edges: np.array, radii: list, thetas: list) -> np.array:
    """
    Requries an array of left and right polar edges as well as 
    radius and theta offsets.
    Returns the euclidean edges as well as the radii of the two lines and their 
    theta values.

    """
    left_r = radii[0]
    right_r = radii[1]
    left_theta = thetas[0]
    right_theta = thetas[0]

    left_x, left_y = left_r * np.cos(left_theta), left_r * np.sin(left_theta)
    right_x, right_y = right_r * np.cos(right_theta), right_r * np.sin(right_theta)

    euclidean_edges = np.array([np.stack([left_x, left_y], axis=1), np.stack([right_x, right_y], axis=1)])
    return euclidean_edges

def revert_to_polar(pt: tuple) -> np.array:
    """ 
    Returns a radius based on euclidean coordinates

    """

    if pt[0] == 0:
        pt = (pt[0] + 1e-5, pt[1]) # avoid divide by 0
    r = np.sqrt(pt[0]**2 + pt[1]**2)
    theta = np.arctan2(pt[1], pt[0]) 
    theta = (theta + (2 * np.pi)) % (2 * np.pi) # map from [-pi, pi] to [0, 2pi]

    return r, theta

