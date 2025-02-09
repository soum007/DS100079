# -*- coding: utf-8 -*-
"""Weatherdatavizz.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qEBelIIhbdwSQPf34Lp2mklva-O0xG7k
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the weather data
weather = pd.read_csv('weather_data.csv', index_col="Date_Time")

# Display the first few rows of the dataset
print("Dataset Overview:")
print(weather.head())

# Basic statistics of the dataset
print("\nDataset Statistics:")
print(weather.describe())

# Check for missing values
print("\nMissing Values:")
print(weather.isnull().sum())

# Fill missing values (if any) using forward fill
weather.fillna(method='ffill', inplace=True)

# Visualizations
sns.set(style="whitegrid", palette="muted")

# Identify anomalies: Extreme temperatures
mean_temp = weather['Temperature_C'].mean()
std_temp = weather['Temperature_C'].std()
threshold = 2  # Define anomaly threshold in terms of standard deviations

# Scatter plot: Temperature vs Humidity
plt.figure(figsize=(8, 6))
sns.scatterplot(data=weather, x='Humidity_pct', y='Temperature_C', alpha=0.6, color='red')
plt.title('Temperature vs. Humidity')
plt.xlabel('Humidity (%)')
plt.ylabel('Temperature (°C)')
plt.show()

# Boxplot: Wind Speed Distribution
plt.figure(figsize=(8, 6))
sns.boxplot(data=weather, y='Wind_Speed_kmh', color='green')
plt.title('Wind Speed Distribution')
plt.ylabel('Wind Speed (km/h)')
plt.show()

# Pairplot to visualize relationships between variables
sns.pairplot(weather, diag_kind="kde")
plt.suptitle('Pairplot of Weather Data', y=1.02)
plt.show()

# Model Training: Predict Temperature using other features
X = weather[['Humidity_pct', 'Precipitation_mm', 'Wind_Speed_kmh']]
y = weather['Temperature_C']

# Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Model Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("\nModel Performance:")
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared: {r2:.2f}")

# Example future values for prediction
future_humidity = 60  # Example value in percentage
future_precipitation = 0  # Example value in mm (e.g., no precipitation)
future_wind_speed = 15  # Example value in km/h

# Combine features into a single input array
future_input = [[future_humidity, future_precipitation, future_wind_speed]]

# Predict the future temperature
future_temp = model.predict(future_input)
print(f"\nPredicted Future Temperature: {future_temp[0]:.2f} °C")

# Plot actual vs predicted values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.7, color='purple')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.title('Actual vs Predicted Temperature')
plt.xlabel('Actual Temperature (°C)')
plt.ylabel('Predicted Temperature (°C)')
plt.show()

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Select features for clustering
features = weather[['Temperature_C', 'Humidity_pct', 'Wind_Speed_kmh', 'Precipitation_mm']]

# Normalize features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Apply K-means clustering
kmeans = KMeans(n_clusters=4, random_state=42)
weather['Cluster'] = kmeans.fit_predict(scaled_features)

# Visualize clusters
plt.figure(figsize=(8, 6))
sns.scatterplot(data=weather, x='Temperature_C', y='Humidity_pct', hue='Cluster', palette='Set1')
plt.title('Weather Clusters')
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.show()