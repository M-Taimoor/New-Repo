# Crop Simulation DSL
class CropSimulation:
    def __init__(self, crop_name, growth_rate):
        self.crop_name = crop_name
        self.growth_rate = growth_rate  # Growth rate per day (in cm)
        self.soil_type = None
        self.weather_conditions = None
        self.irrigation_level = None
        self.days = 0

    def set_soil(self, soil_type):
        """Set soil type: 'sandy', 'clay', 'loamy'."""
        self.soil_type = soil_type
        print(f"Selected soil type: {soil_type}")

    def set_weather(self, weather_conditions):
        """Set weather: 'sunny', 'rainy', 'dry'."""
        self.weather_conditions = weather_conditions
        print(f"Weather conditions: {weather_conditions}")

    def set_irrigation(self, irrigation_level):
        """Set irrigation level: 'low', 'medium', 'high'."""
        self.irrigation_level = irrigation_level
        print(f"Irrigation level: {irrigation_level}")

    def simulate_growth(self, days):
        """Simulate crop growth over a number of days."""
        self.days = days

        # Adjust growth rate based on soil type
        soil_modifier = {'sandy': 0.8, 'clay': 0.9, 'loamy': 1.0}.get(self.soil_type, 1.0)

        # Adjust growth rate based on weather conditions
        weather_modifier = {'sunny': 1.2, 'rainy': 1.0, 'dry': 0.7}.get(self.weather_conditions, 1.0)

        # Adjust growth rate based on irrigation level
        irrigation_modifier = {'low': 0.6, 'medium': 1.0, 'high': 1.3}.get(self.irrigation_level, 1.0)

        # Calculate total growth
        total_growth = self.growth_rate * soil_modifier * weather_modifier * irrigation_modifier * days

        print(f"Simulating growth for {days} days...")
        print(f"Total growth for {self.crop_name}: {total_growth:.2f} cm")

# Example Usage of the DSL
if __name__ == "__main__":
    # Create a simulation for wheat
    wheat_simulation = CropSimulation("Wheat", growth_rate=2.5)  # Growth rate in cm/day

    # Configure the scenario
    wheat_simulation.set_soil("loamy")
    wheat_simulation.set_weather("rainy")
    wheat_simulation.set_irrigation("high")

    # Simulate growth over 30 days
    wheat_simulation.simulate_growth(30)
