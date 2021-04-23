"""
Race car with neural network decision making.
"""

from __future__ import annotations
import numpy as np
import keyboard

from core.training.neural_net import FFNN

class Racecar:
	"""Haven't tested any of this yet."""
	valid_controllers = {"ai", "player"}
	def __init__(
			self,
			controller_type,  # must be in Racecar.valid_controllers
			agent_id: str = "",
			architecture: tuple = (8, 6, 2),
			initial_pos: np.ndarray = None,
			initial_direction: np.ndarray = None,
			initial_speed: float = None,
			initial_accel: float = None,
			speed_decay: float = 0.9125,
			max_turning_rate: float = np.radians(5),
			max_speed: float = 10,
			max_acceleration: float = 1
			) -> None:
		if controller_type not in Racecar.valid_controllers:
			raise TypeError("Controller type must be in " + str(Racecar.valid_controllers))
		self.controller_type = controller_type
		self.get_controls = {
			"ai": self.get_ai_controls,
			"player": self.get_player_controls
		}[self.controller_type]
		
		self.agent_id = agent_id  # this should be base 36 number for uniqueness and to minimize digits, used to track for genetic training
		self.network = FFNN(architecture, outputActivation = "linear")  # can decide steering, acceleration
		
		# initial conditions are important to save when resetting for genetic training
		self.initial_p = initial_pos if initial_pos is not None else np.array([200., 200.])  # position
		self.initial_d = initial_direction if initial_direction is not None else np.array([0., -1.])  # direction 
		self.initial_s = initial_speed if initial_speed is not None else 0  # speed
		self.initial_a = initial_accel if initial_accel is not None else 0  # acceleration
		
		self.speed_decay = speed_decay
		
		# state parameters
		self.p = self.initial_p.copy()
		self.d = self.initial_d.copy()
		self.s = self.initial_s
		self.a = self.initial_a

		# upper bounds
		self.max_turning_rate = max_turning_rate
		self.max_speed = max_speed
		self.max_acceleration = max_acceleration
		self.steps = 0  # number of steps taken
		self.alive = True
		self.resets = 0  # num times this racecar has been reset
		self.boost = False
		self.boost_speed = self.max_speed * 0.5#@0.5

		self.c0 = 0
		self.p0 = 0
		self.total_distance = 0
		self.laps_completed = 0

	def step(self, environment: Environment, inTrack: bool, c0: float) -> None:
		"""Updates cars state."""
		steering, throttle, boost = self.get_controls(environment)

		self.boost = boost
		self.update_distance(c0)
		self.turn(steering)
		self.accelerate(throttle)
		self.p += self.s * self.d
		self.s *= self.speed_decay
		self.steps += 1

	def update_distance(self, c0: float) -> None:
		"""
		Updates the total distance traveled
		and the number of laps completed.

		"""
		p0 = self.p0
		if abs(p0 - c0) > 1:
			self.total_distance += (2 * np.pi) - abs(c0 - p0)
		else:
			self.total_distance += c0 - p0
		self.p0 = c0
		self.laps_completed = int(self.total_distance / (2 * np.pi))

	def accelerate(self, throttle: float) -> None:
		"""Sets acceleration."""
		if throttle != 0:
			raw_magnitude = abs(throttle)
			raw_sign = throttle / raw_magnitude
			self.a = raw_sign * min(raw_magnitude, self.max_acceleration)
		else:
			self.a = 0
		
		if (self.s + self.a) != 0:
			boost = self.boost_speed * self.boost
			max_speed = self.max_speed + boost
			magnitude = abs(self.s + self.a) + boost
			sign = (self.s + self.a) / (magnitude - boost)
			self.s = sign * min(magnitude, max_speed)

	def turn(self, d_theta: float) -> None:
		"""Rotates direction ccw by theta degrees in radians, def need to test this."""
		if d_theta != 0:
			magnitude = abs(d_theta)
			sign =  (d_theta / magnitude)
			d_theta = sign * min(magnitude, self.max_turning_rate)
			
		cos_d_theta = np.cos(d_theta)	
		sin_d_theta = np.sin(d_theta)
		
		rotation_matrix = np.array([[cos_d_theta, -sin_d_theta], [sin_d_theta, cos_d_theta]])  # linear transformation
		
		self.d = rotation_matrix @ self.d  
		
	def cast_rays(self, environment) -> np.ndarray:
		raise NotImplementedError
		return

	def get_ai_controls(self, environment: np.ndarray) -> np.ndarray:
		"""Gets turn angle from neural network."""
		rayLengths = self.cast_rays()
		return self.network.feedForward(rayLengths)  # steering angle, acceleartion

	def get_player_controls(self, environment) -> np.ndarray:
		throttle = 0
		steering = 0
		boost = False

		if keyboard.is_pressed('w'):
			throttle = 5
		if keyboard.is_pressed('a'):
			steering = -1
		if keyboard.is_pressed('s'):
			throttle = -5
		if keyboard.is_pressed('d'):
			steering = 1
		if keyboard.is_pressed('space'):
			boost = True
			
		if keyboard.is_pressed('e'):  # emergency stop, debugging
			self.s = 0
			self.a = 0
			
		return steering, throttle, boost

	def get_network_params(self) -> dict:
		"""Gets important params from network."""
		return self.network.getParams()

	def is_alive(self) -> bool:
		"""Returns whether racecar is alive or not."""
		return self.alive

	def kill(self) -> None:
		"""Kills racecar and sets pos and vel to 0."""
		self.alive = False
		self.p = np.array([0., 0.])
		self.s = 0
		self.a = 0

	def reset(self) -> None:
		"""Resets state of this racecar to initial values."""
		self.p = self.initial_p.copy()
		self.d = self.iniital_d.copy()
		self.s = self.initial_s
		self.a = self.initial_a
		self.steps = 0  # number of steps made
		self.alive = True
		self.resets += 1

	def get_state(self) -> dict:
		"""Returns info about racecar's state"""
		#print(self.d[1], self.d[1] % np.pi)
		if self.d[0] != 0:
			magnitude = abs(self.d[0])
			sign = self.d[0] / abs(self.d[0])
			d0 = sign * min(magnitude, 1)  # dealing with float precision errors causing invalid values
		else:
			d0 = 0
			
		if self.d[1] > 0:
			d = -np.arccos(d0)
		else:
			d = -(2 * np.pi - np.arccos(d0))
		#print(d)
		return {
			"pos"  : self.p,
			"dir"  : d,
			"speed": self.s,
			"accel": self.a,
			"alive": self.alive,
			"boost": self.boost,
			"lap"  : self.laps_completed
		}

	def __eq__(self, other: Racecar) -> bool:
		"""Checks if this racecar and other racecar are equal via id."""
		return self.id == other.id