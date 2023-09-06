import pandas as pd
import pandas_ta as ta

# Load your data from a CSV file
df = pd.read_csv('GBPUSD.csv')

# Define a function to calculate EMA
def calculate_ema(df, column_name='close', window=12):
    df['EMA'] = df[column_name].ewm(span=window, adjust=False).mean()
    return df

# Define a function to calculate RSI
def calculate_rsi(df, column_name='close', window=14):
    price_diff = df[column_name].diff(1)
    gain = price_diff.where(price_diff > 0, 0)
    loss = -price_diff.where(price_diff < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    relative_strength = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + relative_strength))

    df['RSI'] = rsi
    return df

# Calculate EMA and RSI
df = calculate_ema(df)
df = calculate_rsi(df)

# Display the DataFrame with added indicators
print(df.head(40))


#Splliting Data

from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(df, test_size=0.1 , random_state = 20)


# Fetching X_train and y_train
X_train = train_data.drop(labels=['close','Date','volume','RSI','EMA'], axis=1)

y_train = train_data['close']


# Fetching X_test and y_test
X_test = test_data.drop(labels=['close', 'Date','volume','RSI','EMA'], axis=1)


y_test = test_data['close']


from sklearn.neighbors import KNeighborsRegressor

# Create an instance of the KNeighborsRegressor
model = KNeighborsRegressor(n_neighbors=5)  # You can adjust the number of neighbors as needed

# Fit the model to your training data
model.fit(X_train, y_train)  # X_train is your feature data, y_train is your target data



#Predicting Values
y_test_pred = model.predict(X_test)


#Checking accuracy for Training data
train_accuracy = model.score(X_train, y_train)
print("Accuracy of train data predictions:", train_accuracy)

#Checking accuracy for Testing data
test_accuracy = model.score(X_test, y_test)
print("Accuracy of test data predictions:", test_accuracy)
