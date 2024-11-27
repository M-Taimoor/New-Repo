import pandas as pd
import matplotlib.pyplot as plt

# Load user engagement data
data = pd.read_csv("user_engagement_data.csv")

# Filter data for users with 3D Touch devices
users_with_3d_touch = data[data["device_has_3d_touch"] == True]

# Calculate average session duration for users with 3D Touch
avg_session_duration_3d_touch = users_with_3d_touch["session_duration"].mean()

# Filter data for users without 3D Touch devices
users_without_3d_touch = data[data["device_has_3d_touch"] == False]

# Calculate average session duration for users without 3D Touch
avg_session_duration_no_3d_touch = users_without_3d_touch["session_duration"].mean()

# Create a bar chart to compare average session duration
plt.figure(figsize=(10, 6))
plt.bar(
    ["With 3D Touch", "Without 3D Touch"],
    [avg_session_duration_3d_touch, avg_session_duration_no_3d_touch],
    color=["blue", "orange"],
)
plt.title("Average Session Duration Comparison")
plt.xlabel("User Group")
plt.ylabel("Average Session Duration (seconds)")
plt.show()