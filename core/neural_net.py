"""
Contains basic feed forward neural network class.
"""

from numba import jit
import numpy as np


class FFNN:
	"""
	Feed forward neural network without backpropogation.

	Public Methods
	--------------
	feedForward(a) -> np.ndarray:
		Feeds inputs through neural net to obtain output.
	"""
	def __init__(self, layerSizes: list, activation: str = "sigmoid", outputActivation: str = "softmax", weights: list = None, biases: list = None) -> None:
		"""
		Initializes.

		Parameters
		----------
		layerSizes: list
			Layer architecture
		activation: str, default="sigmoid"
			String denoting activation function to use
		outputActivation: str, default="softmax"
			String denoting output layer activation function to use
		weights: list, optional
			List of arrays of weights for each layer, randomized if not passed in
		biases: list, optional
			List of arrays of biases for each layer, randomized if not passed in
		"""
		activations = {
			"sigmoid": FFNN.sigmoid,
			"reLu": FFNN.reLu,
			"softmax": FFNN.softmax,
			"linear": FFNN.linear
		}
		self.layerSizes = layerSizes
		weightShapes = [(i, j) for i, j in zip(layerSizes[1:], layerSizes[:-1])]
		self.weights = [np.random.randn(*s) for s in weightShapes] if weights is None else weights
		self.biases = [np.random.standard_normal(s) for s in layerSizes[1:]] if biases is None else biases
		self.activation = activations[activation]
		self.outputActivation = activations[outputActivation]

	def feedForward(self, a: np.ndarray) -> np.ndarray:
		"""
		Feeds inputs through neural net to obtain output.

		Parameters
		----------
		a: np.ndarray
			Inputs to neural network

		Returns
		-------
		np.ndarray: input after fed through neural network
		"""
		for w, b in zip(self.weights[:-1], self.biases[:-1]):
			a = self.activation(a @ w.T + b)
		return self.outputActivation(a @ self.weights[-1].T + self.biases[-1])

	def get_params(self) -> dict:
		return {
			"weights": self.weights,
			"biases": self.biases,
			"architecture": self.layerSizes,
			"activation": self.activation.__name__,
			"output activation": self.outputActivation.__name__,
		}

	@staticmethod
	@jit(nopython=True)
	def sigmoid(x: float) -> float:
		"""Sigmoid."""
		return 1 / (1 + np.exp(-x))

	@staticmethod
	@jit(nopython=True)
	def reLu(x: float) -> float:
		"""Rectified linear unit."""
		return np.maximum(0, x)

	@staticmethod
	@jit(nopython=True)
	def softmax(v: np.ndarray) -> np.ndarray:
		"""Softmax probability output."""
		e = np.exp(v)
		return e / e.sum()	

	@staticmethod
	def linear(x: float) -> float:
		"""Linear activation"""
		return x
	
