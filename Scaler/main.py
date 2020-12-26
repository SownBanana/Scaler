from Forecast.forecast import Sarima
from Scaler.event_manager import *
from Timer.Timer import *
from Timer.Scheduler import *
from Scaler.proactive import Proactive
import random as rd
import math
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

save_path = '/Data/vmfc/VMforcast.csv'
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

def make_reactive_event():
    return Event(0, 'reactive')

if __name__ == "__main__":
    Timer().initialized()
    event_manager = EventManager()
    proactive = Proactive(event_manager, VM)
    # dự đoán 30 phút
    proactive.make_events(time.time(), time.time() + 1800)
    Timer().delta()

    scale_proactive_task = Scheduler(240, event_manager.scale_proactive_cycle)
    scale_reactive_task = Scheduler(120, make_reactive_event)
    while True:
        scale_proactive_task.update()
        scale_reactive_task.update()


