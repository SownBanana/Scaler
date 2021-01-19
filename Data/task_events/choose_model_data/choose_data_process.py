import pandas as pd
import numpy as np
from datetime import datetime

#%%
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
for no in range(0, 20):
    df = pd.read_csv(path.format(str(no).zfill(5)), header=None)
    df.index = pd.to_timedelta(df[0], 'us')
cpu = 0
count = 0
last_time = 0
# lưu dữ liệu mỗi khoảng thời gian time
print(48 * HOUR * (eval_count + 1))

#%%
for i in range(1, len(df)):
    # nếu đủ khoảng thời gian time, lưu vào new_data
    if df[i:i + 1][0].values[0] > time:

        # timestamp dữ liệu gốc có đơn vị microsecond
        ar_data['time'].append(datetime.fromtimestamp(time / 1000000))
        cpu_data['time'].append(datetime.fromtimestamp(time / 1000000))

        # lưu lương request đến trong khoảng time
        ar_data['arrival_rate'].append(count)
        if count == 0:
            cpu_data['cpu'].append(0)
        # lưu cpu trung bình sử dụng trong time
        else:
            cpu_data['cpu'].append(cpu / count)
        time += INTERVAL
        cpu = 0
        count = 0
    cpu_ar = df[i:i + 1][9].values[0]
    # cộng cpu sử dụng và lượng request nếu là request đến
    if df[i:i + 1][5].values[0] == 1 and type(cpu_ar) == np.float64:
        cpu += cpu_ar
        count += 1
    if last_time != time:
        print(time)
        last_time = time
    if time >= 48 * HOUR * (eval_count + 1):
        new_df = pd.DataFrame(cpu_data)
        new_df.to_csv(cpu_path, index=False)

        new_df = pd.DataFrame(ar_data)
        new_df.to_csv(arrival_rate_path, index=False)

        eval_count += 1
        ar_data.clear()
        cpu_data.clear()
        ar_data = {'time': [], 'arrival_rate': []}
        cpu_data = {'time': [], 'cpu': []}
        print("done")
        raise SystemExit(0)
