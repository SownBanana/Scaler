import pandas as pd
from datetime import datetime

MINUTE = 60000000
HOUR = 60*MINUTE
EVAL = 2*MINUTE
# EVAL = 900000000
path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events/part-{}-of-00500.csv'
save_path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events_processed/part-{}-of-00500.csv'
new_data = {'time': [], 'arrival_rate': []}
time = EVAL
eval_count = 0
for no in range(0, 10):
    df = pd.read_csv(path.format(str(no).zfill(5)), header = None)
    # print(df)
    df.index = pd.to_timedelta(df[0], 'us')
    # time = pd.to_timedelta(EVAL, 'us')
    ar_sum = 0
    for i in range(1, len(df)):
        if df[i:i+1][0].values[0] > time:
            new_data['time'].append(datetime.fromtimestamp(time/1000000))
            new_data['arrival_rate'].append(ar_sum)
            time += EVAL
            ar_sum = 0
        if df[i:i+1][5].values[0] == 1:
            ar_sum += 1
        if time >= HOUR*(eval_count+1):
            new_df = pd.DataFrame(new_data)
            print(new_df)
            new_df.to_csv(save_path.format(str(eval_count).zfill(5)))
            eval_count += 1
            new_data.clear()
            new_data = {'time': [], 'arrival_rate': []}
# df.index=pd.to_datetime(df['Date'])
# df['Sales'].plot()
# plt.show()
