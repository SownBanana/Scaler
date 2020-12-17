from Forecast.forecast import Sarima
import random as rd
import math
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

save_path = '/home/sownbanana/PycharmProjects/Scaler/Data/vmfc/VMforcast.csv'
# ngưỡng sử dụng cpu mỗi máy
upper_cpu = 0.7
lower_cpu = 0.2

upper_vm = math.inf
lower_vm = 1

MINUTE = 60
HOUR = 60 * MINUTE

# random số máy đầu tiên
VM = rd.randint(1, 10)
copy_VM = VM


# tính số máy ảo cần tăng (kết quả âm là giảm)
def get_scale(cpu_need):
    # fvm: forecast vm, lượng máy ảo cần dự đoán
    fvm = VM
    while True:
        # cpu_need: lượng cpu cần thiết dự đoán
        # tính cpu mỗi vm nếu dùng fvm máy ảo
        cpu_per_vm = cpu_need / fvm
        # nếu cpu sử dụng > ngưỡng trên, tăng máy ảo trong khoảng cho phép
        if cpu_per_vm >= upper_cpu and fvm <= upper_vm:
            fvm += 1
        # nếu cpu sử dụng < ngưỡng dưới, giảm số máy ảo
        elif cpu_per_vm <= lower_cpu and fvm >= lower_vm:
            fvm -= 1
        # nếu cpu sử dụng nằm trong khoản cho phép, return số máy ảo cần tăng
        else:
            print(cpu_per_vm)
            return fvm - VM


if __name__ == "__main__":
    # dự đoán từ 12h đến 13h
    first_time = datetime.strptime("1970-01-01 12:00:00", "%Y-%m-%d %H:%M:%S").timestamp()
    last_time = datetime.strptime("1970-01-01 12:30:00", "%Y-%m-%d %H:%M:%S").timestamp()
    cur_time = first_time

    # khởi tạo dự đoán với dữ liệu đầu vào là 4 tiếng đầu tiên
    forecast = Sarima([1])

    # dict dùng để hiển thị đồ thị
    data = {'time': [], 'vm_forecast': []}
    while cur_time < last_time:
        # lượng request đến dự đoán ở thời điểm cur_time
        ar = forecast.get_forecast(datetime.fromtimestamp(cur_time).strftime('%Y-%m-%d %H:%M:%S'))
        # lượng cpu trung bình mỗi request ở thời điểm cur_time
        cpu = forecast.get_estimate(datetime.fromtimestamp(cur_time).strftime('%Y-%m-%d %H:%M:%S'))

        # dự đoán lượng máy ảo cần scale
        forecastVM = get_scale(ar * cpu)

        if forecastVM > 0:
            print("scale up: {}".format(forecastVM))
        elif forecastVM < 0:
            print("scale down:{}".format(-forecastVM))

        #scale máy ảo
        VM = VM + forecastVM

        print("================")
        # lưu trữ
        data['time'].append(datetime.fromtimestamp(cur_time))
        data['vm_forecast'].append(VM)

        # lấy kết quả 1 phút tiếp theo
        cur_time += MINUTE

    df = pd.DataFrame(data)
    df.to_csv(save_path)
    df.index = pd.to_datetime(df['time'])
    df['vm_forecast'].plot(label='vm')
    plt.show()

    # df2 = pd.read_csv('/home/sownbanana/PycharmProjects/Scaler/Data/task_events/task_events_cpu/part-00001-of-00500.csv')
    # up = {'time':[], 'upper':[]}
    # for i in range (1, len(df2)):
    #     copy_VM = copy_VM + get_scale(df2[i:i+1]['cpu'].values[0]*df2[i:i+1]['arrival_rate'].values[0])
    #     up['upper'].append(copy_VM)
    #     up['time'].append(df2['time'].values[0])
    # df3 = pd.DataFrame(up)
    # df3.index = pd.to_datetime(df3['time'])
    # df3['upper'].plot()
    # plt.show()
