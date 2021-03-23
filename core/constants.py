# Screen dimesions
SIZE = (1000, 750)

# Track dimensions
WIDTH = 800 
HEIGHT = 600

OFFSET = ((SIZE[0] - WIDTH) // 2, (SIZE[1] - HEIGHT) // 2)

STARTING_GRID_TILE = 'static/grid_tile.png'
START_TILE_HEIGHT = 10
START_TILE_WIDTH = 10


# Colors
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
#BACKGROUND_COLOR = [163, 217, 182]
#TRACK_COLOR = [216, 242, 220]
BACKGROUND_COLOR = [242, 188, 148]
TRACK_COLOR = [128, 255, 151]
LINE_COLOR = [218, 165, 32]

CHECKPOINT_POINT_ANGLE_OFFSET = 3
CHECKPOINT_MARGIN = 5

TRACK_POINT_ANGLE_OFFSET = 3

###
# Track parameters
###

# Boundaries for the numbers of points that will be randomly 
# generated to define the initial polygon used to build the track
MIN_POINTS = 20
MAX_POINTS = 30
SPLINE_POINTS = 750

# Margin between screen limits and any of the points that shape the
# initial polygon
MARGIN = 25
# minimum distance between points that form the track skeleton
MIN_DISTANCE = 20

# Maximum midpoint displacement for points placed after obtaining the initial polygon
MAX_DISPLACEMENT = 80
# Track difficulty
DIFFICULTY = 0.0
# min distance between two points that are part of thr track skeleton
DISTANCE_BETWEEN_POINTS = 20
# Maximum corner allowed angle
MAX_ANGLE = 60

TRACK_WIDTH = 40

