import random
import logging
from typing import Optional

# Configure logging for production
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thresholds for model deployment
thresholds = {
    'accuracy': 85,
    'cost_limit': 50,
    'latency_limit': 0.5,
    'user_satisfaction': 80
}

class Model:
    """A mock Model class to simulate real model metrics."""
    def __init__(self):
        self.accuracy = random.randint(70, 100)
        self.latency = random.uniform(0.1, 1.0)
        self.user_satisfaction = random.randint(70, 100)

    def get_accuracy(self) -> int:
        return self.accuracy

    def get_latency(self) -> float:
        return self.latency

    def get_user_satisfaction(self) -> int:
        return self.user_satisfaction

def estimate_deployment_cost() -> float:
    """Mock function to estimate deployment cost."""
    return random.uniform(10, 100)

def check_accuracy(model: Model) -> bool:
    """Check if model accuracy meets the minimum threshold."""
    return model.get_accuracy() >= thresholds['accuracy']

def check_latency(model: Model) -> bool:
    """Check if model latency is below the set limit."""
    return model.get_latency() < thresholds['latency_limit']

def check_user_satisfaction(model: Model) -> bool:
    """Check if user satisfaction exceeds the threshold."""
    return model.get_user_satisfaction() > thresholds['user_satisfaction']

def can_deploy(model: Optional[Model] = None) -> bool:
    """Aggregate all checks to determine if the model should be deployed."""
    try:
        if model is None:
            raise ValueError("No model provided for deployment check.")
        if not check_accuracy(model):
            logging.info('Model accuracy does not meet the minimum threshold.')
            return False
        if estimate_deployment_cost() > thresholds['cost_limit']:
            logging.info('Deployment cost exceeds the reasonable limit.')
            return False
        if not check_latency(model):
            logging.info('Model latency is above the acceptable limit.')
            return False
        if not check_user_satisfaction(model):
            logging.info('User satisfaction does not meet the required threshold.')
            return False
        logging.info('Model meets all criteria for deployment.')
        return True
    except (ValueError, KeyError) as e:
        logging.error(f'Deployment check failed: {e}')
        return False

# Create an instance of the Model class
model_instance = Model()

# Test deployment decision
deployment_decision = can_deploy(model_instance)
print(f'Model Accuracy: {model_instance.get_accuracy()}%')
print(f'Model Latency: {model_instance.get_latency():.2f} seconds')
print(f'Model User Satisfaction: {model_instance.get_user_satisfaction()}%')
print(f'Deployment Decision: {"Approved" if deployment_decision else "Rejected"}')