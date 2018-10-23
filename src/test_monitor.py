import os
from queue import Queue

from devlogs.monitors.LogTailMonitor import LogTailMonitor

if __name__ == '__main__':

    q = Queue()

    p = os.path.join(os.path.dirname(__file__), '..', 'testfiles', 'test', 'syslog')
    t = LogTailMonitor(p, target_queue=q)
    t.start()

    while True:
        line = q.get()
        print(">> " + str(line))
