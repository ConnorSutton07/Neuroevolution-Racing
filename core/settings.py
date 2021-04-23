"""
Contains global game settings

"""


import os
from PIL import Image
#import psutil

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"  # hide Pygame greeting message

# SCREEN
SCREEN_SIZE = (900, 675)

# FPS AND DISPLAY
TARGET_FPS = 60
SMOOTHNESS = 3  # controls how fast and smooth animations run
LAP_TEXT_POS = (210, 75)

# TRACK
TRACK_TYPE = "perlin"
TRACK_ORIGIN = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)
TRACK_SCALE = 1.5 * (SCREEN_SIZE[0] / 800)

# PATHS / FILE NAMES
ASSET_FOLDER = os.path.join(os.getcwd(), "assets")
IMAGE_FOLDER = os.path.join(ASSET_FOLDER, "images")
FONT_FOLDER  = os.path.join(ASSET_FOLDER, "fonts")
TRACK_TEXTURE = 'earth2.png'
FROG_CAR      = 'frog-car.png'
BACKGROUND    = 'new_flowers-big.png'
FONT_FILE     = 'DisposableDroidBB.ttf'

# PARTICLES
PARTICLE_SIZE = 5
NUM_PARTICLES = 3
FIRE_COLORS = [(242, 163, 15), (242, 139, 12), (242, 73, 12), (115, 12, 2), (64, 6, 1)]
