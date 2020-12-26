import time


class _Timer:
    _instance = None

    def __init__(self):
        self.before_time = time.time()
        self.current_time = time.time()

    def initialized(self):
        self.before_time = time.time()

    def update(self):
        self.current_time = time.time()

    def delta(self):
        return self.current_time - self.before_time

    def reset(self):
        self.before_time = self.current_time


def Timer():
    if _Timer._instance is None:
        _Timer._instance = _Timer()
    return _Timer._instance
