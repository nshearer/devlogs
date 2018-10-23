import os

from .SourceMonitorThread import SourceMonitorThread


class LogTailMonitor(SourceMonitorThread):
    '''Monitor a traditional log file by watching it for new lines'''

    MAX_BYTES = 4096

    def __init__(self, path, target_queue, name=None, sleep_sec=1, encoding='utf8'):

        self.__path = path
        self.__encoding = encoding

        if name is None:
            name = os.path.basename(path)

        super().__init__(name=name, target_queue=target_queue, sleep_sec=sleep_sec)

        self.__last_bytes = None
        self.__last_pos = None


    def get_new_chars(self):
        '''
        Check source to see if there are any new bytes to read

        :return: yield new chars (forever)
        '''

        if os.path.exists(self.__path):

            # Check to see if file shrunk
            if self.__last_pos is not None:
                if os.path.getsize(self.__path) <= self.__last_pos:
                    self.__last_pos = None
                    self.__last_bytes = None

            # If last bytes present, see if they're still there
            if self.__last_bytes is not None and self.__last_pos is not None:
                with open(self.__path, 'rt') as fh:
                    fh.seek(self.__last_pos - len(self.__last_bytes))
                    if fh.read(self.MAX_BYTES) != self.__last_bytes:
                        self.__last_pos = None
                        self.__last_bytes = None

            # Determine where to start
            if self.__last_bytes is None or self.__last_pos is None:
                pos = 0
            else:
                pos = self.__last_pos

            # Read new bytes
            with open(self.__path, 'rt') as fh:
                fh.seek(pos)
                new_data = fh.read(self.MAX_BYTES)

            if not new_data:
                return None

            # Save state for next call
            self.__last_pos = pos + len(new_data)
            self.__last_bytes = new_data

            # # Decode and return (optionally stripping up to 3 chars off tail to help decode)
            # first_decode_e = None
            # for i in (0, 1, 2, 3):
            #     if i > 0:
            #         self.__last_pos -= 1
            #         self.__last_bytes = self.__last_bytes[:-1]
            #     if len(self.__last_bytes) > 0:
            #         try:
            #             return new_data.decode(self.__encoding)
            #         except Exception as e:
            #             if first_decode_e is None:
            #                 first_decode_e = e
            #
            # if first_decode_e:
            #     raise first_decode_e
            # else:
            #     raise Exception("Can we get to here?")

            return new_data





