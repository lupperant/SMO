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
        self.a = 1
        self.b = 10
        self.speed = 0.2
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
        self.events = sorted(self.events, key=lambda event: event.time)

    def iteration(self):
        event = self.events.pop()
        buffer = None
        if event.eventType == "Source":
            for i in it.chain(range(self.bufferIndex, self.bufferNum), range(0, self.bufferIndex)):
                if self.buffers[i].request is None:
                    self.buffers[i].request = Request(event.compNumber, event.reqNumber, event.time, -1, -1, - 1)
                    self.buffers[i].numSource = event.compNumber
                    self.buffers[i].numRequest = event.reqNumber
                    gen_time = self.sources[event.compNumber].gen_time()
                    self.sources[event.compNumber].numRequest += 1
                    self.events.append(gen_time)
                    self.events = sorted(self.events, key=attrgetter('time'))
                    self.bufferIndex = (i + 1) % self.bufferNum
                    buffer = not None
                    break
            if buffer is None:
                newReq = self.buffers[self.bufferIndex].request
                newReq.refuseTime = event.time
                self.requests.append(newReq)
                self.buffers[self.bufferIndex].request = Request(event.compNumber, event.reqNumber, event.time, -1, -1, - 1)
                self.buffers[self.bufferIndex].numSource = event.compNumber
                self.buffers[self.bufferIndex].numRequest = event.reqNumber
                gen_time = self.sources[event.compNumber].gen_time()
                self.sources[event.compNumber].numRequest += 1
                self.events.append(gen_time)
                self.requests.append(Request(event.compNumber, event.reqNumber, gen_time.time, -1, -1, -1))
                self.events = sorted(self.events, key=attrgetter('time'))
                self.bufferIndex = (self.bufferIndex + 1) % self.bufferNum
            for i in it.chain(range(self.deviceIndex, self.deviceNum), range(0, self.deviceIndex)):
                if self.devices[i].request is None:
                    num = self.buffers[0].numSource
                    buf_num = 0
                    for j in range(0, self.bufferNum):
                        if self.buffers[j].numSource < num:
                            num = self.buffers[j].numSource
                            buf_num = j
                    req = self.buffers[buf_num].request
                    if self.devices[i].num != event.compNumber:
                        self.buffers[buf_num].request = None
                        self.buffers[buf_num].numRequest = -1
                        self.buffers[buf_num].numSource = -1
                        gen_time = self.devices[i].gen_time()
                        self.events.append(gen_time)
                        req.releaseTime = gen_time.time
                        req.deviceTime = req.genTime
                        self.devices[i].request = req
                        self.requests.append(req)

        if event.eventType == "Device":
            for i in it.chain(range(self.deviceIndex, self.deviceNum), range(0, self.deviceIndex)):
                if self.devices[i].request is None:
                    num = self.buffers[0].numSource
                    buf_num = 0
                    for j in range(0, self.bufferNum):
                        if self.buffers[j].numSource < num:
                            num = self.buffers[j].numSource
                            buf_num = j
                    req = self.buffers[buf_num].request
                    if self.devices[i].num != event.compNumber:
                        self.buffers[buf_num].request = None
                        self.buffers[buf_num].numRequest = -1
                        self.buffers[buf_num].numSource = -1
                        gen_time = self.devices[i].gen_time()
                        self.events.append(gen_time)
                        req.releaseTime = gen_time.time
                        req.deviceTime = req.genTime
                        self.devices[i].request = req
                        self.requests.append(req)
                    else:
                        self.buffers[buf_num].request = None
                        self.buffers[buf_num].numRequest = -1
                        self.buffers[buf_num].numSource = -1
                        gen_time = self.devices[i].gen_time()
                        self.events.append(gen_time)
                        req.releaseTime = gen_time.time
                        req.deviceTime = event.time
                        self.devices[i].request = req
                        self.requests.append(req)

