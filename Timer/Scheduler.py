from Timer.Timer import *


class Scheduler:
    def __init__(self, duration, callback):
        self.work_duration = duration
        self.store_work_duration = self.work_duration
        self.elapsed_time = 0
        self.callback = callback

    def update(self):
        self.elapsed_time += Timer().delta()
        if self.elapsed_time >= self.work_duration:
            self.elapsed_time -= self.work_duration
            if self.callback:
                self.callback()
