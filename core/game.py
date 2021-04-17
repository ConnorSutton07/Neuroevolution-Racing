"""

"""
import os

from core.game_components.track import Track
from core.game_components.environment import Environment
from core.settings import *
from core.ui.engine import Engine
import keyboard
import numpy as np
from random import randint

def prepareTrackSurface(engine: Engine, environment: Environment) -> Engine.Surface:
	""" 
	This function is called once per run, and it prepares the track's surface 
	so that recalculation of each component is not necessary every frame

	""" 
	track = environment.track

	# retrieves the coordinates for all points on the inside and outside edges of the track
	inner_edges = track.getInnerEdges()
	outer_edges = track.getOuterEdges()

	# create empty surfaces that will contain the inside/outside edges
	outer_surface = engine.Surface(SCREEN_SIZE, flag="srcalpha")
	inner_surface = engine.Surface(SCREEN_SIZE, flag="srcalpha")

	# draw the edges to the corresponding surfaces
	engine.renderPolygon((255, 255, 255), outer_edges, outer_surface)
	engine.renderPolygon((0, 0, 0), inner_edges, inner_surface)



	if engine.getBackgroundType() == 'image':
		# load the texture that will be applied to the track
		texture = engine.load_image(TRACK_TEXTURE)
		texture = engine.tile_surface(texture)
	else:
		texture = engine.Surface(outer_surface.get_size(), flag='srcalpha')
		texture.fill(engine.colors['pastelDarkGreen'])

	# remove the inside surface from the outside to create the track surface and apply the texture to the result
	
	outer_surface = (outer_surface - inner_surface).apply_texture(texture)

	# draw some boundaries
	#engine.renderPolygon(engine.colors["pastelBlue"], outer_edges, outer_surface, width=5)
	#engine.renderPolygon(engine.colors["pastelBlue"], inner_edges, outer_surface, width=5)


	return outer_surface



def PvAI():
	track = Track(type=TRACK_TYPE)
	grid_colors = ('pastelLightGreen', 'pastelYellow', 'pastelDarkGreen')

	engine = Engine(SCREEN_SIZE, 
					numGrids = (27, 27), 
					backgroundType = 'checkered', 
					backgroundPath = BACKGROUND, 
					gridColors = grid_colors, 
					title = "NEUROEVOLUTION RACING",
					imageFolder = os.path.join(os.getcwd(), "assets"))


	environment = Environment(track)
	track_surface = prepareTrackSurface(engine, environment)
	carSurface = engine.load_image(FROG_CAR)  # added this here so we don't have to load image from file every time step

	# pts = []
	# for i in range(3000):
	#	 pt = (randint(-300, 300) + TRACK_ORIGIN[0], randint(-300, 300) + TRACK_ORIGIN[1])
	#	 pts.append(pt)

	while not keyboard.is_pressed('esc'):
		environment.step()
		for step in range(1, SMOOTHNESS + 1):
			if engine.shouldRun():
				engine.clearScreen()
				engine.renderScene(_renderEnvironment, environment, track_surface, carSurface)
				engine.updateScreen()

	engine.exit()


	
def _renderEnvironment(engine: Engine, environment: Environment, track_surface: Engine.Surface, carSurface) -> None:
	""" 
	Contains all the instructions for the engine to render 
	the environment to the screen

	"""
	engine.renderSurface(track_surface)
	renderCar(engine, environment, carSurface.copy())



def renderCar(engine: Engine, environment: Environment, carSurface) -> None:
	car = environment.getCar()
	car_state = car.get_state()
	#engine.renderCircle(car.p, 10, engine.colors['black'])
	
	carSurface.rotate(np.degrees(car_state['dir']))
	# print(car_state['pos'])
	# print(car_state['vel'])
	rect = carSurface.surface.get_rect()
	engine.renderRect(car_state['pos'], (rect.width, rect.height), (0, 255, 0), 100)
	pos = car_state['pos']
	engine.renderSurface(carSurface, (pos[0] - int(rect.width/2), pos[1] - int(rect.height/2)))
	engine.renderLine((car.p[0], car.p[1]), (car.p[0] + 50 * car.d[0], car.p[1] + 50 * car.d[1]), 5, (255, 0, 0))


#	 for pt in pts:
#		 pt2 = (pt[0] - 2.5, pt[1] - 2.5)
#		 if environment.trackContains(pt):
#			 engine.renderCircle(pt2, 5, (0, 255, 0))
#		 else:
#			 engine.renderCircle(pt2, 5, (255, 0, 0))
#	# pt = (400, 400)







