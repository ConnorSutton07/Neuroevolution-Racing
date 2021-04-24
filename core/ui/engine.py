"""
Pygame wrapper allowing for easy, convenient, and customizable GUI windows.
Classes
-------
Engine
	Used to render window and blit shapes and text to screen.
"""

from __future__ import annotations
import os
import pygame
import numpy.random as rand
from copy import deepcopy


__author__ = "Grant Holmes"
__email__ = "g.holmes429@gmail.com"


class Engine:
	"""
	Used to render window and blit shapes and text to screen.
	Attributes
	----------
	targetFPS: int
		Target frames per second
	fontStyle: str
		Font style
	clock: pygame.time.Clock
		Used to regulate game ticks and FPS
	dt: float
		Delta time, measurement of latency between frames, used to achieve frame rate motion independence
	running: bool
		Whether engine is running
	fontCache: dict
		Caches rendered fonts, improves performance
	surfaceCache: dict
		Caches rendered surfaces, improves performance
	background: pygame.Surface
		Background for active window
	screen: pygame.Surface
		Background for entire screen
	screenSize: tuple
		(width, height) of the screen
	offset: tuple
		(x, y) offset for position of active window relative to screen
	Public Methods
	--------------
	shouldRun() -> None:
		Determines if engine should keep running.
	clearScreen() -> None:
		Removes everything blitted on screen by covering everything with background.
	updateScreen() -> None:
		Renders necessary components to screen.
	exit() -> None:
		Has engine exit.
	scaleUp(coord: tuple) -> tuple:
		Scales (x, y) coords to fit resolution of screen.
	renderScene(func: callable, *args) -> None:
		Renders custom scene defined outside of this class in the form of customScene(engine: graphics.Engine...
	printToScreen(text: str, pos: tuple, fontSize: int, textColor: tuple, backgroundColor: tuple = None) -> None:
		Blits text to screen.
	renderRect(pos: tuple, size: tuple, fillColor: tuple, alpha: int = 255) -> None:
		Blits rect to screen.
	renderCircle(pos: tuple, radius: float, fillColor: tuple, alpha: int = 255) -> None:
		Blits circle to screen.
	renderLine(start: tuple, end: tuple, width: int, fillColor: tuple) -> None:
		Blits line to screen.
	"""
	colors = {
		"green"			   : (0, 255, 0),
		"red"			   : (255, 0, 0),
		"purple"		   : (200, 100, 200),
		"blue"			   : (0, 0, 255),
		"mediumBlue"	   : (150, 150, 255),
		"lightBlue"		   : (175, 175, 255),
		"black"			   : (0, 0, 0),
		"white"			   : (255, 255, 255),
		"brown"			   : (82, 75, 36),
		"pastelLightGreen" : (93, 255, 163),
		"pastelDarkGreen"  : (36, 232, 189),
		"pastelYellow"	   : (246, 245, 155),
		"pastelBlue"	   : (193, 198, 252),
		"pastelPink"	   : (254, 151, 218),
		"darkGrass"		   : (73, 255, 130),
		"lightGrass"       : (93, 255, 164),
		"brickRed"		   : (213, 153, 122)
	}

	def __init__(self,
				 screenSize: tuple,
				 numGrids: tuple,
				 backgroundType: str = 'checkered',
				 backgroundPath: str = None,
				 gridColors: tuple = ("black", "white", "black"),
				 targetFPS: int = 60,
				 title: str = "Untitled Game",
				 fontStyle: str = "impact",
				 imageFolder: str = "images"
				 ) -> None:
		"""
		Initializes engine, calculates aspect ratio and fits active window to screen.
		Parameters
		----------
		screenSize: tuple
			Resolution of GUI window
		numGrids: tuple
			Number of grid for active game window
		checkered: bool
			If active game window should have checkered background
		targetFPS: int
			Target frames per second
		title: str
			Window title
		fontStyle: str
			Font style
		gridColors: tuple
			Colors of grid if checkered in form (checker color 1, checker color 2, border color)
		"""
		self.targetFPS = targetFPS
		self.fontStyle = fontStyle
		self.backgroundType = backgroundType

		pygame.init()
		pygame.font.init()

		self.clock = pygame.time.Clock()
		self.dt = None
		self.running = True
		pygame.display.set_caption(title)

		self.fontCache = {}
		self.surfaceCache = {}
		self.imageCache = {}
		
		self.imageFolder = os.path.join(os.getcwd(), imageFolder)

		# aspect ratios
		screenAR, gridsAR = screenSize[0]/screenSize[1], numGrids[0]/numGrids[1]

		# position active window to fit on screen
		if gridsAR == screenAR:
			self.offset = (0, 0)
			backgroundSize = screenSize
		elif gridsAR > screenAR:
			compression = screenSize[0]/numGrids[0]
			backgroundSize = (numGrids[0]*compression, numGrids[1]*compression)
			self.offset = (0, 0.5*(screenSize[1] - backgroundSize[1]))
		else:
			compression = screenSize[1] / numGrids[1]
			backgroundSize = (numGrids[0] * compression, numGrids[1] * compression)
			self.offset = (0.5 * (screenSize[0] - backgroundSize[0]), 0)

		self.screenSize = screenSize
		self.screen = pygame.display.set_mode(screenSize)
		self.surfaceCache[backgroundSize] = Engine.Surface(backgroundSize, flag="srcalpha")
		self.background = self.surfaceCache[backgroundSize]

		self.gridSize = tuple([int(backgroundSize[0] / numGrids[0]), int(backgroundSize[1] / numGrids[1])])
		self.paddedGridSize = (self.gridSize[0] + 1, self.gridSize[1] + 1)

		# calculate clipping due to discrepancy of integer rounding
		clipping = (0.5*(backgroundSize[0] % numGrids[0]), 0.5 * (backgroundSize[1] % numGrids[1]))
		self.offset = (self.offset[0]+clipping[0], self.offset[1]+clipping[1])
		self.screen.set_clip(pygame.Rect(*self.offset, backgroundSize[0]-clipping[0]*2, backgroundSize[1]-clipping[1]*2))

		# create checkered background
		if backgroundType == 'checkered':
			for coord, val in Engine.checkerboard(numGrids).items():
				#rect = pygame.Surface(self.gridSize)
				rect = Engine.Surface(self.gridSize, flag='srcalpha')
				rect.fill(Engine.colors[gridColors[val]])
				self.background.blit(rect, (coord[0] * self.gridSize[0], coord[1] * self.gridSize[1]))
		elif backgroundType == 'image':
			self.tileImageAsBackground(backgroundPath)

		self.particles = []


	def shouldRun(self) -> bool:
		"""
		Determines if engine should keep running.
		Returns
		-------
		bool: if engine is now running after checks
		"""
		if not self.running:
			return False
		self._handleEvents()
		self.dt = self.clock.tick(self.targetFPS) / 1000 * self.targetFPS
		return self.running

	def clearScreen(self) -> None:
		"""Removes everything blitted on screen by covering everything with background."""
		self.screen.blit(self.background.surface, self.offset)

	def updateScreen(self) -> None:
		"""Renders necessary components to screen."""
		pygame.display.flip()

	def getBackgroundType(self) -> str:
		return self.backgroundType

	def exit(self) -> None:
		"""Has engine exit."""
		if self.running:
			pygame.quit()

	def scaleUp(self, coord: tuple) -> tuple:
		"""
		Scales (x, y) coords to fit resolution of screen.
		Parameters
		----------
		coord: tuple
			(x, y) coord to scale up
		Returns
		-------
		tuple: scaled coord
		"""
		return coord[0] * self.gridSize[0] + self.offset[0], coord[1] * self.gridSize[1] + self.offset[1]

	def renderScene(self, func: callable, *args) -> None:
		"""
		Renders custom scene defined outside of this class in the form of customScene(engine: graphics.Engine...
		Parameters
		----------
		func: callable
			Function describing how to render custom scene
		*args
			Arguments to pass into func
		"""
		func(self, *args)

	def printToScreen(self, text: str, pos: tuple, fontSize: int, textColor: tuple, backgroundColor: tuple = None) -> None:
		"""
		Blits text to screen.
		Parameters
		----------
		text: str
			Text to display
		pos: tuple
			(x, y) pos on screen to display text
		fontSize: int
			Size of font
		textColor: tuple
			RGB color value
		backgroundColor: tuple, optional
			RGB color value for rect behind text
		"""
		if fontSize not in self.fontCache:
			self.fontCache[fontSize] = pygame.font.Font(self.fontStyle, fontSize)

		font = self.fontCache[fontSize]
		paddedOutput = " " + text + " "

		if backgroundColor is not None:
			text = font.render(paddedOutput, True, textColor, backgroundColor)
		else:
			text = font.render(paddedOutput, True, textColor)

		textRect = text.get_rect()
		textRect.center = pos
		self.screen.blit(text, textRect)

	def renderRect(self, pos: tuple, size: tuple, fillColor: tuple, alpha: int = 255, dest: Engine.Surface = None) -> None:
		"""
		Blits rect to screen.
		Parameters
		----------
		pos: tuple
			(x, y) pos to blit rect to screen
		size: tuple
			(x, y) size of rect
		fillColor: tuple
			RGB values for color of rect
		alpha: int, default=255
			Transparency value (0-255) of rect
		"""
		if size not in self.surfaceCache:
			self.surfaceCache[size] = Engine.Surface(size, flag="srcalpha")

		surface = self.surfaceCache[size]
		surface.set_alpha(alpha)
		surface.fill(fillColor)

		dest_surface = self.screen if dest is None else dest.surface
		dest_surface.blit(surface.surface, pos)

	def renderCircle(self, pos: tuple, radius: float, fillColor: tuple, alpha: int = 255, dest: Engine.Surface = None) -> None:
		"""
		Blits circle to screen.
		Parameters
		----------
		pos: tuple
			(x, y) pos to blit rect to screen
		radius: float
			Radius of circle
		fillColor: tuple
			RGB values for color of rect
		alpha: int, default=255
			Transparency value (0-255) of rect
		"""
		frameSize = (radius * 2, radius * 2)
		rel_x = radius
		rel_y = radius

		if frameSize not in self.surfaceCache:
			self.surfaceCache[frameSize] = Engine.Surface(frameSize, flag="srcalpha")

		surface = self.surfaceCache[frameSize]
		surface.fill(Engine.colors["white"])
		surface.set_colorkey(Engine.colors["white"])
		surface.set_alpha(alpha)
		#print(pos)
				
		pygame.draw.circle(surface.surface, fillColor, (rel_x, rel_y), radius)
		dest_surface = self.screen if dest is None else dest.surface
		dest_surface.blit(surface.surface, pos)

	def renderLine(self, start: tuple, end: tuple, width: int, fillColor: tuple, dest: Engine.Surface = None) -> None:
		"""
		Blits line to screen.
		Parameters
		----------
		start: tuple
			(x, y) pos for start point of line
		end: tuple
			(x, y) pos for end point of line
		width: int
			Value denoting width of line
		fillColor: tuple
			RGB values for color of rect
		"""
		dest_surface = self.screen if dest is None else dest.surface
		pygame.draw.line(dest_surface, fillColor, start, end, width)
	

	def renderPolygon(self, color: tuple, points: list, width: int = 0, dest: Engine.Surface = None) -> None:
		"""
		Draws polygon to given surface

		Parameters
		----------
		surface
			Surface to draw on (defaults to engine.screen)
		points: list
			list of (x, y) pairs of points to connect
		color: tuple
			color to fill polygon
		width: int
			width of poylgon edges
		
		"""
		dest_surface = self.screen if dest is None else dest.surface
		pygame.draw.polygon(dest_surface, color, points, width)



	def renderSurface(self, source: Engine.Surface, dest: tuple = (0,0), area=None, flag: str = 0) -> None:
		"""
		Blits a surface to the screen

		Parameters
		----------
		source: Engine.Surface
			the surface to be drawn to the screen
		dest: tuple
			the (x, y) coordinates of the upper left corner of the 
			drawing area
		area: Rect
			an optional area rectangle that can be used to limit
			the area of the drawing
		flag: str
			optional flag for additional instruction

		"""
		self.screen.blit(source.surface, dest, area=area, special_flags=flag)


	def emit(self) -> None:
		""" 
		Draws all particles to screen after removing
		those with negative size value

		"""
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle.update()
				self.renderCircle(*(particle.getAttributes()))

	def add_particles(self, pos: tuple, dir: tuple, colors: list, size: int, N: int) -> None:
		""" 
		Adds particles based on given parameters with
		some variability added to the position, speed,
		and size.

		Parameters
		----------

		pos: tuple
			(x, y) coordinates of the particle. Subject to slight variability
		dir: tuple
			(dx, dy), indicates the direction of movement
		colors: list
			contains a list of colors; one will be randomly chosen as the 
			particle's color
		size: int
			radius of the particle
		N: int
			number of particles to be added

		"""
		for _ in range(N):
			p = (pos[0] + rand.randint(-5, 5), pos[1] + rand.randint(-5, 5))
			speed = 1 + rand.normal(0, 0.5)
			size += rand.randint(-1, 1)
			particle = Particle(p, dir, colors[rand.randint(0, len(colors) - 1)], size, speed)
			self.particles.append(particle)

	def delete_particles(self) -> None:
		""" 
		Removes all particles that have shrunk to
		a negative size

		"""
		p_copy = [p for p in self.particles if p.size > 0]
		self.particles = p_copy


	#def applyTexture(self, texture_path: str, surface: Engine.Surface = self.screen) -> Engine.Surface:
	#	texture = pygame.image.load(texture_path, )

	def cacheSurface(self, name, surface):
		self.surfaceCache[name] = surface

	def _handleEvents(self) -> None:
		"""Handles events from Pygame's event queue. pygame.QUIT occurs when "X" on top right corner is clicked."""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				pygame.quit()

	@staticmethod
	def checkerboard(n: tuple, border: bool = True) -> dict:
		"""
		Creates checkerboard representation.
		x x x x x . . .
		x o x o x
		x x o x o
		.		. . .
		.		.
		.		.
		Parameters
		----------
		n: tuple
			Size of checkerboard
		border: bool
			Whether border should be included on edges
		Returns
		-------
		dict: Keys are (x, y) coords, values are 0, 1, or 2
		"""
		board = {}
		edges = ({0, n[0] - 1}, {0, n[1] - 1})
		for i in range(n[0]):
			for j in range(n[1]):
				#if border and any([(i, j)[k] in edges[k] for k in range(2)]):
				#	board[(i, j)] = 2
				if (i + j) % 2 == 0:
					board[(i, j)] = 1
				else:
					board[(i, j)] = 0
		return board


	def load_image(self, filename: str) -> Engine.Surface:
		"""
		Returns a surface containing the image 
		corresponding to the given file. The file
		must be contained within the engine's image
		folder.

		Parameters
		----------
		filename: str
			The name of the file inside the image folder

		"""
		image_file = os.path.join(self.imageFolder, filename)
		img = pygame.image.load(image_file)
		img_surface = Engine.Surface((img.get_width(), img.get_height()), flag="srcalpha")
		img_surface.surface = img
		return img_surface

	def tile_surface(self, surface: Engine.Surface, size: tuple = None) -> Engine.Surface:
		"""
		Tiles a surface across a given area

		Parameters
		----------
		surface: Engine.Surface
			the surface that will be tiled
		size: tuple 
			(x, y) The width (x) and height (y) of the area to tile across

		"""
		if size is None:
			size = self.screenSize
		img = surface#.surface
		result = Engine.Surface(size, flag="srcalpha", depth=32)
		for x in range(0, size[0], img.surface.get_width()):
			for y in range(0, size[1], img.surface.get_height()):
				result.blit(img, (x, y))
		return result

	def tileImageAsBackground(self, img_name: str):
		""" 
		Opens the image with the given file name 
		and tiles it across the screen size to be
		used as a background.

		Parameters
		----------
		img_name: str
			the file name of the image to use as the background

		"""
		if img_name not in self.imageCache:
			#self.imageCache[img_name] = pygame.image.load(os.path.join(self.imageFolder, img_name))
			self.imageCache[img_name] = self.load_image(os.path.join(self.imageFolder, img_name))
		img = self.imageCache[img_name]
		for x in range(0, self.screenSize[0], img.get_width()):
			for y in range(0, self.screenSize[1], img.get_height()):
				self.background.blit(img, (x, y))


	class Surface:
		"""
		Used to contain and manipulate rendered objects such as
		shapes, textures, images, etc.

		"""
		def __init__(self, size: tuple, flag: str = None, depth: int = 0, surface=None):
			self.size = size
			self.flag = flag
			self.depth = depth
			if surface is not None:
				self.surface = surface
			elif (flag == "srcalpha"):
				self.surface = pygame.Surface(size, pygame.SRCALPHA)
			else:
				self.surface = pygame.Surface(size, depth=depth)

		def blit(self, source: Engine.Surface, dest: tuple, area=None, flag: str = 0) -> None:
			""" 
			Draws a source surface onto this surface

			Parameters
			----------
			source: Engine.Surface
				the surface to draw onto this surface
			dest: tuple
				The (x, y) coordinates of the upper left corner where the
				source surface will be drawn
			area: Rect
				an optional area rectangle that can be used to limit
				the area of the drawing
			flag: str
				optional flag for additional instruction
			"""
			self.surface.blit(source.surface, dest, area=area, special_flags=flag)

		def get_size(self) -> tuple:
			""" Returns the dimensions of this surface """
			return self.surface.get_size()

		def get_width(self) -> int: 
			""" Returns the width of the surface """
			return self.surface.get_width()

		def get_height(self) -> int:
			""" Return the height of the surface """
			return self.surface.get_height()

		def convert_alpha(self) -> None:
			""" 
			Changes the pixel format of the surface to 
			include per-pixel alpha value
			
			"""
		
			self.surface.convert_alpha()

		def set_alpha(self, alpha: int = None) -> None:
			""" sets the alpha value for pixels contained in the surface """
			self.surface.set_alpha(alpha)

		def set_colorkey(self, color: tuple = None) -> None:
			"""  sets """
			self.surface.set_colorkey(color)

		def fill(self, color: tuple, flag: str = 0) -> None:
			""" fills a surface with a given color """
			self.surface.fill(color, special_flags=int(flag))

		def invert(self) -> Engine.Surface:
			"""Not operation relative to universe"""
			mask = pygame.mask.from_surface(self.surface)
			mask.invert()
			surface = mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0,0,0,0))
			new_surface = Engine.Surface(surface.get_size(), flag="srcalpha")
			new_surface.surface = surface.copy()
			return new_surface
			
		def union(self, surface: Engine.Surface) -> Engine.Surface:
			"""Union of two masks"""
			mask = pygame.mask.from_surface(self.surface)
			other_mask = pygame.mask.from_surface(innerSurface.surface)
			union = other_mask.draw(surface)
			surface = union.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0,0,0,0))
			new_surface = Engine.Surface(surface.get_size(), flag="srcalpha")
			new_surface.surface = surface.copy()
			return new_surface
			
		def intersection(self, surface: Engine.Surface) -> Engine.Surface:
			"""Intersection of two masks"""
			mask = pygame.mask.from_surface(self.surface)
			other_mask = pygame.mask.from_surface(innerSurface.surface)
			intersection = other_mask.overlap_mask(surface)
			surface = intersection.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0,0,0,0))
			new_surface = Engine.Surface(surface.get_size(), flag="srcalpha")
			new_surface.surface = surface.copy()
			return new_surface
			
		def difference(self, surface: Engine.Surface) -> Engine.Surface:
			"""Difference of two masks"""
			outer_mask = pygame.mask.from_surface(self.surface)
			inner_mask = pygame.mask.from_surface(surface.surface)
			outer_mask.erase(inner_mask, (0, 0))
			outer_surface = outer_mask.to_surface(setcolor=(255, 255, 255, 255), unsetcolor=(0,0,0,0))
			new_surface = Engine.Surface(outer_surface.get_size(), flag="srcalpha")
			new_surface.surface = outer_surface.copy()
			return new_surface
			
		def __and__(self, surface: Engine.Surface) -> Engine.Surface:
			"""Ex. surface1 & surface2"""
			return self.intersection(surface)
			
		def __or__(self, surface: Engine.Surface) -> Engine.Surface:
			"""Ex. surface1 | surface2"""
			return self.union(surface)
			
		def __sub__(self, surface) -> Engine.Surface:
			"""Ex. surface1 - surface2"""
			return self.difference(surface)
			
		def __NE__(self) -> Engine.Surface:
			"""Ex. !surface1"""
			return self.invert()

		def copy(self):
			return Engine.Surface(self.size, self.flag, self.depth, self.surface.copy())

		def apply_texture(self, texture: Engine.Surface) -> Engine.Surface:
			"""
			Stamps the texture of the given surface
			across the area of the original surface
			
			"""
			texture.convert_alpha()
			target = pygame.surfarray.pixels_alpha(texture.surface)
			target[:] = pygame.surfarray.array2d(self.surface)

			del target
			return texture

		def rotate(self, angle: float) -> None:
			""" 
			Counterclockwise rotation of this surface. 
			Negative values will rotate clockwise.

			"""
			self.surface = pygame.transform.rotate(self.surface, angle)
			#loc = self.surface.get_rect().center  #rot_image is not defined 
			#rot_image = pygame.transform.rotate(self.surface, angle)
			#rot_image.get_rect().center = loc
			#self.surface = rot_image

class Particle:
	def __init__(self, pos: tuple, dir: tuple, color: tuple, size: int, speed: int, shrink_rate: float = 0.2) -> None:
		self.pos = pos 
		self.dir = (dir[0] * speed, dir[1] * speed)
		self.color = color 
		self.size = size 
		self.speed = speed
		self.shrink_rate = shrink_rate 

	def update(self) -> None:
		self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
		self.size -= self.shrink_rate

	def getAttributes(self) -> tuple:
		return self.pos, self.size, self.color