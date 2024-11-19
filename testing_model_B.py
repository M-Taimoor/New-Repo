import pandas as pd
import statsmodels.api as sm
from itertools import product
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample data: Variations of headers, images, and descriptions with corresponding conversions
raw_data = [
    ["Header A", "Image X", "Desc 1", 50, 500],
    ["Header A", "Image Y", "Desc 1", 65, 600],
    ["Header B", "Image X", "Desc 2", 80, 700],
    ["Header B", "Image Y", "Desc 2", 75, 750],
    ["Header C", "Image X", "Desc 3", 90, 800],
    ["Header C", "Image Y", "Desc 3", 85, 850],
]

# Convert to DataFrame
df = pd.DataFrame(raw_data, columns=["Header", "Image", "Description", "Conversions", "Visitors"])

# Convert all columns to numeric, coerce errors to NaN, then drop invalid rows
df[["Conversions", "Visitors"]] = df[["Conversions", "Visitors"]].apply(pd.to_numeric, errors='coerce')
df.dropna(inplace=True)

# Ensure that X and y are numeric
X = df[["Header", "Image", "Description"]].astype(str)
y = df["Conversions"] // df["Visitors"]  # Integer division

# Ensure that y contains no infinite or NaN values
X = X[~y.isna()]
y = y[~y.isna()]

# One-hot encode categorical variables
X_encoded = pd.get_dummies(X, drop_first=True)

# Fit OLS model
model = sm.OLS(y, sm.add_constant(X_encoded)).fit()

# Display the dataset and the model summary
print("Dataset for Multivariate Testing:")
print(df)
print("\nMultivariate Testing Results:")
print(model.summary())

# Best combination for maximum conversion rate
best_combination = X_encoded.iloc[model.predict(X_encoded).idxmax()].drop('const')
print("\nBest Combination for Maximum Conversion Rate:")
print(best_combination)