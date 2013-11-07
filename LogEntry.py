import string
import datetime

__author__ = 'wil'


class LogEntry:

    def __init__(self, defaultType = 'generalEntry', defaultInfo = 'Unspecified', defaultActor = 'System'):

        self.type = defaultType
        self.info = defaultInfo
        self.actor = defaultActor
        self.timeStamp = str(datetime.datetime.now())


    def setType(self, newType):

        self.type = newType

    def getType(self):

        return self.type

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

        out = self.getActor() + ' : ' + self.getTimeStamp() + ' - ' + self.getType() + ' (' + self.getInfo() + ') '
        print out







