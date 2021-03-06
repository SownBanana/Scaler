import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

ROUND = 120
CUT = ROUND
path = './data/wc_day{}_{}.csv'
cols = ['time', 'datetime', 'request', 'bytes']
df = pd.DataFrame()

for day in range(46, 50):
    for part in range(1, 10):
        try:
            df2 = pd.read_csv(path.format(day, part), names=cols, header=None)
            df = pd.concat([df, df2])
        except FileNotFoundError:
            break
# print(df)
df.index = pd.to_datetime(df['time'])

ax = df['request'].iloc[:CUT].plot(label="fit")
# plt.show()

# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(df['arrival_rq'].diff().dropna(), lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(df['arrival_rq'].diff().dropna(), lags=40, ax=ax2)
# plt.show()

# model:
# (0,0,1)(0,1,2,12)
# (1,0,2)(0,1,2,12)
# (2,0,2)(0,1,11,12)v
# (11,0,11)(11,1,11,12)
model = sm.tsa.statespace.SARIMAX(endog=df['request'], order=(2, 0, 2), seasonal_order=(0, 1, 11, 12), trend='c',
                                  enforce_invertibility=False)
results = model.fit()
print(results.summary())

# df['fit'] = results.fittedvalues
# df['fit'].iloc[CUT:].plot()
# plt.show()

forecast = results.get_forecast(steps=ROUND)
# f_ci = forecast.conf_int()

# print('======================>')
# print(forecast.predicted_mean)
# print(forecast.predicted_mean)
# print('======================>')

# ax.fill_between(f_ci.index,
#                 f_ci.iloc[:, 0],
#                 f_ci.iloc[:, 1], color='g', alpha=.5)
ax.set_xlabel('time')
ax.set_ylabel('cpu')

for day in range(50, 60):
    for part in range(1, 10):
        try:
            df2 = pd.read_csv(path.format(day, part), names=cols, header=None)
            df = pd.concat([df, df2])
        except FileNotFoundError:
            break
df['cpu'].iloc[(CUT-1):].plot(label="real")
forecast.predicted_mean.plot(ax=ax, label='forecast', color='g')

plt.legend()
plt.show()
