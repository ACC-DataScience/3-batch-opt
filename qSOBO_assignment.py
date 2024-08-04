# ======================================================================================
# ASSIGNMENT 3: Optimizing APS Coating Parameters in Batches

# Your assignment is to use Honegumi to develop an optimization script to help
# you identify a set of parameters minimizes the material mass loss in the
# erosion trials. Your experimental budget is limited to 30 experiments divided
# into batches of three. A synthetic objective function has been provided that
# will serve as a proxy for real experimental measurements. Refer to the README
# for specifics regarding each task.
# ======================================================================================

from utils import set_seeds, measure_erosion

set_seeds()  # setting the random seed for reproducibility

# --------------------------------------------------------------------------------------
# TASK A: Use Honegumi to set up and run the optimization problem.
# --------------------------------------------------------------------------------------

import numpy as np
from ax.service.ax_client import AxClient, ObjectiveProperties

ax_client = AxClient(random_seed=42)

# TODO: Your Code Goes Here

# --------------------------------------------------------------------------------------
# TASK B: Report the optimal parameters, associted erosion rate, and the stress_index
# --------------------------------------------------------------------------------------

# TODO: Your Code Goes Here

# --------------------------------------------------------------------------------------
# TASK C: How many solutions have a stress index > 700
# --------------------------------------------------------------------------------------

# TODO: Your Code Goes Here

# --------------------------------------------------------------------------------------
# TASK D: On average, how many experiments per batch were lower than the previous best?
# --------------------------------------------------------------------------------------

df = ax_client.get_trials_data_frame()
df["batch"] = df.index // 3

# TODO: Your Code Goes Here

# --------------------------------------------------------------------------------------
# TASK E: Which non-sobol batch was the most and least diverse in terms parameters?
# --------------------------------------------------------------------------------------

# *combinations* can help you get all pairs of input vectors
from itertools import combinations

df = ax_client.get_trials_data_frame()
df["batch"] = df.index // 3

# TODO: Your Code Goes Here
