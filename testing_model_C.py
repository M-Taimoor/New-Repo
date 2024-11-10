from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

# Load and preprocess data
data = pd.read_csv('transaction_data.csv')
# Preprocessing steps would be implemented here

# Feature Engineering
# This would include code to create new features

# Split the data
X = data.drop('is_fraud', axis=1)
y = data['is_fraud']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Function to handle real-time transactions
def handle_transaction(transaction_data):
    # Preprocess and feature engineer the transaction data
    # Predict fraud
    is_fraudulent = model.predict([transaction_data])
    if is_fraudulent:
        # Trigger alert
        trigger_alert(transaction_data)

def trigger_alert(transaction_data):
    # Pause transaction
    # Notify customer
    # Escalate to fraud team
    pass

# Note: The actual implementation would include more details, such as 
# connecting to a live data stream, real-time prediction, and integration
# with notification and alerting systems.