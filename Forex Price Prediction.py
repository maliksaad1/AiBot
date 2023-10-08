import pandas as pd
import pandas_ta as ta


df = pd.read_csv('GBPUSD.csv')


def calculate_ema(df, column_name='close', window=12):
    df['EMA'] = df[column_name].ewm(span=window, adjust=False).mean()
    return df

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

df = calculate_ema(df)
df = calculate_rsi(df)


print(df.head(40))



from sklearn.model_selection import train_test_split

train_data, test_data = train_test_split(df, test_size=0.1 , random_state = 20)


X_train = train_data.drop(labels=['close','Date','volume','RSI','EMA'], axis=1)

y_train = train_data['close']


X_test = test_data.drop(labels=['close', 'Date','volume','RSI','EMA'], axis=1)


y_test = test_data['close']


from sklearn.neighbors import KNeighborsRegressor

model = KNeighborsRegressor(n_neighbors=5)  

model.fit(X_train, y_train)  



y_test_pred = model.predict(X_test)


train_accuracy = model.score(X_train, y_train)
print("Accuracy of train data predictions:", train_accuracy)


test_accuracy = model.score(X_test, y_test)
print("Accuracy of test data predictions:", test_accuracy)
