import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load app usage data from CSV file
data = pd.read_csv('app_usage_data.csv')

# Filter data for users with 3D Touch devices
data_3d_touch = data[data['device_has_3d_touch'] == True]

# Filter data for users without 3D Touch devices
data_no_3d_touch = data[data['device_has_3d_touch'] == False]

# Calculate average session duration for users with 3D Touch
avg_session_duration_3d_touch = data_3d_touch['session_duration'].mean()

# Calculate average session duration for users without 3D Touch
avg_session_duration_no_3d_touch = data_no_3d_touch['session_duration'].mean()

# Print results
print(f"Average session duration for users with 3D Touch: {avg_session_duration_3d_touch:.2f} seconds")
print(f"Average session duration for users without 3D Touch: {avg_session_duration_no_3d_touch:.2f} seconds")

# Create bar chart comparing average session duration
labels = ['With 3D Touch', 'Without 3D Touch']
values = [avg_session_duration_3d_touch, avg_session_duration_no_3d_touch]

plt.bar(labels, values)
plt.xlabel('User Group')
plt.ylabel('Average Session Duration (seconds)')
plt.title('Impact of 3D Touch on User Engagement')
plt.show()