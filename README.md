## 3. Batch Optimization: Optimizing Erosion Resistant Coating Parameters

Perform batch optimization to maximize the erosion resistance of a protective coating.

### Task Context

Atmospheric Plasma Spraying (APS) is a process for depositing protective coatings on
material substrates. Your team is interested in applying a metallic coating with a high
hardness to a cheap metal substrate using APS to improve its erosion resistance as
measured by mass loss under sand blasting. To test the performance of these coatings,
however, requires that they be sent to a laboratory with specialized testing equipment.
You estimate that it will take approximately four days to ship a sample to the other
lab and get it tested. With a budget of 30 experiments, this translates to 120 days of
transit time! In the interest of efficiency, you decide to pursue a batch optimization
approach where you will prepare and send samples in batches of three, which translates
to 40 days of total transit time.

The design space consists of a set of six operating parameters. Looking through some
historical APS data within your company, you define the following bounds on your
parameter design space.

| Parameter               | Historic Range   |
| ----------------------- | ---------------- |
| Primary Gas Flow Rate   | 30 - 80 [SLPM]   |
| Secondary Gas Flow Rate | 10 - 50 [SLPM]   |
| Gun Current             | 300 - 800 [A]    |
| Carrier Gas Flow Rate   | 2 - 10 [SLPM]    |
| Power Feed Rate         | 10 - 100 [g/min] |
| Spray Distance          | 50 - 150 [mm]    |

The manufacturer of your APS device defines a constraint on the operating conditions
of the device to extend its operational lifetime. As this APS device will be used
during the prodction stage of these coatings, you decide to apply this constraint to
avoid damaging it. The constraint is formulated as an equation relating the primary
gas flow rate, secondary gas flow rate and gun current.

```python
device_stress_index = primary_gas_flow_rate + secondary_gas_flow_rate + gun_current <= 750
```

Your task is to use Honegumi to develop an optimization script to help you identify a
set of parameters that minimize the material mass loss in the erosion trials. Your
experimental budget is limited to 30 experiments divided into batches of three. A
synthetic objective function has been provided that will serve as a proxy for real
experimental measurements.

### **TASK A:** Use Honegumi to set up and run the optimization problem.

In this problem you are expected to use [Honegumi](https://honegumi.readthedocs.io/en/latest/) to generate a code template for this problem which you will then modify to meet the problem criteria. For some specific examples of this check out the [tutorials](https://honegumi.readthedocs.io/en/latest/tutorials.html) page on the Honegumi website.

To complete this problem, you are given access to a synthetic objective function that will be used as a proxy for real experimental observations called `measure_erosion()`, which is stored in the `./utils.py` file. This function takes in six variables: `pg_rate`, `sg_rate`, `current`, `cg_rate`, `pf_rate`, `distance` and returns the measured mass loss value for the coating. These are the parameters you should specify when setting up your optimization problem.

### **TASK B:** Report the optimal parameters, associted erosion rate, and the stress_index.

Now that you have completed the optimization, assign the optimial parameters as a dictionary to a variable named `optimal_params` and the lowest erosion score as a float to a variable named `min_mass_loss`. Finally create a variable named `device_stress_index` and assign the stress index of the optimal solution to it.

### **TASK C:**  How many solutions have a stress index > 700

Calculate the number of solutions in the bottom 15% of trials that have a stress index greater than 700 and the number to a variable named `high_stress_count`.

### **TASK D:** On average, how many experiments per batch were lower than the previous best?

Iterate through each non_sobol batch and determine how many experiments in that batch
were lower than the lowest value found up to the previous batch. In other words how many points in a given batch would have set a new global minimum. Now Calculate the average of these values over all non_sobol batches and assign the result to a variable named `avg_lower`.

The `.groupby` method in `pandas` will be particularly helpful in calcualting batch-level statistics.

### **TASK E:** Which non-sobol batch was the most and least diverse in terms parameters?

The diversity of solutions can be measured by the euclidian distance between their
parameters. This can be computed with `np.linalg.norm(x1-x2)`. Calculate the *average* distance between all pairs of solutions within each non-sobol batch. The first non-sobol batch is batch 4. Assign the most and least diverse batch numbers to variables named `most_diverse` and `least_diverse`, respectively.