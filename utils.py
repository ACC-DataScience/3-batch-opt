import numpy as np
import torch
import random

def set_seeds(seed: int = 42):
    """Set random seeds for reproducibility."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    random.seed(seed)

def measure_erosion(pg_rate, sg_rate, current, cg_rate, pf_rate, distance):
    """
    Hartmann 6-dimensional function modified to support the erosion problem

    Parameters:
    -----------
    pg_rate : float
        Flow rate of the primary gas in standard liters per minute (SLPM). Historically ranges from 30 to 80 SLPM.
    sg_rate : float
        Flow rate of the secondary gas in standard liters per minute (SLPM). Historically ranges from 10 to 50 SLPM.
    current : float
        Electric current of the gun in amperes (A). Historically ranges from 300 to 800 A.
    cg_rate : float
        Flow rate of the carrier gas in standard liters per minute (SLPM). Historically ranges from 2 to 10 SLPM.
    pf_rate : float
        Feed rate of the power in grams per minute (g/min). Historically ranges from 10 to 100 g/min.
    distance : float
        Distance of the spray in millimeters (mm). Historically ranges from 50 to 150 mm.

    Returns:
    --------
    float
        Measured erosion of the alloy.
    """
    # rescale to 0, 1

    inputs = np.array([pg_rate, sg_rate, current, cg_rate, pf_rate, distance])
    low_bound = np.array([30, 10, 300, 2, 10, 50])
    up_bound = np.array([80, 50, 800, 10, 100, 150])

    scaled_inputs = (inputs - low_bound) / (up_bound - low_bound)

    alpha = np.array([1.0, 1.2, 3.0, 3.2])

    A = np.array([[10, 3, 17, 3.5, 1.7, 8],
                  [0.05, 10, 17, 0.1, 8, 14],
                  [3, 3.5, 1.7, 10, 17, 8],
                  [17, 8, 0.05, 10, 0.1, 14]])
    
    P = 10**(-4) * np.array([[1312, 1696, 5569, 124, 8283, 5886],
                             [2329, 4135, 8307, 3736, 1004, 9991],
                             [2348, 1451, 3522, 2883, 3047, 6650],
                             [4047, 8828, 8732, 5743, 1091, 381]])

    outer = 0
    for ii in range(4):
        inner = 0
        for jj in range(6):
            xj = scaled_inputs[jj]
            Aij = A[ii, jj]
            Pij = P[ii, jj]
            inner += Aij * (xj - Pij)**2
        outer += alpha[ii] * np.exp(-inner)

    y = -(2.58 + outer) / 1.94 + 3.1
    return y

def validate_parameters(parameters):
    """Validate parameter values before running optimization"""
    required_fields = ["name", "type", "bounds", "value_type"]
    try:
        for param in parameters:
            if not all(field in param for field in required_fields):
                raise ValueError(f"Parameter missing required fields: {required_fields}")
            
            if param["type"] != "range":
                raise ValueError(f"Unsupported parameter type: {param['type']}")
                
            if len(param["bounds"]) != 2:
                raise ValueError(f"Invalid bounds for parameter {param['name']}")
                
            if param["bounds"][0] >= param["bounds"][1]:
                raise ValueError(f"Invalid bounds range for parameter {param['name']}")
    except Exception as e:
        raise ValueError(f"Parameter validation failed: {e}")

def check_stress_constraint(params):
    """Check if parameters satisfy the device stress constraint"""
    try:
        stress = params["pg_rate"] + params["sg_rate"] + params["current"]
        return stress <= 750
    except KeyError as e:
        raise ValueError(f"Missing parameter for stress calculation: {e}")
    except Exception as e:
        raise ValueError(f"Error in stress constraint check: {e}")