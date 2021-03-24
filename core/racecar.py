"""
Race car with neural network decision making.
"""

import numpy as np

from neural_net import FFNN


class Racecar:
	"""Haven't tested any of this yet."""
	def __init__(
				self,
				id: str,
				architecture: tuple = (8, 6, 3),
				initial_pos: np.ndarray = None,
				initial_vel: np.ndarray = None,
				initial_accel: np.ndarray = None
				) -> None:
		self.id = id  # this should be base 36 number for uniqueness and to minimize digits
		self.network = FFNN(architecture, outputAcivation = "linear")  # can decide steering, acceleration
		self.initial_p = initial_pos if initial_pos is not None else np.array([0., 0.])  # position
		self.initial_v = initial_vel if initial_vel is not None else np.array([0., 0.])  # velocity
		self.initial_a = initial_accel if initial_accel is not None else np.array([0., 0.])  # acceleration
		self.p = self.initial_p.copy()
		self.v = self.initial_v.copy()
		self.a = self.initial_a.copy()
		self.steps = 0  # number of steps made
		self.alive = True
		self.resets = 0  # num times this racecar has been reset

	def step(self) -> None:
		"""Updates cars state."""
		self.p += self.v
		self.v *= self.a
		self.steps += 1

	def steer(self, theta: float) -> None:
		"""Rotates direction ccw by theta degrees in radians, def need to test this."""
		self.v = np.array([[np.cos(theta), -sin(theta)], [sin(theta), cos(theta)]]) @ self.v

	def get_optimal_state(self, rayLengths: np.ndarray) -> np.ndarray:
		"""Gets turn angle from neural network."""
		return self.network.feedForward(rayLengths)  # steering angle, acceleartion

	def accelerate(self, a) -> None:
		"""Sets acceleration."""
		self.a = a

	def is_alive(self) -> bool:
		"""Returns whether racecar is alive or not."""
		return self.alive

	def kill(self) -> None:
		"""Kills racecar and sets pos and vel to 0."""
		self.alive = False
		self.p = np.array([0., 0.])
		self.v = np.array([0., 0.])

	def get_network_params(self) -> dict:
		"""Gets important params from network."""
		return self.network.getParams()

	def reset(self) -> None:
 		"""Resets state of this racecar to initial values."""
		self.p = self.initial_p.copy()
		self.v = self.initial_v.copy()
		self.a = self.initial_a.copy()
		self.steps = 0  # number of steps made
		self.alive = True
		self.resets += 1

	def __eq__(self, other: Racecar) -> bool:
		"""Checks if this racecar and other racecar are equal via id."""
		return self.id == other.id

