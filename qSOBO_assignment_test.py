import os
import warnings
from utils import set_seeds, measure_erosion
import numpy as np
from ax.service.ax_client import AxClient, ObjectiveProperties
import matplotlib.pyplot as plt
import pytest


@pytest.fixture(scope="session")
def get_namespace():
    script_fname = "qSOBO_assignment.py"
    script_content = open(script_fname).read()

    namespace = {}
    exec(script_content, namespace)
    return namespace


def test_task_a(get_namespace):

    running_ax_client = get_namespace["ax_client"]
    user_op_params = running_ax_client.experiment.parameters

    assert len(user_op_params) == 6, "Expected 6 parameters, got {}".format(
        len(user_op_params)
    )

    assert all(
        [
            param in ["pg_rate", "sg_rate", "current", "cg_rate", "pf_rate", "distance"]
            for param in user_op_params
        ]
    ), "Expected parameters named ['pg_rate', 'sg_rate', 'current', 'cg_rate', 'pf_rate', 'distance'], got {}".format(
        user_op_params.keys()
    )

    assert (
        len(running_ax_client.get_trials_data_frame()) == 30
    ), "Expected optimization budget of 30 trials, got {}".format(
        len(running_ax_client.get_trials_data_frame())
    )


def test_task_b(get_namespace):

    # optimal_params
    # min_mass_loss
    # device_stress_index

    user_optimal_params = get_namespace["optimal_params"]
    user_min_mass_loss = get_namespace["min_mass_loss"]
    user_device_stress_index = get_namespace["device_stress_index"]

    # assert optimal current is above 610
    assert (
        user_optimal_params["current"] > 610.0
    ), "Expected optimal current to be > 610, got {}".format(
        user_optimal_params["current"]
    )

    # asset min mass loss less than 0.3
    assert user_min_mass_loss < 0.3, "Expected min_mass_loss < 0.3, got {}".format(
        user_min_mass_loss
    )

    # assert device stress index is less than 700
    assert (
        user_device_stress_index < 700
    ), "Expected device_stress_index < 700, got {}".format(user_device_stress_index)


def test_task_c(get_namespace):

    user_high_stress_count = get_namespace["high_stress_count"]

    assert user_high_stress_count == 1, "Expected high_stress_count: 1, got {}".format(
        user_high_stress_count
    )


def test_task_d(get_namespace):

    user_avg_lower = get_namespace["avg_lower"]

    assert user_avg_lower < 1.7, "Expected avg_lower < 1.7, got {}".format(
        user_avg_lower
    )


def test_task_e(get_namespace):

    user_most_diverse = get_namespace["most_diverse"]
    user_least_diverse = get_namespace["least_diverse"]

    assert user_most_diverse == 4, "Expected most_diverse: 6, got {}".format(
        user_most_diverse
    )

    assert user_least_diverse == 9, "Expected least_diverse: 9, got {}".format(
        user_least_diverse
    )
