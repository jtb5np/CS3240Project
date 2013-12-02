import string
import datetime

__author__ = 'wil'


class LogEntry:

    def __init__(self, defaultActor = 'Admin', defaultInfo = 'Unspecified'):

        self.info = defaultInfo
        self.actor = defaultActor
        self.timeStamp = str(datetime.datetime.now())


    def setInfo(self, newInfo):

        self.info = newInfo

    def getInfo(self):

        return self.info

    def setActor(self, newActor):

        self.Actor = newActor

    def getActor(self):

        return self.actor

    def getTimeStamp(self):

        return self.timeStamp

    def setTimeStamp(self):

        self.timeStamp = str(datetime.now())

    def printLogEntry(self):

        out = self.getActor() + ' : ' + self.getTimeStamp() + ' - ' + (self.getInfo())
        return out







