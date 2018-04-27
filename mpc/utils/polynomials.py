import random
import operator
import functools

from mpc.field import (
    FieldElement,
)

def generate_random_polynomial_by_intercept(degree, field, intercept, seed=None):
    """
    Generates a random polynomial with positive coefficients.
    """
    assert degree >= 0, 'Degree cannot be negative'

    random.seed(seed)

    return [intercept] + [field(random.randint(0, field.modulus)) for _ in range(degree)]

def generate_random_polynomial_by_root(degree, field, root, seed=None):
    """
    Generates a random polynomial with positive coefficients.
    """
    assert degree >= 0, 'Degree cannot be negative'

    random.seed(seed)

    polynomial = []
    last_rand = 0

    for x in range(degree + 1):
        rand = field(random.randint(0, field.modulus))

        if x == degree:
            polynomial.append(-last_rand)
        else:
            polynomial.append(root * rand - last_rand)
            last_rand = rand

    return polynomial

def evaluate_polynomial(coefficients, points, field):
    results = []
    num_coef = len(coefficients)

    for x in points:
        cur_point = x if isinstance(x, FieldElement) else field(x)
        cur_share = coefficients[num_coef - 1]

        for j in range(num_coef - 2, -1, -1):
            cur_share = coefficients[j] + cur_share * cur_point

        results.append((cur_point, cur_share))

    return results

def lagrange_interpolation(x, points):
    # break the points up into lists of x and y values
    x_values, y_values = zip(*points)

    vector = []
    for i, x_i in enumerate(x_values):
        factors = [(x_k - x) / (x_k - x_i) for k, x_k in enumerate(x_values) if k != i]
        vector.append(functools.reduce(operator.mul, factors))

    # print("\nhehe", y_values, vector)

    return sum(map(operator.mul, y_values, vector))

def verify_polynomial(points, degree):
    """
    Verifies that a sharing is correct.

    It is verified that the given shares correspond to points on a
    polynomial of at most the given degree.
    """
    used_points = points[0:degree + 1]

    for i in range(degree + 1, len(points) + 1):
        if lagrange_interpolation(i, used_points) != points[i - 1][1]:
            return False

    return True