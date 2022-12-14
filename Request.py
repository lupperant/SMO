class Request:
    def __init__(self, sourceNumber, requestNumber, genTime, refuseTime, deviceTime, releaseTime):
        self.sourceNumber = sourceNumber
        self.requestNumber = requestNumber
        self.genTime = genTime
        self.refuseTime = refuseTime
        self.deviceTime = deviceTime
        self.releaseTime = releaseTime
