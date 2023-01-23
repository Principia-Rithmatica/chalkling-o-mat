from typing import List, Tuple

import numpy as np
from scipy.special import comb


# See https://stackoverflow.com/questions/12643079/b%C3%A9zier-curve-fitting-with-scipy


def bernstein_poly(i: int, n: int, t):
    """
     The Bernstein polynomial of n, i as a function of t
    """

    return comb(n, i) * (t ** (n - i)) * (1 - t) ** i


def bezier_curve(points: List[Tuple[float, float]], n_times: int = 10) -> List[Tuple[float, float]]:
    """
       Given a set of control points, return the
       bezier curve defined by the control points.

       points should be a list of lists, or list of tuples
       such as [ [1,1],
                 [2,3],
                 [4,5], ..[Xn, Yn] ]
        nTimes is the number of time steps, defaults to 1000

        See http://processingjs.nihongoresources.com/bezierinfo/
    """

    n_points = len(points)
    x_points = np.array([p[0] for p in points])
    y_points = np.array([p[1] for p in points])

    t = np.linspace(0.0, 1.0, n_times)

    polynomial_array = np.array([bernstein_poly(i, n_points - 1, t) for i in range(0, n_points)])

    x_vals = np.dot(x_points, polynomial_array)
    y_vals = np.dot(y_points, polynomial_array)

    return list(zip(x_vals, y_vals))
