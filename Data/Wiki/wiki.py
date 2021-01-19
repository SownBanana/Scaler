import os
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

path = './PageViewsPerHourAll_{}.csv'
chunksize = 10 ** 6
path_with_locate = path.format('br')
for df in pd.read_csv(path_with_locate, chunksize=chunksize):
    print(df)
    df['datetime'] = df['date'] + ":" + df['hour'].astype(str)
    df.plot(x='datetime', y='request')
plt.show()
