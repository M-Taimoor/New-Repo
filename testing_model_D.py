class CropSimulation:
    """Class representing crop simulation."""

    MODIFIERS = {
        'soil_type': {
            'sandy': 0.8,
            'clay': 0.9,
            'loamy': 1.0
        },
        'weather_conditions': {
            'sunny': 1.2,
            'rainy': 1.0,
            'dry': 0.7
        },
        'irrigation_level': {
            'low': 0.6,
            'medium': 1.0,
            'high': 1.3
        }
    }

    def __init__(self, crop_name, growth_rate):
        """Initialize the CropSimulation instance."""
        self.crop_name = crop_name
        self.growth_rate = growth_rate  # Growth rate per day (in cm)
        self.parameters = {
            'soil_type': None,
            'weather_conditions': None,
            'irrigation_level': None
        }
        self.days = 0

    def set_parameter(self, parameter_name, parameter_value):
        """Set a parameter."""
        if parameter_name in self.MODIFIERS and parameter_value in self.MODIFIERS[parameter_name]:
            self.parameters[parameter_name] = parameter_value
            print(f"Set parameter: {parameter_name} = {parameter_value}")
        else:
            raise ValueError(f"Invalid parameter value: {parameter_value}")

    def simulate_growth(self, days):
        """Simulate crop growth over a number of days."""
        if not isinstance(days, int) or days <= 0:
            raise ValueError("Number of days must be a positive integer.")

        self.days = days

        # Adjust growth rate based on parameters
        total_growth = self.growth_rate
        for parameter_name, parameter_value in self.parameters.items():
            modifier = self.MODIFIERS[parameter_name].get(parameter_value, 1.0)
            total_growth *= modifier

        print(f"Simulating growth for {days} days...")
        print(f"Total growth for {self.crop_name}: {total_growth:.2f} cm")


# Example Usage of the DSL
if __name__ == "__main__":
    # Create a simulation for wheat
    wheat_simulation = CropSimulation("Wheat", growth_rate=2.5)  # Growth rate in cm/day

    # Configure the scenario
    wheat_simulation.set_parameter('soil_type', 'loamy')
    wheat_simulation.set_parameter('weather_conditions', 'rainy')
    wheat_simulation.set_parameter('irrigation_level', 'high')

    # Simulate growth over 30 days
    wheat_simulation.simulate_growth(30)