import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

# Simulating a disaster alert function
def disaster_alert():
    return "Hurricane approaching! Please move to a safe location!"

# Simulating GPS location (In a real app, you would use actual GPS hardware or a library)
def get_user_location():
    # Simulating a fixed location (latitude, longitude)
    return (30.7333, 76.7794)  # Example coordinates (Chandigarh, India)

# Creating the user interface
class DisasterApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Title of the app
        self.title_label = Label(text="Disaster Management & Emergency Locator", font_size=24, size_hint=(1, 0.1))
        self.layout.add_widget(self.title_label)

        # Emergency Alert Button
        self.alert_button = Button(text="Get Emergency Alert", size_hint=(1, 0.2))
        self.alert_button.bind(on_press=self.show_alert)
        self.layout.add_widget(self.alert_button)

        # Location Button
        self.location_button = Button(text="Get My Location", size_hint=(1, 0.2))
        self.location_button.bind(on_press=self.show_location)
        self.layout.add_widget(self.location_button)

        # User Input for emergency message
        self.emergency_input = TextInput(hint_text="Enter your emergency message", size_hint=(1, 0.2), multiline=True)
        self.layout.add_widget(self.emergency_input)

        return self.layout

    # Function to show the disaster alert
    def show_alert(self, instance):
        alert_message = disaster_alert()
        alert_popup = Popup(title="Emergency Alert", content=Label(text=alert_message), size_hint=(None, None), size=(400, 400))
        alert_popup.open()

    # Function to show user's location
    def show_location(self, instance):
        location = get_user_location()
        location_popup = Popup(title="Your Location", content=Label(text=f"Your location: {location}"), size_hint=(None, None), size=(400, 400))
        location_popup.open()

    # Function to simulate periodic disaster alerts (e.g., push notifications in a real app)
    def periodic_alert(self, dt):
        alert_message = disaster_alert()
        print(f"ALERT: {alert_message}")

    def on_start(self):
        # Setting up periodic disaster alerts every 10 seconds
        Clock.schedule_interval(self.periodic_alert, 10)

# Running the app
if __name__ == '__main__':
    DisasterApp().run()
