import heapq
import random
import math
import numpy as np

from Event import Event
from Request import Request


class Source:
    def __init__(self, number, a, b, numRequest):
        self.num = number
        self.numRequest = numRequest
        self.time = 0
        self.a = a
        self.b = b

    def gen_time(self):
        self.time += random.uniform(self.a, self.b)
        return Event(self.time, self.num, "Source", self.numRequest)
