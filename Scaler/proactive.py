import math
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from Forecast.forecast import Sarima
from Scaler.event_manager import Event, EventManager

upper_cpu = 0.7
lower_cpu = 0.2

upper_vm = math.inf
lower_vm = 1

MINUTE = 60
HOUR = 60 * MINUTE


class Proactive:
    def __init__(self, event_manager, VM):
        self.event_manager = event_manager
        self.VM = VM
    # tính số máy ảo cần tăng (kết quả âm là giảm)
    def get_scale(self,cpu_need):
        # fvm: forecast vm, lượng máy ảo cần dự đoán
        fvm = self.VM
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
                return fvm - self.VM

    def make_events(self, start_time, end_time):
        cur_time = start_time

        forecast = Sarima([1])

        # dict dùng để hiển thị đồ thị
        data = {'time': [], 'vm_forecast': []}
        while cur_time < end_time:
            # lượng request đến dự đoán ở thời điểm cur_time
            ar = forecast.get_forecast(datetime.fromtimestamp(cur_time).strftime('%Y-%m-%d %H:%M:%S'))
            # lượng cpu trung bình mỗi request ở thời điểm cur_time
            cpu = forecast.get_estimate(datetime.fromtimestamp(cur_time).strftime('%Y-%m-%d %H:%M:%S'))

            # dự đoán lượng máy ảo cần scale
            forecastVM = self.get_scale(ar * cpu)
            VM = VM + forecastVM

            if forecastVM > 0:
                print("scale up: {}".format(forecastVM))
            elif forecastVM < 0:
                print("scale down:{}".format(-forecastVM))

            event = Event(cur_time, forecastVM, 'proactive')

            self.event_manager.add_event(event)

            # lấy kết quả 1 phút tiếp theo
            cur_time += MINUTE
