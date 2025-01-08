# Batch Optimization: Optimizing Erosion Resistant Coating Parameters

## Overview

This project focuses on optimizing the erosion resistance of protective coatings using Atmospheric Plasma Spraying (APS) through batch optimization techniques.

## Problem Context

### Background
Atmospheric Plasma Spraying (APS) is used to deposit protective coatings on material substrates. The goal is to apply a high-hardness metallic coating to improve erosion resistance, measured by mass loss under sand blasting.

### Optimization Challenge
- Testing requires shipping samples to a specialized laboratory
- Each test takes approximately 4 days
- Budget: 30 experiments total
- Solution: Batch optimization approach (3 samples per batch)
- Total optimization time reduced from 120 to 40 days

### Design Space Parameters

| Parameter               | Range          | Units  |
|------------------------|----------------|--------|
| Primary Gas Flow Rate  | 30 - 80       | SLPM   |
| Secondary Gas Flow Rate| 10 - 50       | SLPM   |
| Gun Current           | 300 - 800     | A      |
| Carrier Gas Flow Rate | 2 - 10        | SLPM   |
| Power Feed Rate       | 10 - 100      | g/min  |
| Spray Distance        | 50 - 150      | mm     |

### Device Constraint
To protect the APS device, the following constraint must be satisfied:
```python
device_stress_index = primary_gas_flow_rate + secondary_gas_flow_rate + gun_current <= 750
```

## Tasks

### Task A: Optimization Setup
Use Honegumi to set up and run the optimization problem:
- Configure parameters and constraints
- Implement batch processing
- Handle device stress constraints

### Task B: Results Analysis
Report:
- Optimal parameters
- Associated erosion rate
- Device stress index

### Task C: Stress Analysis
Calculate the number of solutions in the bottom 15% of trials that have a stress index > 700.

### Task D: Batch Performance Analysis
For non-Sobol batches:
- Calculate how many experiments per batch were lower than the previous best
- Compute the average of these improvements

### Task E: Batch Diversity Analysis
For non-Sobol batches:
- Calculate diversity using Euclidean distance between parameters
- Identify most and least diverse batches

## Implementation Details

- Uses synthetic objective function `measure_erosion()` from `utils.py`
- Implements proper error handling and validation
- Provides comprehensive logging
- Ensures reproducibility through seed setting

## Project Structure
```
.
├── qSOBO_assignment.py    # Main optimization implementation
├── utils.py              # Utility functions and measurements
├── requirements.txt      # Project dependencies
└── README.md            # Project documentation
```

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the optimization:
```bash
python qSOBO_assignment.py
```

## Notes
- First 3 batches use Sobol sampling
- Subsequent batches use Bayesian optimization
- All parameters are validated before optimization
- Device stress constraint is enforced throughout optimization