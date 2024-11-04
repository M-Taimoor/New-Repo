import random
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Thresholds for model deployment
thresholds = {
    'accuracy': 85,
    'cost_limit': 50,
    'latency_limit': 0.5,
    'user_satisfaction': 80
}

class ModelDeploymentException(Exception):
    """Custom exception for model deployment errors."""
    pass

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

def can_deploy(model: Model) -> bool:
    """Aggregate all checks to determine if the model should be deployed."""
    try:
        if not check_accuracy(model):
            raise ModelDeploymentException('Model accuracy does not meet the minimum threshold.')
        if estimate_deployment_cost() > thresholds['cost_limit']:
            raise ModelDeploymentException('Deployment cost exceeds the reasonable limit.')
        if not check_latency(model):
            raise ModelDeploymentException('Model latency is above the acceptable limit.')
        if not check_user_satisfaction(model):
            raise ModelDeploymentException('User satisfaction does not meet the required threshold.')
        logging.info('Model meets all criteria for deployment.')
        return True
    except ModelDeploymentException as e:
        logging.error(f'Deployment aborted: {e}')
        return False
    except KeyError as e:
        logging.error(f'Missing configuration for {e}')
        raise

# Create an instance of the Model class
model_instance = Model()

# Test deployment decision
deployment_decision = can_deploy(model_instance)
print(f'Model Accuracy: {model_instance.get_accuracy()}%')
print(f'Model Latency: {model_instance.get_latency():.2f} seconds')
print(f'Model User Satisfaction: {model_instance.get_user_satisfaction()}%')
print(f'Deployment Decision: {"Approved" if deployment_decision else "Rejected"}')