from threading import Thread
from dateparser.search import search_dates
from time import sleep

class LogLine:
    '''Encapsulate a line from a log file'''

    def __init__(self, txt, source_name):
        self.__txt = txt
        self.__source = source_name
        self.linenum = None
        self.ts = None

    @property
    def txt(self):
        return self.__txt

    @property
    def source_name(self):
        return self.__source

    def __str__(self):
        return self.txt

    def __repr__(self):
        return "LogLine"


class SourceMonitorThread(Thread):
    '''
    A thread that monitors a log file for new log activity

        +------+       +-------------------------------+
        |     \|       | get_new_chars()               |
        |Source+------->  * Check source for new chars |
        |      |       |  * decode bytes -> chars      |
        +------+       |  * detect file trunc          |
                       +--+----------------------------+
                          |
                          |new chars
                          |
                       +--v----------------------------+
                       | handle_new_chars()            |
                       |  * convert char stream to     |
                       |    lines                      |
                       |  * detect duplicate lines?    |
                       +--+----------------------------+
                          |
                          |new lines
                          |
                       +--v----------------------------+
                       | new_line()                    |
                       |  * Detect Dates               |
                       |  * Add metadata               |
                       +-------------------------------+

    '''

    def __init__(self, name, target_queue, sleep_sec=1):
        self.__name = name
        self.__target = target_queue
        self.__sleep_for = sleep_sec

        super().__init__(daemon=True, name=name)

        self.__new_char_buffer = ''


    def run(self):
        while True:
            new_data = self.get_new_chars()
            if new_data is not None:
                for line in self.handle_new_chars(new_data):
                    self.handle_new_line(line)
            sleep(self.__sleep_for)


    def get_new_chars(self):
        '''
        Check source to see if there are any new bytes to read

        :return: yield new chars (forever)
        '''
        raise NotImplementedError()
        if False:
            yield None


    def handle_new_chars(self, chars):
        '''
        New characters read from monitored log source

        Called repeatedly, and should buffer characters not returned yet.

        Base implementation acts like readline from incoming char stream.

        :param chars: Alread decoded characters
        :return:
            Generate LogLine
            Any new, full lines detected from the character stream (in order)
        '''
        lines = (self.__new_char_buffer + chars).split("\n")
        for line in lines[:-1]:
            if len(line) > 0:
                yield LogLine(line, self.__name)

        if lines[-1].endswith("\n"):
            yield LogLine(lines[-1], self.__name)
            self.__new_char_buffer = ''
        else:
            self.__new_char_buffer = lines[-1]



    def handle_new_line(self, line):
        '''
        Handle new line detect from the input

        1) Performs metadata extration like line number and date string

        :param line: LogLine
        '''

        # Look for timestamp
        detected = search_dates(line.txt, languages=['en'])
        if len(detected) > 0:
            line.ts = min(detected)

        # Dispatch
        self.__target.put(line)

