from unittest import TestCase
import numpy as np

from benchmarks.base_functions import sphere as base_sphere
from benchmarks.shifted_functions import generate_shift_vector
from benchmarks.rotated_functions import generate_rotation_matrix
from benchmarks.continuous_functions import sphere
from benchmarks.continuous_functions import _load_shift_and_rotation
from benchmarks.test_base_functions import Sample


class RotatedShiftedSample(Sample):
    """Test correctness of rotated-shifted function via sampling (test cases).
    """
    def __init__(self, ndim=None):
        Sample.__init__(self, ndim)

    def compare_rotated_shifted_func_values(self, func, ndim, y_true,
                                            atol=1e-08, shift_vector=None, rotation_matrix=None):
        """Compare true (expected) function values with these returned (computed) by rotated-shifted function.

        :param func: rotated-shifted function, a function object.
        :param ndim: number of dimensions, an `int` scalar ranged in [1, 7].
        :param y_true: a 1-d `ndarray`, where each element is the true function value of the corresponding test case.
        :param atol: absolute tolerance parameter, a `float` scalar.
        :param shift_vector: shift vector, array_like of floats.
        :param rotation_matrix: rotation matrix, array_like of floats.
        :return: `True` if all function values computed on test cases match `y_true`; otherwise, `False`.
        """
        x = self.make_test_cases(ndim)
        y = np.empty((x.shape[0],))
        for i in range(x.shape[0]):
            shift_vector, rotation_matrix = _load_shift_and_rotation(func, x[i], shift_vector, rotation_matrix)
            y[i] = func(np.dot(np.linalg.inv(rotation_matrix), x[i]) + shift_vector)
        return np.allclose(y, y_true, atol=atol)


class Test(TestCase):
    def test_load_shift_and_rotation(self):
        func, ndim, seed = base_sphere, 2, 1
        generate_shift_vector(func, 2, [-1, -2], [1, 2], 0)
        generate_rotation_matrix(func, ndim, seed)
        shift_vector, rotation_matrix = _load_shift_and_rotation(func, [0, 0])
        self.assertTrue(np.allclose(shift_vector, [2.739233746429086125e-01, -9.208531449445187533e-01]))
        self.assertTrue(np.allclose(rotation_matrix, [[7.227690004350708630e-01, 6.910896989610599839e-01],
                                                      [6.910896989610598729e-01, -7.227690004350709740e-01]]))

    def test_sphere(self):
        for ndim in range(1, 8):
            generate_shift_vector(sphere, ndim, -100, 100, seed=0)
            generate_rotation_matrix(sphere, ndim, 0)
        rotated_shifted_sample = RotatedShiftedSample()
        x1 = [4, 1, 0, 1, 4]
        self.assertTrue(rotated_shifted_sample.compare_rotated_shifted_func_values(sphere, 1, x1))
        x2 = [8, 2, 0, 2, 8]
        self.assertTrue(rotated_shifted_sample.compare_rotated_shifted_func_values(sphere, 2, x2))
        x3 = [12, 3, 0, 3, 12]
        self.assertTrue(rotated_shifted_sample.compare_rotated_shifted_func_values(sphere, 3, x3))
        x4 = [0, 4, 4, 4, 30, 30, 30]
        self.assertTrue(rotated_shifted_sample.compare_rotated_shifted_func_values(sphere, 4, x4))
        x5 = [0, 5, 5, 5, 55, 55, 55]
        self.assertTrue(rotated_shifted_sample.compare_rotated_shifted_func_values(sphere, 5, x5))
        x6 = [0, 6, 6, 6, 91, 91, 91]
        self.assertTrue(rotated_shifted_sample.compare_rotated_shifted_func_values(sphere, 6, x6))
        x7 = [0, 7, 7, 7, 140, 140, 140, 91]
        self.assertTrue(rotated_shifted_sample.compare_rotated_shifted_func_values(sphere, 7, x7))
