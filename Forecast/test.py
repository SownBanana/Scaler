# import pandas as pd
# import statsmodels
# import statsmodels.api as sm
# import matplotlib.pyplot as plt
# import numpy as np
#
# df = pd.read_csv('/home/sownbanana/PycharmProjects/Scaler/Data/salesdata.csv')
# df.index = pd.to_datetime(df['Date'])
# df['Sales'].plot()
# plt.show()
#
# # model=sm.tsa.ARIMA(endog=df['Sales'],order=(0,1,6))
# # results=model.fit()
# # print(results.summary())
# #
# # results.resid.plot()
# # plt.show()
# # fig = plt.figure(figsize=(12,8))
# # ax1 = fig.add_subplot(211)
# # fig = sm.graphics.tsa.plot_acf(results.resid, lags=40, ax=ax1)
# # ax2 = fig.add_subplot(212)
# # fig = sm.graphics.tsa.plot_pacf(results.resid, lags=40, ax=ax2)
# # plt.show()
# #
# # forecast,std,conf=results.forecast(12)
# # plt.plot(forecast)
# # plt.show()
#
#
# # print(df['Sales'].diff(12))
# #%%
# np.random.seed(5967)
# noise=[np.random.normal(scale=500)]
#
# for i in range(len(df)-1):
#     noise.append(np.random.normal(scale=500)+noise[i]*(-0.85))
# df['Sales2']=df['Sales']+noise
# df['Sales2'].plot()
# plt.show()
#
# # print(df['Sales2'].diff().diff(12))
#
# model=sm.tsa.statespace.SARIMAX(endog=df['Sales2'],order=(1,1,0),seasonal_order=(0,1,1,12),trend='c',enforce_invertibility=False)
# results=model.fit()
# print(results.summary())
#
# results.resid.plot()
# plt.show()
#
# df['noise']=[noise[i]+0.85*noise[i-1] if i>0 else 0 for i in range(len(noise))]
# results.resid2.loc['2008-02-01':].plot(label='Regression Residuals')
# df['noise'].loc['2008-02-01':].plot(color='r',label='True Noise')
# plt.legend(loc=2)
# plt.show()
#
# model2=sm.tsa.statespace.SARIMAX(endog=df['Sales2'],order=(1,1,0),seasonal_order=(0,1,1,12),trend='c',enforce_invertibility=False)
# results2=model2.fit()
# print(results2.summary())


import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import numpy as np

df=pd.read_csv('/Data/salesdata.csv')

df.index=pd.to_datetime(df['Date'])
df['Sales'].plot()
plt.show()

# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(df['Sales'].diff().dropna(), lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(df['Sales'].diff().dropna(), lags=40, ax=ax2)
# plt.show()

#This model is shown but not run because it will return an error.
#model=sm.tsa.statespace.SARIMAX(endog=df['Sales'],order=(0,1,0),seasonal_order=(0,1,0,12),trend='c',enforce_invertibility=False)
#results=model.fit()
#print(results.summary())

#To show you why it will return an error use this code:
# print(df['Sales'].diff().diff(12))
#%%
np.random.seed(5967)
noise=[np.random.normal(scale=500)]

for i in range(len(df)-1):
    noise.append(np.random.normal(scale=500)+noise[i]*(-0.85))
df['Sales2']=df['Sales']+noise
df['Sales2'].plot()
plt.show()



# #%%
# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(df['Sales2'].diff().diff(12).dropna(), lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(df['Sales2'].diff().diff(12).dropna(), lags=40, ax=ax2)
# plt.show()

# model=sm.tsa.statespace.SARIMAX(endog=df['Sales2'],order=(1,1,0),seasonal_order=(0,1,0,12),trend='c',enforce_invertibility=False)
# results=model.fit()
# print(results.summary())
# #%%
# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(results.resid, lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(results.resid, lags=40, ax=ax2)
# plt.show()

# df['noise']=noise
# results.resid.loc['2008-02-01':].plot(label='Regression Residuals')
# df['noise'].loc['2008-02-01':].plot(color='r',label='True Noise')
# plt.legend(loc=2)
# plt.show()

#%%
model=sm.tsa.statespace.SARIMAX(endog=df['Sales2'],order=(1,1,0),seasonal_order=(0,1,1,12),trend='c',enforce_invertibility=False)
results=model.fit()
print(results.summary())

# fig = plt.figure(figsize=(12,8))
# ax1 = fig.add_subplot(211)
# fig = sm.graphics.tsa.plot_acf(results2.resid, lags=40, ax=ax1)
# ax2 = fig.add_subplot(212)
# fig = sm.graphics.tsa.plot_pacf(results2.resid, lags=40, ax=ax2)
# plt.show()
#
# df['noise']=[noise[i]+0.85*noise[i-1] if i>0 else 0 for i in range(len(noise))]
# results2.resid.loc['2008-02-01':].plot(label='Regression Residuals')
# df['noise'].loc['2008-02-01':].plot(color='r',label='True Noise')
# plt.legend(loc=2)
# plt.show()

# forecast=results.forecast(12)
# plt.plot(forecast)
# plt.show()

forecast=results.get_forecast(steps=50)
f_ci = forecast.conf_int()
# plt.plot(forecast2)
# plt.show()

ax=df['Sales2'].plot()

forecast.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(f_ci.index,
                f_ci.iloc[:, 0],
                f_ci.iloc[:, 1], color='g', alpha=.5)
ax.set_xlabel('Date')
ax.set_ylabel('Sale')
plt.legend()
plt.show()