import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


ar_path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events_processed/part-{}-of-00500.csv'
cpu_path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events_cpu/part-{}-of-00500.csv'
df = pd.read_csv(ar_path.format(str(0).zfill(5)))
for i in range(1, 10):
    df2 = pd.read_csv(ar_path.format(str(i).zfill(5)))
    df = pd.concat([df, df2])
# print(df)
df.index = pd.to_datetime(df['time'])
ax = df['arrival_rq'].plot(label="arrival")
plt.show()

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df['arrival_rq'].diff().dropna(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df['arrival_rq'].diff().dropna(), lags=40, ax=ax2)
plt.show()