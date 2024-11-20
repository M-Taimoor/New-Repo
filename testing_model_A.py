class CropSimulation:
    """Class representing crop simulation."""

    MODIFIERS = {
        'soil': {
            'sandy': 0.8,
            'clay': 0.9,
            'loamy': 1.0
        },
        'weather': {
            'sunny': 1.2,
            'rainy': 1.0,
            'dry': 0.7
        },
        'irrigation': {
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
            'soil': None,
            'weather': None,
            'irrigation': None
        }
        self.days = 0

    def set_parameter(self, parameter, value):
        """Set a parameter: 'soil', 'weather', or 'irrigation'."""
        if parameter in self.MODIFIERS and value in self.MODIFIERS[parameter]:
            self.parameters[parameter] = value
            print(f"Selected {parameter}: {value}")
        else:
            raise ValueError(f"Invalid {parameter}. Must be one of {list(self.MODIFIERS[parameter].keys())}.")

    def simulate_growth(self, days):
        """Simulate crop growth over a number of days."""
        if not isinstance(days, int) or days <= 0:
            raise ValueError("Number of days must be a positive integer.")

        self.days = days

        # Adjust growth rate based on parameters
        total_modifier = 1.0
        for parameter, value in self.parameters.items():
            total_modifier *= self.MODIFIERS[parameter].get(value, 1.0)

        # Calculate total growth
        total_growth = self.growth_rate * total_modifier * days

        print(f"Simulating growth for {days} days...")
        print(f"Total growth for {self.crop_name}: {total_growth:.2f} cm")

    def get_parameters(self):
        """Get the current parameter values."""
        return self.parameters


# Example Usage of the DSL
if __name__ == "__main__":
    # Create a simulation for wheat
    wheat_simulation = CropSimulation("Wheat", growth_rate=2.5)  # Growth rate in cm/day

    # Show available parameters
    print("Available parameters:")
    for parameter, values in CropSimulation.MODIFIERS.items():
        print(f"{parameter}: {list(values.keys())}")

    # Set parameters based on user input
    soil = input("Enter soil type (sandy, clay, loamy): ")
    weather = input("Enter weather conditions (sunny, rainy, dry): ")
    irrigation = input("Enter irrigation level (low, medium, high): ")

    # Set parameters
    wheat_simulation.set_parameter('soil', soil)
    wheat_simulation.set_parameter('weather', weather)
    wheat_simulation.set_parameter('irrigation', irrigation)

    # Simulate growth over 30 days
    wheat_simulation.simulate_growth(30)