import pandas as pd
import numpy as np
from datetime import datetime

MINUTE = 60000000
HOUR = 60 * MINUTE

# lấy mẫu mỗi 1 phút
INTERVAL = MINUTE

path = '../task_events/part-{}-of-00500.csv.gz'
arrival_rate_path = './arrival_rate.csv'
cpu_path = './cpu.csv'
ar_data = {'time': [], 'arrival_rate': []}
cpu_data = {'time': [], 'cpu': []}
time = INTERVAL
eval_count = 0
series = pd.read_csv(path.format(str(0).zfill(5)), header=None)
for i in range(1, 3):
    df2 = pd.read_csv(path.format(str(i).zfill(5)), header=None)
    series = pd.concat([series, df2])

print(series)
series.index = pd.to_timedelta(series[0], 'us')
series[0] = datetime.fromtimestamp(series[0] / 1000000)

series = series.groupby(series[0].dt.minute).sum()
print(series)