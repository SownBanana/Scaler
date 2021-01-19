import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

path = './PageViewsPerHourAll.csv'
save_path = './PageViewsPerHourAll_{}.csv'
cols = ['lo', 'date', 'hour', 'request']
chunksize = 10 ** 5
last_locate = 'aa'
new_data = {'date': [], 'hour': [], 'request': []}
for df in pd.read_csv(path, chunksize=chunksize, names=cols, header=None):
    for i in range(1, len(df)):
        locate = df[i:i + 1]['lo'].values[0]
        if locate != last_locate:
            new_df = pd.DataFrame(new_data)
            new_df.to_csv(save_path.format(last_locate))
            new_data.clear()
            new_data = {'date': [], 'hour': [], 'request': []}
            last_locate = locate
        else:
            new_data['date'].append(df[i:i + 1]['date'].values[0])
            new_data['hour'].append(df[i:i + 1]['hour'].values[0])
            new_data['request'].append(df[i:i + 1]['request'].values[0])
