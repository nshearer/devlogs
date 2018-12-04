import os
import logging
from threading import RLock, Thread
from tempfile import TemporaryDirectory, gettempdir
from queue import Queue, Empty
import subprocess
from datetime import datetime

from .SourceMonitorThread import SourceMonitorThread


class CommandStateError(Exception): pass


class CommandMonitor(SourceMonitorThread):
    '''A command that the user can execute through the web interface'''

    MAX_BYTES = 1024 * 1024

    READY = 'ready'
    RUNNING = 'running'
    FINISHED = 'finished'
    ERROR = 'error'


    def __init__(self, monitor_id, name, working_dir=None):

        self.__log = logging.getLogger(__name__)

        self.__name = name
        self.__command_working_dir = working_dir
        if self.__command_working_dir is None:
            self.__command_working_dir = gettempdir() # /tmp
        self.__steps = list()

        self.__lock = RLock()
        self.__state = self.READY

        self.__command_thread = None
        self.__command_output = Queue()

        super().__init__(monitor_id=monitor_id, name=self.__name, sleep_sec=1)


    def _assert_state(self, *states):
        with self.__lock:
            if self.__state not in states:
                raise CommandStateError("Can't call in this state (%s not in %s)" % (
                    self.__state, ', '.join(states)))


    @property
    def source_spec(self):
        '''What to display to the user on what this is monitoring'''
        return "%s Command" % (self.name)


    def add_step(self, name, commands):
        '''
        Add a step to be executed when this command is requested by the user

        :param name: Name of the step
        :param commands: Shell commands to run to execute the step
        '''
        self.__steps.append((name, commands))


    def start_command(self):
        '''
        Start the command
        '''
        with self.__lock:

            self._assert_state(self.READY, self.ERROR, self.FINISHED)
            self.__command_thread = Thread(target=self._run_all_steps)
            self.__command_thread.start()
            self.__state = self.RUNNING


    def _run_all_steps(self):

        # Output Execution Header
        header = "Executing command at " + str(datetime.now())
        self.__command_output.put('='*len(header) + "\n")
        self.__command_output.put(header + "\n")
        self.__command_output.put('='*len(header) + "\n")

        # Prep for execution
        step_stack = self.__steps[:]
        tempdir = TemporaryDirectory()
        script_path = None

        for i, step in enumerate(step_stack):

            # Get next command
            name, commands = step

            # Output step header
            self.__command_output.put("""\

                ========== Step %d of %d: %s ========== 
                """ % (i + 1, len(step_stack), name))

            # Prep shell script to execute
            args = None
            if os.name == 'nt':
                script_path = os.path.join(tempdir.name, 'step.cmd')
                with open(script_path, 'wt') as fh:
                    fh.write("\n".join([c.rstrip() for c in commands.split("\n")]) + "\n")
                args = (script_path, )
            elif os.name == 'posix':
                script_path = os.path.join(tempdir.name, 'step.sh')
                with open(script_path, 'wt') as fh:
                    fh.write("\n".join([c.rstrip() for c in commands.split("\n")]) + "\n")
                args = ('bash', script_path)
            else:
                raise Exception("Don't know how to execute on " + os.name)

            # Start execution of the commands for this step
            process = subprocess.Popen(
                args = args,
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
                cwd = self.__command_working_dir)

            # TODO: Currently unable to iterate over output as it comes out.
            process.wait()

            # Monitor output until complete
            self.__command_output.put(process.stdout.read())

            # Show step return code
            self.__command_output.put("Step %s completed with exit code %d\n" % (
                name, process.returncode))

            # Check for error
            if process.returncode != 0:
                self.__command_output.put("Aborting execution due to error\n")
                with self.__lock:
                    self.__state = self.ERROR
                    os.unlink(script_path)
                    tempdir.cleanup()
                return

        # Cleanup
        self.__command_output.put("\nAll steps Finished\n")
        if script_path is not None and os.path.exists(script_path):
            os.unlink(script_path)
        tempdir.cleanup()
        with self.__lock:
            self.__state = self.FINISHED


    def get_new_chars(self):
        '''
        Check source to see if there are any new bytes to read

        :return: Any new data from the command output
        '''
        try:
            return self.__command_output.get(block=False)
        except Empty:
            return None


    def handle_new_chars(self, chars):
        return super().handle_new_chars(chars)












