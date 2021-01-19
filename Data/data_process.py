import pandas as pd
import numpy as np
from datetime import datetime

MINUTE = 60000000
HOUR = 60 * MINUTE

# lấy mẫu mỗi 1 phút
INTERVAL = MINUTE

path = './task_events/task_events/part-{}-of-00500.csv.gz'
save_path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events_cpu/part-{}-of-00500.csv'
new_data = {'time': [], 'cpu': [], 'arrival_rate': []}
time = INTERVAL
eval_count = 0
for no in range(0, 20):
    df = pd.read_csv(path.format(str(no).zfill(5)), header=None)
    df.index = pd.to_timedelta(df[0], 'us')
    cpu = 0
    count = 0
    # lưu dữ liệu mỗi khoảng thời gian time
    for i in range(1, len(df)):
        # nếu đủ khoảng thời gian time, lưu vào new_data
        if df[i:i + 1][0].values[0] > time:

            # timestamp dữ liệu gốc có đơn vị microsecond
            new_data['time'].append(datetime.fromtimestamp(time / 1000000))

            # lưu lương request đến trong khoảng time
            new_data['arrival_rate'].append(count)
            if count == 0:
                new_data['cpu'].append(0)
            # lưu cpu trung bình sử dụng trong time
            else:
                new_data['cpu'].append(cpu / count)
            time += INTERVAL
            cpu = 0
            count = 0
        cpu_ar = df[i:i + 1][9].values[0]
        # cộng cpu sử dụng và lượng request nếu là request đến
        if df[i:i + 1][5].values[0] == 1 and type(cpu_ar) == np.float64:
            cpu += cpu_ar
            count += 1
        # elif df[i:i + 1][5].values[0] != 1 and type(cpu_ar) == float:
        #     cpu -= cpu_ar

        # nếu data đủ trong 2 giờ, lưu vào file mới task_events_cpu/part-{index}-of-00500.csv
        if time >= 2 * HOUR * (eval_count + 1):
            new_df = pd.DataFrame(new_data)
            print(new_df)
            new_df.to_csv(save_path.format(str(eval_count).zfill(5)))
            eval_count += 1
            new_data.clear()
            new_data = {'time': [], 'cpu': [], 'arrival_rate': []}

# df.index=pd.to_datetime(df['Date'])
# df['Sales'].plot()
# plt.show()
