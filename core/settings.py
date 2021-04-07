"""
Contains global game settings

"""


import os
#import psutil

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide Pygame greeting message


# SCREEN
SCREEN_SIZE = (800, 600)

# FPS AND DISPLAY
TARGET_FPS = 60
SMOOTHNESS = 3  # controls how fast and smooth animations run

# TRACK
TRACK_TYPE = "perlin"
TRACK_ORIGIN = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
TRACK_SCALE = 1.5

# ASSET PATHS
BACKGROUND = 'new_flowers-big.png'
TRACK_TEXTURE = 'earth2.png'
FROG_CAR = 'frog-car-big.png'
