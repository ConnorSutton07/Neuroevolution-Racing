"""
Contains global game settings

"""


import os
#import psutil

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide Pygame greeting message


# SCREEN
SCREEN_SIZE = (1200, 900)

# FPS AND DISPLAY
TARGET_FPS = 60
SMOOTHNESS = 3  # controls how fast and smooth animations run

# TRACK
TRACK_TYPE = "perlin"
TRACK_ORIGIN = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
TRACK_SCALE = 1.5 * (SCREEN_SIZE[0] / 800)
print(TRACK_SCALE)

# ASSET PATHS
TRACK_TEXTURE = 'earth2.png'
FROG_CAR = 'frog-car-fitted.png'
BACKGROUND = 'new_flowers-big.png'
