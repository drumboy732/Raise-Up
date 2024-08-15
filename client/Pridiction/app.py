import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load historical stock data (replace 'your_data.csv' with your dataset)
data = pd.read_csv('^NSEI.csv')
data = pd.read_csv('AAPL.csv')
data = pd.read_csv('ADBE.csv')
data = pd.read_csv('TATATECH.NS')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Define short-term and long-term moving averages
short_window = 40
long_window = 100

# Create signals
data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
data['Signal'] = 0.0
data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1.0, 0.0)

# Generate trading orders
data['Position'] = data['Signal'].diff()

# Plotting the strategy
plt.figure(figsize=(14, 8))
plt.plot(data['Close'], label='Stock Price', linewidth=2)
plt.plot(data['Short_MA'], label=f'Short {short_window} Days MA', linewidth=2)
plt.plot(data['Long_MA'], label=f'Long {long_window} Days MA', linewidth=2)

# Plot buy signals
plt.plot(data[data['Position'] == 1].index,
         data['Short_MA'][data['Position'] == 1],
         '^', markersize=10, color='g', label='Buy Signal')

# Plot sell signals
plt.plot(data[data['Position'] == -1].index,
         data['Short_MA'][data['Position'] == -1],
         'v', markersize=10, color='r', label='Sell Signal')

plt.title('Stock Market Simulator - Moving Average Crossover Strategy')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()