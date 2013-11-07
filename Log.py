import LogEntry

__author__ = 'wil'


class Log:


    def __init__(self, history = []):

        self.log = history

    def addEntry(self, entry):

        self.log.append(entry)

    def printLatestEntry(self):

        print self.log[len(self.log)-1]

    def printLog(self):

        for x in self.log:

           if isinstance(x, LogEntry):
            x.printLogEntry()


    def getActivity(self,type):

        results = []

        for x in self.log[0,len[self.log]]:

            if self.log[x].getType is type:

                results.append(self.log[x])

        for x in results[0,len(results)]:

            print results[x]


    def getActivity(self,actor):

        results = []

        for x in self.log[0,len[self.log]]:

            if self.log[x].getActor is actor:

                results.append(self.log[x])

        for x in results[0,len(results)]:

            print results[x]


    def getActivity(self,startTime, endTime):

        results = []

        for x in self.log[0,len[self.log]]:

            if self.log[x].timeStamp :

                results.append(self.log[x])

        for x in results[0,len(results)]:

            print results[x]

def main():
        testLog = Log()
        testEntry = LogEntry()
        testLog.addEntry(testEntry)
        testLog.printLog()

if __name__ == '__main__':
    main()