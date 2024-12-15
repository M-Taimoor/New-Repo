import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Example data (Year vs CO2 emissions)
years = np.array([2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009])
emissions = np.array([2.5, 2.6, 2.8, 3.0, 3.1, 3.1, 3.2, 3.5, 3.7, 3.9])

# Define piecewise linear function
def piecewise_linear(x, x0, y0, k1, k2):
    """Piecewise linear function with two segments."""
    return np.piecewise(
        x,
        [x < x0, x >= x0],
        [lambda x: k1 * x + y0 - k1 * x0, lambda x: k2 * x + y0 - k2 * x0]
    )

# Initial guesses for parameters
x0_guess = 2005  # Initial guess for the joinpoint (year)
y0_guess = emissions[years == x0_guess][0]  # Emission at the joinpoint
k1_guess = 0.1  # Slope before the joinpoint
k2_guess = 0.2  # Slope after the joinpoint

# Fit the piecewise function
params, _ = curve_fit(piecewise_linear, years, emissions, p0=[x0_guess, y0_guess, k1_guess, k2_guess])

# Extract fitted parameters
x0, y0, k1, k2 = params

# Print joinpoint and slopes
print(f"Joinpoint (Year): {x0:.2f}")
print(f"Slope before joinpoint: {k1:.2f}")
print(f"Slope after joinpoint: {k2:.2f}")

# Generate data for the fitted curve
fitted_emissions = piecewise_linear(years, *params)

# Plot original data and the fitted curve
plt.scatter(years, emissions, label="Original Data", color="blue")
plt.plot(years, fitted_emissions, label="Fitted Joinpoint Regression", color="red")
plt.axvline(x=x0, color="green", linestyle="--", label=f"Joinpoint at {x0:.2f}")
plt.xlabel("Year")
plt.ylabel("CO2 Emissions")
plt.legend()
plt.title("Joinpoint Regression Example")
plt.show()
