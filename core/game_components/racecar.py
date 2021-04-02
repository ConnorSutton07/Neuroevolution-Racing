"""
Race car with neural network decision making.
"""

from __future__ import annotations
import numpy as np

from core.neural_net import FFNN

class Racecar:
	"""Haven't tested any of this yet."""
	def __init__(
			self,
			id: str = "",
			architecture: tuple = (8, 6, 2),
			initial_pos: np.ndarray = None,
			initial_vel: np.ndarray = None,
			initial_accel: np.ndarray = None,
			max_turning_rate: float = np.radians(135),
			max_acceleration: float = 5,
			) -> None:
		self.id = id  # this should be base 36 number for uniqueness and to minimize digits
		self.network = FFNN(architecture, outputActivation = "linear")  # can decide steering, acceleration
		self.initial_p = initial_pos if initial_pos is not None else np.array([0., 0.])  # position
		self.initial_v = initial_vel if initial_vel is not None else np.array([0., 0.])  # velocity
		self.initial_a = initial_accel if initial_accel is not None else np.array([0., 0.])  # acceleration
		self.p = self.initial_p.copy()
		self.v = self.initial_v.copy()
		self.a = self.initial_a.copy()
		self.max_turning_rate = max_turning_rate
		self.max_acceleration = max_acceleration
		self.steps = 0  # number of steps made
		self.alive = True
		self.resets = 0  # num times this racecar has been reset

	def step(self) -> None:
		"""Updates cars state."""
		self.p += self.v
		self.v += self.a
		self.steps += 1

	def autostep(self, rayLengths: np.ndarray) -> None:
		""""Calculates AI controls then takes a step."""
		steering, throttle = self.get_optimal_controls(rayLengths)
		self.turn(steering)
		self.accelerate(throttle)
		self.step()

	def turn(self, d_theta: float) -> None:
		"""Rotates direction ccw by theta degrees in radians, def need to test this."""
		d_theta = (d_theta / abs(d_theta)) * min(abs(d_theta), self.max_turning_rate)
		cos_d_theta = np.cos(d_theta)
		sin_d_theta = np.sin(d_theta)
		self.v = np.array([[cos_d_theta, -sin_d_theta], [sin_d_theta, cos_d_theta]]) @ self.v

	def get_optimal_controls(self, rayLengths: np.ndarray) -> np.ndarray:
		"""Gets turn angle from neural network."""
		return self.network.feedForward(rayLengths)  # steering angle, acceleartion

	def accelerate(self, a) -> None:
		"""Sets acceleration."""
		self.a = min(a, self.max_acceleration)

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

	def get_state(self) -> dict:
		"""Returns info about racecar's state"""
		return {
			"pos": self.p,
			"vel": self.v,
			"accel": self.a,
			"alive": self.alive,
		}

	def __eq__(self, other: Racecar) -> bool:
		"""Checks if this racecar and other racecar are equal via id."""
		return self.id == other.id

