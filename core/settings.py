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
TRACK_SIZE = (300, 300)
TRACK_ORIGIN = (400, 300)

# ASSET PATHS
BACKGROUND = 'assets/grass.png'

