import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Generate some sample data (using random data for demonstration)
np.random.seed(0)
data_size = 100
features = np.random.rand(data_size, 1)  # Example feature, e.g., mean RR intervals
labels = np.random.randint(0, 2, data_size)  # Binary labels (0 or 1)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train a simple RandomForest model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test the model (optional)
y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save the model to a .pkl file
joblib.dump(model, 'ecg_model.pkl')
