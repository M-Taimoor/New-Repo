import pandas as pd
import matplotlib.pyplot as plt

# Load hypothetical user engagement data
data = {
    'UserID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'DeviceType': ['3D Touch', 'Non-3D Touch', '3D Touch', 'Non-3D Touch', '3D Touch', 'Non-3D Touch', '3D Touch', 'Non-3D Touch', '3D Touch', 'Non-3D Touch'],
    'SessionDuration': [120, 90, 150, 80, 110, 100, 140, 85, 130, 95],
    'ConversionRate': [0.8, 0.6, 0.9, 0.5, 0.7, 0.7, 0.8, 0.6, 0.8, 0.6]
}

df = pd.DataFrame(data)

# Calculate average session duration and conversion rate for each device type
avg_session_duration = df.groupby('DeviceType')['SessionDuration'].mean()
avg_conversion_rate = df.groupby('DeviceType')['ConversionRate'].mean()

# Create a bar chart to compare average session duration
plt.figure(figsize=(8, 6))
avg_session_duration.plot(kind='bar', color='skyblue')
plt.title('Average Session Duration by Device Type')
plt.xlabel('Device Type')
plt.ylabel('Average Session Duration (seconds)')
plt.xticks(rotation=0)
plt.show()

# Create a bar chart to compare average conversion rate
plt.figure(figsize=(8, 6))
avg_conversion_rate.plot(kind='bar', color='orange')
plt.title('Average Conversion Rate by Device Type')
plt.xlabel('Device Type')
plt.ylabel('Average Conversion Rate')
plt.xticks(rotation=0)
plt.show()