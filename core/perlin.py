from perlin_noise import PerlinNoise

def get_perlin_line(density: int, num_points: int, octaves: int = 4, amplitude: int = 75) -> np.array:
    """
    Returns perlin noise based on given level of stochasticity

    Octaves: Number of layered noise functions being used to create the
    perlin noise. More octaves means more stochasticty and more jaggedness

    """
    noise = PerlinNoise(octaves = octaves)
    pts = np.zeros((num_points, 2))

    for i in range(num_points):
        
        noise_val =         noise(i / num_points)
        noise_val += 0.25 * noise((i - 1) / num_points)
        noise_val += 0.125 * noise((i + 1) / num_points)
        noise_val *= amplitude
        pts[i] = np.array([0 + noise_val, i / density])

    return pts

def get_wild_line(density: int, num_points: int, amplitude: int = 75) -> np.array:
    """
    This one's unpredictable but has done some cool stuff

    """
    noise1 = PerlinNoise(octaves=4)
    noise2 = PerlinNoise(octaves=8)
    noise3 = PerlinNoise(octaves=12)
    noise4 = PerlinNoise(octaves=16)
    pts = np.zeros((num_points, 2))

    for i in range(num_points):
        
        noise_val =          noise1(i / num_points)
        noise_val += 0.5 *   noise2(i / num_points)
        noise_val += 0.25 *  noise3(i / num_points)
        noise_val += 0.125 * noise4(i / num_points)

        noise_val *= amplitude
        pts[i] = np.array([0 + noise_val, i / density])

    return pts
