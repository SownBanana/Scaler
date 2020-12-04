import pandas as pd
import numpy as np
from datetime import datetime

MINUTE = 60000000
HOUR = 60 * MINUTE

RECORD_PER_FILE = 100000

path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_usage/part-{}-of-00500.csv.gz'
save_path = '/home/sownbanana/PycharmProjects/Scaler/Data/task_usage/getdata/part-{}-of-00500.csv'
new_data = {'start_time': [], 'end_time': [], 'duration': [], 'job_id': [], 'task_index': [],
            'cpu_rate': [], 'cpu_usage': [], 'ram_usage': []}
eval_count = 0
for no in range(0, 5):
    df = pd.read_csv(path.format(str(no).zfill(5)), header=None)
    df.index = pd.to_timedelta(df[0], 'us')
    record_count = 0
    # lưu dữ liệu mỗi khoảng thời gian time
    for i in range(1, len(df)):
        start_time = df[i:i + 1][0].values[0]
        end_time = df[i:i + 1][1].values[0]
        duration = end_time - start_time

        # unit CPU-core seconds / second normalized (divide for largest capacity)
        cpu_rate = df[i:i + 1][5].values[0]
        cpu_usage = cpu_rate*(duration/1000000)

        # bytes normalized
        ram_usage =df[i:i + 1][6].values[0]

        new_data['start_time'].append(start_time)
        new_data['end_time'].append(end_time)
        new_data['duration'].append(duration)
        new_data['job_id'].append(df[i:i + 1][2].values[0])
        new_data['task_index'].append(df[i:i + 1][3].values[0])
        new_data['cpu_rate'].append(cpu_rate)
        new_data['cpu_usage'].append(cpu_usage)
        new_data['ram_usage'].append(df[i:i + 1][6].values[0])

        record_count += 1

        if record_count >= RECORD_PER_FILE:
            new_df = pd.DataFrame(new_data)
            print(eval_count)
            new_df.to_csv(save_path.format(str(eval_count).zfill(5)))
            eval_count += 1
            new_data.clear()
            new_data = {'start_time': [], 'end_time': [], 'duration': [], 'job_id': [], 'task_index': [],
                        'cpu_rate': [], 'cpu_usage': [], 'ram_usage': []}
            record_count = 0
