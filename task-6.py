import pytest
import json
import numpy as np
from scipy.integrate import ode
from pathlib import Path
from matplotlib import pyplot as plt
from pendulum_simulator import PendulumDynamics, Simulator


data_folder = Path('tests', 'task-6-data')
ASSERT_PLOT = False
ALWAYS_PLOT = False
PLOT = ALWAYS_PLOT or ALWAYS_PLOT


def plot_graphs(submitted, expected, task_title=None):
    s_t, s_th, s_dth = submitted
    e_t, e_th, e_dth = expected

    extra_title = f" for \"{task_title}\"" if task_title is not None else ""

    plt.figure()
    plt.grid()
    plt.plot(e_t, 'go--')
    plt.plot(s_t, 'ro')
    plt.title("t" + extra_title)

    plt.figure()
    plt.grid()
    plt.plot(e_t, e_th, 'g')
    plt.plot(s_t, s_th, 'r--')
    plt.title("Theta(t)" + extra_title)

    plt.figure()
    plt.grid()
    plt.plot(e_t, e_dth, 'g')
    plt.plot(s_t, s_dth, 'r--')
    plt.title("dTheta(t)" + extra_title)
    plt.show()


def gen_config(control_points: int):
    np.random.seed(12)
    mass = np.random.uniform(0.1, 5)
    length = np.random.uniform(1, 1.5)
    g = np.random.normal(9.8, 0.5)
    system = {
        "inertia_momentum": mass * (length ** 2) + np.random.uniform(1E-4, mass**2),
        "dry_friction": np.random.random()*0.7,
        "viscous_friction": np.random.random()*0.5,
        "mass": mass,
        "length": length,
        "gravity_accel": g
    }
    time = np.linspace(0, 5, control_points)
    simulation = {
        "control_input":
            {
                "time": time.tolist(),
                "value": (np.sin(time) * 2).tolist()
            },
        "initial_state": [0., 0.]
    }

    config = {
        "system_parameters": system,
        "simulation_parameters": simulation
    }
    return config


def get_params(filename):
    with open(filename) as f:
        return json.load(f)


class KindaWrongSolution:  # Испорченный вариант реализации, вам нужно сделать правильно :)

    def __init__(self, params):
        self.J = params["system_parameters"]["inertia_momentum"]
        self.kd = params["system_parameters"]["dry_friction"]
        self.kv = params["system_parameters"]["viscous_friction"]
        self.m = params["system_parameters"]["mass"]
        self.L = params["system_parameters"]["length"]
        self.g = params["system_parameters"]["gravity_accel"]
        self.t_array = params["simulation_parameters"]["control_input"]["time"]
        self.u_array = params["simulation_parameters"]["control_input"]["value"]
        self.initial_state = params["simulation_parameters"]['initial_state']
        self.u = 0

    def eval_u(self, time):
        for i, t in enumerate(self.t_array):
            if t >= time:
                return self.u_array[i]
        return self.u_array[-1]

    @staticmethod
    def soft_sign(x):
        eps = 1e-2
        return x / (abs(x) + eps)

    def call(self, t, state):
        theta, dtheta = state
        d2theta = (-self.kd*self.soft_sign(dtheta) - self.kv*dtheta -
                   self.m * self.g * self.L * np.sin(theta) +
                   self.u) / self.J
        # print(t, dtheta)
        return [dtheta, d2theta]

    def run(self):

        solver = ode(self.call)
        solver.set_integrator('dopri5', atol=1e-8, rtol=1e-8, max_step=1e-3, nsteps=1000)
        solver = solver.set_initial_value(self.initial_state)
        theta = [self.initial_state[0]]
        dtheta = [self.initial_state[1]]

        for t, u in zip(self.t_array[1:], self.u_array[:-1]):
            # print(t, u)
            assert solver.successful()
            self.u = u
            th, dth = solver.integrate(t)
            theta.append(th)
            dtheta.append(dth)

        return self.t_array, theta, dtheta


