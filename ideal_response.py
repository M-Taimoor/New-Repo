import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Load and preprocess the transaction data
data = pd.read_csv('transaction_data.csv')

# Convert categorical columns to numeric using one-hot encoding
X = data.drop(columns=['is_fraud'])  # Assuming 'is_fraud' is the target column
X = pd.get_dummies(X, drop_first=True)  # Encode categorical variables
y = data['is_fraud']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the fraud detection model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Define a threshold for fraud probability (you can adjust this as needed)
threshold = 0.5

# Function to predict and respond to potential fraud cases
def detect_fraud(transaction):
    # Predict if the transaction is fraudulent
    fraud_probability = model.predict_proba([transaction])[0][1]
    
    # Trigger an alert if fraud probability is high
    if fraud_probability > threshold:
        trigger_alert(transaction)
        pause_transaction(transaction)
        notify_customer(transaction)
        escalate_to_fraud_team(transaction)

# Implement the alert trigger, pause, notification, and escalation functions
def trigger_alert(transaction):
    print("Alert: Potential fraud detected!")

def pause_transaction(transaction):
    print("Transaction paused for review.")

def notify_customer(transaction):
    print("Customer notified about the suspicious transaction.")

def escalate_to_fraud_team(transaction):
    print("Escalated to fraud response team.")

# Example usage with a single transaction from the test set
# (Assuming transaction data is structured similarly to your feature set)
sample_transaction = X_test.iloc[0]
detect_fraud(sample_transaction)
