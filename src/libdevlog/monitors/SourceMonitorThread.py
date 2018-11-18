from threading import Thread
#from dateparser.search import search_dates
from time import sleep
from threading import RLock, Condition, Lock

class LogLine:
    '''Encapsulate a line from a log file'''

    def __init__(self, txt, source_name, line_id):
        self.__txt = txt
        self.__source = source_name
        self.linenum = None
        self.ts = None
        self.line_id = line_id

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


class NoNewLines(Exception): pass


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

    def __init__(self, monitor_id, name, sleep_sec=1):
        self.__monitor_id = monitor_id
        self.__name = name
        self.__sleep_for = sleep_sec

        self.monitor_lock = RLock()
        self.__log_lines = list()
        self.__next_line_id = 0

        super().__init__(daemon=True, name=name)

        self.__new_char_buffer = ''

        self.__new_line_available = Condition(lock=self.monitor_lock)


    @property
    def monitor_id(self):
        with self.monitor_lock:
            return self.__monitor_id


    @property
    def source_spec(self):
        '''What to display to the user on what this is monitoring'''
        return self.__name


    def run(self):
        while True:
            new_data = self.get_new_chars()
            if new_data is not None:
                for line in self.handle_new_chars(new_data):
                    self.handle_new_line(line)
            else:
                sleep(self.__sleep_for)


    # -- Log capture methods --

    def get_new_chars(self):
        '''
        Check source to see if there are any new bytes to read

        :return: yield new chars (forever)
        '''
        raise NotImplementedError()
        if False:
            yield None


    def _get_next_line_id(self):
        with self.monitor_lock:
            self.__next_line_id += 1
            return self.__next_line_id - 1


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
                yield LogLine(line, self.__name, self._get_next_line_id())

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
        # detected = search_dates(line.txt, languages=['en'])
        # if len(detected) > 0:
        #     line.ts = min(detected)

        # TODO: Detect duplicate lines here?

        # Save line
        with self.monitor_lock:
            line.linenum = len(self.__log_lines)
            self.__log_lines.append(line)

            # Tell anyone waiting with wait_new_line_available() there's new data
            #
            # Since condition uses same lock, re-aquiring the lock might not
            # be needed.  Shouldn't hurt though?
            with self.__new_line_available:
                self.__new_line_available.notify_all()


    # -- Log line query methods --

    def all_lines(self):
        with self.monitor_lock:
            for line in self.__log_lines:
                yield line


    def last_lines(self, num=None):
        if num is None:
            with self.monitor_lock:
                for i in range(len(self.__log_lines)-1, 0-1, -1):
                    yield self.__log_lines[i]
        else:
            for i, line in enumerate(self.last_lines()):
                if i < num:
                    yield line
                else:
                    return


    @property
    def last_line(self):
        with self.monitor_lock:
            if len(self.__log_lines) > 0:
                return self.__log_lines[-1]
            else:
                return None


    def wait_new_line_available(self, last_line_num, timeout_sec):
        '''
        Hold until either a new line has been detected in the log, or a timeout occurs

        Don't need to hold lock to call this, as it will use the condition to wait until
        available.

        :param last_line_num:
            The last LogLine.line_id the caller knows of.
            Will only return lines greater than this.
        :param timeout_sec:
            The number of seconds to wait before timing out
        :return:
            List of new lines
        :raises NoNewLines:
            If the timeout occurs
        '''

        def _new_line_available():
            last = self.last_line
            if last is not None:
                if last_line_num is None or last.line_id > last_line_num:
                    return True
            return False


        with self.__new_line_available:

            # Wait for new line to be available
            while not _new_line_available():
                if not self.__new_line_available.wait(timeout=timeout_sec):
                    raise NoNewLines()

            # Collect all new lines
            lines = list()
            for line in self.last_lines():
                if last_line_num is None or line.line_id > last_line_num:
                    lines.append(line)
                else:
                    break

        return list(reversed(lines))



