import random
import math

from Event import Event


class Device:
    def __init__(self, number, speed):
        self.num = number
        self.request = None
        self.speed = speed
        self.time = 0

    def gen_time(self):
        self.time += (-1 / self.speed) * math.log(random.random())
        return Event(self.time, self.num, "Device")
