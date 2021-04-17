"""
Race car with neural network decision making.
"""

from __future__ import annotations
import numpy as np
import keyboard

from core.training.neural_net import FFNN

class Car:
	"""Haven't tested any of this yet."""
	def __init__(
			self,
			ai: bool = True,
			id: str = "",
			architecture: tuple = (8, 6, 2),
			initial_pos: np.ndarray = None,
			max_turning_rate: float = np.radians(10),
			max_momentum: float = 8,
			) -> None:
		self.isAi = ai
		self.id = id  # this should be base 36 number for uniqueness and to minimize digits
		self.network = FFNN(architecture, outputActivation = "linear")  # can decide steering, acceleration
		self.initial_p = initial_pos if initial_pos is not None else np.array([0., 0.])  # position

		self.d = 0 # direction
		self.p = self.initial_p.copy()
		self.m = 0
		self.v = 0

		self.max_turning_rate = max_turning_rate
		self.max_momentum = max_momentum
		self.boost = self.max_momentum * 1.5
		self.steps = 0  # number of steps made
		self.alive = True
		self.resets = 0  # num times this car has been reset

	def step(self) -> None:
		"""Updates cars state."""

		self.p += self.v
		self.steps += 1

	def autostep(self, rayLengths: np.ndarray = None) -> None:
		""""Calculates AI controls then takes a step."""
		if self.isAi:
			steering, throttle = self.get_optimal_controls(rayLengths)
		else:
			steering, throttle, boost = get_player_controls()
		self.turn(steering)
		self.accelerate(throttle, boost)
		self.step()

	def turn(self, d_theta: float) -> None:
		self.d += d_theta

	def get_optimal_controls(self, rayLengths: np.ndarray) -> np.ndarray:
		"""Gets turn angle from neural network."""
		return self.network.feedForward(rayLengths)  # steering angle, acceleartion

	def accelerate(self, a, boost) -> None:
		""" Sets velcoity """

		cos_d = np.cos(self.d) + (2 * np.pi) % (2 * np.pi)
		sin_d = -1 * np.sin(self.d) + (2 * np.pi) % (2 * np.pi)

		if a == 0:
			self.m *= 0.9
		else:
			if boost:
				self.m = max(min(self.m + a + self.boost, self.max_momentum + self.boost), -self.max_momentum + self.boost)
			else:
				self.m = max(min(self.m + a, self.max_momentum), -self.max_momentum)

		self.v = self.m * np.array([cos_d, sin_d])


	def is_alive(self) -> bool:
		"""Returns whether car is alive or not."""
		return self.alive

	def kill(self) -> None:
		"""Kills car and sets pos and vel to 0."""
		self.alive = False
		self.p = np.array([0., 0.])
		self.v = np.array([0., 0.])

	def get_network_params(self) -> dict:
		"""Gets important params from network."""
		return self.network.getParams()

	def reset(self) -> None:
		"""Resets state of this car to initial values."""
		self.p = self.initial_p.copy()
		self.v = self.initial_v.copy()
		self.a = self.initial_a.copy()
		self.steps = 0  # number of steps made
		self.alive = True
		self.resets += 1

	def get_state(self) -> dict:
		"""Returns info about car's state"""
		return {
			"pos": self.p,
			"vel": self.v,
			"mom": self.m,
			"alive": self.alive,
			"dir": self.d
		}

	def __eq__(self, other: Car) -> bool:
		"""Checks if this car and other car are equal via id."""
		return self.id == other.id



def get_player_controls():
	direction = 0
	throttle = 0
	boost = 0
	if keyboard.is_pressed('w'):
		throttle = .15
	if keyboard.is_pressed('a'):
		direction = .1
	if keyboard.is_pressed('s'):
		throttle = -.15
	if keyboard.is_pressed('d'):
		direction = -.1
	if keyboard.is_pressed('space'):
		boost = 1
	#self.d += direction
	#velocity = throttle * np.array([np.cos(direction), np.sin(direction)])
	return direction, throttle, boost
	
