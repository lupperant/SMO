from Buffer import Buffer
from Device import Device
from Request import Request
from Source import Source
import itertools as it
from operator import attrgetter


class System:
    def __init__(self, sourceNum, deviceNum, bufferNum, a, b, speed):
        self.sourceNum = sourceNum
        self.deviceNum = deviceNum
        self.bufferNum = bufferNum
        self.a = a
        self.b = b
        self.speed = speed
        self.sources = [Source(i, self.a, self.b, -1) for i in range(self.sourceNum)]
        self.devices = [Device(i, self.speed) for i in range(self.deviceNum)]
        self.buffers = [Buffer(i, -1, -1) for i in range(self.bufferNum)]
        self.events = []
        self.requests = []
        self.bufferIndex = 0
        self.deviceIndex = 0

    def genSystem(self):
        for i in range(self.sourceNum):
            gen_time = self.sources[i].gen_time()
            self.sources[i].numRequest += 1
            self.events.append(gen_time)
            self.requests.append(Request(i, 1, gen_time.time, -1, -1, -1))
        self.events = sorted(self.events, key=lambda event: event.time)

    def iteration(self):
        event = self.events.pop()
        buffer = None
        if event.eventType == "Source":
            for i in it.chain(range(self.bufferIndex, self.bufferNum), range(0, self.bufferIndex)):
                if self.buffers[i].request is None:
                    self.buffers[i].request = not None
                    self.buffers[i].numSource = event.compNumber
                    self.buffers[i].numRequest = event.reqNumber
                    gen_time = self.sources[i].gen_time()
                    self.sources[i].numRequest += 1
                    self.events.append(gen_time)
                    self.requests.append(Request(event.compNumber, event.reqNumber, gen_time.time, -1, -1, -1))
                    self.events = sorted(self.events, key=lambda e: event.time)
                    self.bufferIndex = i + 1
                    buffer = not None
                    break
            if buffer is None:
                self.requests[self.bufferIndex].refuseTime = event.time
                gen_time = self.sources[i].gen_time()
                self.sources[i].numRequest += 1
                self.events.append(gen_time)
                self.requests.append(Request(event.compNumber, event.reqNumber, gen_time.time, -1, -1, -1))
                self.events = sorted(self.events, key=lambda e: e.time)
                self.bufferIndex += 1
            self.buffers = sorted(self.buffers, key=attrgetter('time'))

        if event.eventType == "Device":
            self.requests = sorted(self.requests, key=attrgetter('sourceNumber'))
            for i in it.chain(range(self.deviceIndex, self.deviceNum), range(0, self.deviceIndex)):
                if self.devices[i].request is None:


