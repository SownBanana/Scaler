from datetime import datetime
import time

PROACTIVE_SCOPE = 120
REACTIVE_SCOPE = 60


class Event:
    import random as rd
    VM = rd.randint(1, 10)

    def __init__(self, scale_time, amount, event_type):
        self.type = type
        self.scale_time = scale_time
        self.amount = amount
        self.event_type = event_type

    def scale(self):
        Event.VM = Event.VM + self.amount


class EventManager:
    def __init__(self):
        self.proactive_cycle = []
        self.old_cycle = [[]]

    def scale(self, event):
        event.scale()

    def add_event(self, event):
        if event.type == 'reactive':
            old_cycle_index = -1
            pe = self.proactive_cycle[-1]
            if event.scale_time > pe.scale_time - PROACTIVE_SCOPE:
                return
            else:
                while True:
                    if len(self.old_cycle[old_cycle_index]) > 0:
                        pe = self.old_cycle[old_cycle_index][-1]
                        if event.scale_time > pe.scale_time - PROACTIVE_SCOPE:
                            return
                        else:
                            old_cycle_index -= 1
                    else:
                        break
            self.scale(event)
        else:
            self.proactive_cycle.append(event)

    def scale_proactive_cycle(self):
        pe = self.proactive_cycle[-1]
        if pe.scale_time == time.time():
            self.scale(pe)
            self.old_cycle = [[]]
        else:
            old_cycle_index = -1
            while True:
                if len(self.old_cycle[old_cycle_index]) > 0:
                    pe = self.old_cycle[old_cycle_index][-1]
                    if pe.scale_time == time.time():
                        self.scale(pe)
                        old_cycle_index -= 1
                        while len(self.old_cycle[old_cycle_index]) > 0:
                            self.old_cycle[old_cycle_index] = []
                            old_cycle_index -= 1
                    else:
                        old_cycle_index -= 1
                else:
                    break
