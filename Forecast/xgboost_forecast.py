import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import xgboost as xgb
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error, mean_absolute_error

#LSTM

field = 'cpu'
path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/choose_model_data/{}.csv'.format(field)
# %%
series = pd.read_csv(path.format(str(0).zfill(5)), header=0, index_col=0)
for i in range(1, 2):
    df2 = pd.read_csv(path.format(str(i).zfill(5)), header=0, index_col=0)
    series = pd.concat([series, df2])

series.index = pd.to_datetime(series.index, errors='coerce')
color_pal = ["#F8766D", "#D39200", "#93AA00", "#00BA38", "#00C19F", "#00B9E3", "#619CFF", "#DB72FB"]
# _ = series.plot(figsize=(15, 5), color=color_pal[0], title='Arrival Rate')
# plt.show()

# %%
split_date = '1970-01-01 17:30:00'
data_train = series.loc[series.index <= split_date].copy()
data_test = series.loc[series.index > split_date].copy()

ax = series.plot(figsize=(15, 5), color=color_pal[0])
series.loc[series.index <= split_date].plot(ax=ax, figsize=(15, 5), color=color_pal[1])
plt.show()


# %%
def create_features(df, label=None):
    """
    Creates time series features from datetime index
    """
    df['date'] = df.index
    df['minute'] = df['date'].dt.minute
    df['hour'] = df['date'].dt.hour
    df['dayofweek'] = df['date'].dt.dayofweek
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear

    X = df[['minute', 'hour', 'dayofweek', 'quarter', 'month', 'year',
            'dayofyear', 'dayofmonth', 'weekofyear']]
    if label:
        y = df[label]
        return X, y
    return X


# %%
X_train, y_train = create_features(data_train, label=field)
X_test, y_test = create_features(data_test, label=field)

# print(X_train)
# print(y_test)

# %%
reg = xgb.XGBRegressor(n_estimators=1000)
reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        early_stopping_rounds=200,
        verbose=True)
print('train done')

# %%
_ = plot_importance(reg, height=0.9)
plt.show()

# %%
data_test['forecast'] = reg.predict(X_test)
data_all = pd.concat([data_test, data_train], sort=False)

_ = data_all[[field, 'forecast']].plot(figsize=(15, 5))
plt.show()
_ = data_all[[field, 'forecast']].loc[data_all.index > split_date].plot(figsize=(15, 5))
plt.show()


# %%
def mean_absolute_percentage_error(y_true, y_pred):
    """Calculates MAPE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# %%
def standard_deviation(y_true, y_pred):
    """Calculates MAPE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


# %%
print(mean_absolute_percentage_error(y_true=data_test[field],
                                     y_pred=data_test['forecast']))
