# ======================================================================================
# ASSIGNMENT 3: Optimizing APS Coating Parameters in Batches

# Your assignment is to use Honegumi to develop an optimization script to help
# you identify a set of parameters minimizes the material mass loss in the
# erosion trials. Your experimental budget is limited to 30 experiments divided
# into batches of three. A synthetic objective function has been provided that
# will serve as a proxy for real experimental measurements. Refer to the README
# for specifics regarding each task.
# ======================================================================================

from utils import set_seeds, measure_erosion, validate_parameters, check_stress_constraint
import pandas as pd
import numpy as np
from ax.service.ax_client import AxClient, ObjectiveProperties
from itertools import combinations
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

set_seeds()  # setting the random seed for reproducibility

# Error handling for ax_client initialization
try:
    ax_client = AxClient(random_seed=42)
except Exception as e:
    logger.error(f"Failed to initialize AxClient: {e}")
    raise RuntimeError(f"Failed to initialize AxClient: {e}")

# TASK A: Set up optimization problem
parameters = [
    {
        "name": "pg_rate",
        "type": "range",
        "bounds": [30.0, 80.0],
        "value_type": "float",
    },
    {
        "name": "sg_rate", 
        "type": "range",
        "bounds": [10.0, 50.0],
        "value_type": "float",
    },
    {
        "name": "current",
        "type": "range", 
        "bounds": [300.0, 800.0],
        "value_type": "float",
    },
    {
        "name": "cg_rate",
        "type": "range",
        "bounds": [2.0, 10.0],
        "value_type": "float",
    },
    {
        "name": "pf_rate",
        "type": "range",
        "bounds": [10.0, 100.0],
        "value_type": "float",
    },
    {
        "name": "distance",
        "type": "range",
        "bounds": [50.0, 150.0],
        "value_type": "float",
    },
]

try:
    # Validate parameters before optimization
    validate_parameters(parameters)
    
    # Add parameters to ax_client
    ax_client.create_experiment(
        name="coating_optimization",
        parameters=parameters,
        objective_name="mass_loss",
        minimize=True,
    )
except Exception as e:
    logger.error(f"Failed to setup experiment: {e}")
    raise

# Run optimization with batches
for batch in range(10):
    try:
        for _ in range(3):
            parameters, trial_index = ax_client.get_next_trial()
            
            # Check device stress constraint
            while not check_stress_constraint(parameters):
                parameters, trial_index = ax_client.get_next_trial()
            
            # Run experiment with error handling
            try:
                mass_loss = measure_erosion(
                    parameters["pg_rate"],
                    parameters["sg_rate"],
                    parameters["current"],
                    parameters["cg_rate"],
                    parameters["pf_rate"],
                    parameters["distance"]
                )
            except Exception as e:
                logger.error(f"Error in measure_erosion: {e}")
                raise
                
            ax_client.complete_trial(trial_index=trial_index, raw_data=mass_loss)
            
    except Exception as e:
        logger.error(f"Error in batch {batch}: {e}")
        raise

# Process results with error handling
try:
    best_parameters, metrics = ax_client.get_best_parameters()
    optimal_params = best_parameters
    min_mass_loss = metrics["mass_loss"]
    device_stress_index = optimal_params["pg_rate"] + optimal_params["sg_rate"] + optimal_params["current"]
except Exception as e:
    logger.error("Failed to get optimization results")
    raise

# Data processing for analysis tasks
try:
    df = ax_client.get_trials_data_frame()
    if df.empty:
        raise ValueError("No optimization results available")
        
    df["batch"] = df.index // 3
    df["stress_index"] = df["pg_rate"] + df["sg_rate"] + df["current"]
    
    # Task C
    threshold = df["mass_loss"].quantile(0.15)
    bottom_15_df = df[df["mass_loss"] <= threshold]
    high_stress_count = len(bottom_15_df[bottom_15_df["stress_index"] > 700])
    
    # Task D
    improvements = []
    for batch_num in range(4, 10):
        prev_min = df[df["batch"] < batch_num]["mass_loss"].min()
        batch_data = df[df["batch"] == batch_num]
        improvements.append(sum(batch_data["mass_loss"] < prev_min))
    
    avg_lower = np.mean(improvements) if improvements else 0
    
    # Task E
    batch_diversity = {}
    param_cols = ["pg_rate", "sg_rate", "current", "cg_rate", "pf_rate", "distance"]
    
    for batch_num in range(4, 10):
        batch_data = df[df["batch"] == batch_num]
        if len(batch_data) >= 2:  # Ensure we have enough points for pairwise distances
            params = batch_data[param_cols].values
            distances = [np.linalg.norm(p1 - p2) for p1, p2 in combinations(params, 2)]
            batch_diversity[batch_num] = np.mean(distances) if distances else 0
            
    most_diverse = max(batch_diversity.items(), key=lambda x: x[1])[0] if batch_diversity else 4
    least_diverse = min(batch_diversity.items(), key=lambda x: x[1])[0] if batch_diversity else 4
    
except Exception as e:
    logger.error(f"Error in data analysis: {e}")
    raise
