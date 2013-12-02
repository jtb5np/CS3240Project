from Server import LogEntry

__author__ = 'wil'


class Log:


    def __init__(self, history = []):
        self.log = history
        self.log_file = open("log.txt", "a")

    def addEntry(self, entry):

        self.log.append(entry)
        self.update_log_file(entry)

    def printLatestEntry(self):

        print self.log[len(self.log)-1]

    def printLog(self):

        for x in self.log:

            if isinstance(x, LogEntry):
                x.printLogEntry()

    def update_log_file(self,entry):
        with open("log.txt", "a") as myFile:
            myFile.write(str(entry.printLogEntry()))

    def get_actor_activity(self,actor):

        results = []

        for x in self.log[0,len[self.log]]:

            if self.log[x].getActor is actor:

                results.append(self.log[x])

        for x in results[0,len(results)]:

            print results[x]


    def get_time_activity(self,startTime, endTime):

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