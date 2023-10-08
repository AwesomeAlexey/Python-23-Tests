import pytest
import numpy as np
import os

filename = '../bases.txt'
field_size = 100


def gen_data(nbases):
    np.random.seed(0)
    data_ = np.random.rand(nbases, 3)
    data_ = (data_ * 100).astype(np.int32)
    data_[:, 2] += 1
    np.savetxt(filename, data_, fmt='%d')
    return data_


def get_mask(data_, x_, y_, radius_):
    return (data_[:, 0] - x_) ** 2 + (data_[:, 1] - y_) ** 2 <= radius_ ** 2


def get_estimation(data_, x_, y_, radius_):
    mask_ = get_mask(data_, x_, y_, radius_)
    return np.sum(data_[mask_, 2])


def compress_data(data_):
    field = np.zeros((100, 100))
    for base in data_:
        x, y, w = base
        field[x, y] += w
    new_data = []

    for x in range(0, 100):
        for y in range(0, 100):
            if field[x, y] > 0:
                new_base = [x, y, field[x, y]]
                new_data.append(new_base)
    return np.array(new_data)


def suboptimal_solution(data, radius):
    max_x = 0
    max_y = 0
    max_points = 0
    steps = 1
    X = np.linspace(0, field_size, (field_size * steps) + 1)
    Y = np.linspace(0, field_size, (field_size * steps) + 1)

    for x in X:
        for y in Y:
            points = get_estimation(data, x, y, radius)
            if points >= max_points:
                max_points = points
                max_x = x
                max_y = y

    return max_x, max_y, max_points


@pytest.mark.timeout(240)
def test_missile_attack():
    nbases = 1_000
    radius = 10
    data = gen_data(nbases)
    data = compress_data(data)
    outfile = '../outfile.txt'
    os.system(f"rm {outfile}")
    os.system(f"python3 ../app.py {filename} {radius} >> {outfile}")

    x, y, points = np.loadtxt(outfile)

    expected_points = get_estimation(data, x, y, radius)
    assert points == expected_points, f"Your program calculate wrong points. " \
                                      f"For point ({x}, {y}) and radius = {radius} " \
                                      f"you got {points} pts, but here it is {expected_points}"

    sx, sy, s_points = suboptimal_solution(data, radius)

    assert s_points == get_estimation(data, sx, sy, radius), f"Something went wrong with the tests, " \
                                                             f"please contact the devs"

    assert points >= s_points, f"Your solution is not good enough. You got {points}, but on that field " \
                               f"you can have at least {s_points} (even with an integer coordinates)"


@pytest.mark.timeout(240)
def test_missile_attack_small():
    nbases = 1_00
    radius = 15
    data = gen_data(nbases)
    data = compress_data(data)
    outfile = '../outfile.txt'
    os.system(f"rm {outfile}")
    os.system(f"python3 ../app.py {filename} {radius} >> {outfile}")

    x, y, points = np.loadtxt(outfile)

    expected_points = get_estimation(data, x, y, radius)
    assert points == expected_points, f"Your program calculate wrong points. " \
                                      f"For point ({x}, {y}) and radius = {radius} " \
                                      f"you got {points} pts, but here it is {expected_points}"

    sx, sy, s_points = suboptimal_solution(data, radius)

    assert s_points == get_estimation(data, sx, sy, radius), f"Something went wrong with the tests, " \
                                                             f"please contact the devs"

    assert points >= s_points, f"Your solution is not good enough. You got {points}, but on that field " \
                               f"you can have at least {s_points} (even with an integer coordinates)"
