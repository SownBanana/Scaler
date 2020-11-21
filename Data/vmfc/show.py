import matplotlib.pyplot as plt
import pandas as pd

path = '/home/sownbanana/PycharmProjects/Scaler/Data/vmfc/VMforcast.csv'
df = pd.read_csv(path)
df.index = pd.to_datetime(df['time'])
df['vm_forecast'].plot()
plt.show()
