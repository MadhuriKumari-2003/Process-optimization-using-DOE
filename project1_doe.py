# -------------------------------
# IMPORT LIBRARIES
# -------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# STEP 1: CREATE DOE TABLE (2^3 FACTORIAL)
# -------------------------------
data = pd.DataFrame({
    'Temperature': [300,300,300,300,400,400,400,400],
    'Pressure':    [1,1,3,3,1,1,3,3],
    'Time':        [10,20,10,20,10,20,10,20]
})

# -------------------------------
# STEP 2: GENERATE THICKNESS (SIMULATION)
# -------------------------------
np.random.seed(42)  # for reproducibility

noise = np.random.normal(0, 2, len(data))

data['Thickness'] = (
    0.2 * data['Temperature'] +
    5 * data['Pressure'] +
    2 * data['Time'] +
    noise
)

# -------------------------------
# STEP 3: DEFINE SPEC LIMITS
# -------------------------------
LSL = 95
USL = 105

# -------------------------------
# STEP 4: CHECK IF IN SPEC
# -------------------------------
data['In_Spec'] = data['Thickness'].between(LSL, USL)

# -------------------------------
# STEP 5: CALCULATE YIELD
# -------------------------------
yield_percent = data['In_Spec'].mean() * 100

# -------------------------------
# STEP 6: CALCULATE Cp & Cpk
# -------------------------------
mean = data['Thickness'].mean()
std = data['Thickness'].std()

Cp = (USL - LSL) / (6 * std)
Cpk = min((USL - mean)/(3*std), (mean - LSL)/(3*std))

# -------------------------------
# STEP 7: DISPLAY RESULTS
# -------------------------------
print("DOE Data:\n", data)
print("\nYield (%):", round(yield_percent, 2))
print("Cp:", round(Cp, 2))
print("Cpk:", round(Cpk, 2))

# -------------------------------
# STEP 8: VISUALIZATION
# -------------------------------
plt.figure()
plt.scatter(range(len(data)), data['Thickness'])
plt.axhline(LSL, linestyle='--')
plt.axhline(USL, linestyle='--')
plt.title("Thickness Distribution")
plt.xlabel("Experiment Run")
plt.ylabel("Thickness (nm)")
plt.show()

# -------------------------------
# STEP 9: OPTIMIZATION (FIND BEST COMBINATION)
# -------------------------------
best = data[data['In_Spec'] == True]
print("\nBest Parameter Settings:\n", best)