def match_solutions(submitted, expected):
    s_t, s_th, s_dth = submitted
    e_t, e_th, e_dth = expected
    assert len(s_t) == len(e_t), f"Your solution has wrong size, " \
                                 f"you should return values only for the given timestamps, " \
                                 f"expected t = \n{e_t}\nbut got t_actual = \n{s_t}"
    assert len(s_th) == len(e_th), f"Your solution has wrong size, " \
                                   f"you should return values only for the given timestamps, " \
                                   f"expected theta = \n{e_th}\nbut got theta_actual = \n{s_th}"
    assert len(s_dth) == len(e_dth), f"Your solution has wrong size, " \
                                     f"you should return values only for the given timestamps, " \
                                     f"expected dtheta = \n{e_dth}\nbut got dtheta_actual = \n{s_dth}"

    assert np.all(np.isclose(np.array(s_t), np.array(e_t))), \
        f"Your solution has wrong t, " \
        f"expected t = \n{e_t}\nbut got t_actual = \n{s_t}"
    assert np.all(np.isclose(np.array(s_th), np.array(e_th))),\
        f"Your solution has wrong theta, " \
        f"expected theta = \n{e_th}\nbut got t_actual = \n{s_th}"
    assert np.all(np.isclose(np.array(s_dth), np.array(e_dth))), \
        f"Your solution has wrong t, " \
        f"expected t = \n{e_dth}\nbut got t_actual = \n{s_dth}"


def get_student_solution(config):

    J = config["system_parameters"]["inertia_momentum"]
    Kd = config["system_parameters"]["dry_friction"]
    Kv = config["system_parameters"]["viscous_friction"]
    m = config["system_parameters"]["mass"]
    L = config["system_parameters"]["length"]
    g = config["system_parameters"]["gravity_accel"]
    t_array = config["simulation_parameters"]["control_input"]["time"]
    u_array = config["simulation_parameters"]["control_input"]["value"]
    initial_state = config["simulation_parameters"]['initial_state']

    pendulum = PendulumDynamics(J=J, Kd=Kd, Kv=Kv, m=m, L=L, g=g)
    simulator = Simulator(t_array=t_array, u_array=u_array,
                          initial_state=initial_state,
                          dynamics=pendulum)
    return simulator.run()


def get_expected_solution(config):
    return KindaWrongSolution(config).run()


@pytest.mark.timeout(30 if not PLOT else 0)
def test_zero_u():
    config_name = 'parameters1.json'
    config = get_params(Path(data_folder, config_name))
    student_sol = get_student_solution(config)
    expected_sol = get_expected_solution(config)

    if ALWAYS_PLOT:
        plot_graphs(student_sol, expected_sol, 'zero_u')

    try:
        match_solutions(student_sol, expected_sol)
    except AssertionError:
        if ASSERT_PLOT:
            plot_graphs(student_sol, expected_sol, 'zero_u')
        raise


@pytest.mark.timeout(30 if not PLOT else 0)
def test_stable_u():
    config_name = 'stable-u.json'
    config = get_params(Path(data_folder, config_name))
    student_sol = get_student_solution(config)
    expected_sol = get_expected_solution(config)

    if ALWAYS_PLOT:
        plot_graphs(student_sol, expected_sol, 'stable_u')

    try:
        match_solutions(student_sol, expected_sol)
    except AssertionError:
        if ASSERT_PLOT:
            plot_graphs(student_sol, expected_sol, 'stable_u')
        raise


@pytest.mark.timeout(30 if not PLOT else 0)
def test_cos_u():
    config_name = 'cos-u.json'
    config = get_params(Path(data_folder, config_name))
    student_sol = get_student_solution(config)
    expected_sol = get_expected_solution(config)

    if ALWAYS_PLOT:
        plot_graphs(student_sol, expected_sol, 'cos_u')

    try:
        match_solutions(student_sol, expected_sol)
    except AssertionError:
        if ASSERT_PLOT:
            plot_graphs(student_sol, expected_sol, 'cos_u')
        raise


@pytest.mark.timeout(30 if not PLOT else 0)
def test_sin_u():
    config_name = 'sin-u.json'
    config = get_params(Path(data_folder, config_name))
    student_sol = get_student_solution(config)
    expected_sol = get_expected_solution(config)

    if ALWAYS_PLOT:
        plot_graphs(student_sol, expected_sol, 'sin_u')

    try:
        match_solutions(student_sol, expected_sol)
    except AssertionError:
        if ASSERT_PLOT:
            plot_graphs(student_sol, expected_sol, 'sin_u')
        raise


@pytest.mark.timeout(30 if not PLOT else 0)
def test_lots_of_u():
    config_name = 'lots-of-u.json'
    config = get_params(Path(data_folder, config_name))
    student_sol = get_student_solution(config)
    expected_sol = get_expected_solution(config)

    if ALWAYS_PLOT:
        plot_graphs(student_sol, expected_sol, 'lots-of-u')
    try:
        match_solutions(student_sol, expected_sol)
    except AssertionError:
        if ASSERT_PLOT:
            plot_graphs(student_sol, expected_sol, 'lots-of-u')
        raise
