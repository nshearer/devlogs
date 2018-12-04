import os
from textwrap import dedent
import yaml


class ConfigFileSyntaxError(Exception): pass


class DevlogConfigSection:
    '''A section of the config file'''
    def __init__(self, path, info, entry_name=None):
        self.__path = path
        self.__name = entry_name
        self.info = info
    def _syntax_error(self, msg):
        if self.__name is None:
            raise ConfigFileSyntaxError("Error in %s: %s" % (self.__path, msg))
        else:
            raise ConfigFileSyntaxError("Error in %s record in %s: %s" % (
                self.__name, self.__path, msg))
    @property
    def entry_name(self):
        return self.__name


class DevlogLogConfig(DevlogConfigSection):
    '''Entry in logs: in config file'''

    monitor_type = 'tail'

    @property
    def path(self):
        '''Path to monitor'''
        try:
            return self.info['path']
        except KeyError:
            self._syntax_error("Missing required path")


class DevlogCommandConfig(DevlogConfigSection):

    monitor_type = 'command'

    @property
    def name(self):
        try:
            return self.info['name']
        except KeyError:
            self._syntax_error("Missing required name")

    @property
    def working_dir(self):
        try:
            return self.info['working_dir']
        except KeyError:
            return None

    @property
    def steps(self):
        try:
            steps = list(self.info['steps'])
        except:
            self._syntax_error("Missing steps")

        for i, step in enumerate(steps):

            try:
                name = step['name']
            except:
                self._syntax_error("Step %d is missing a name" % (i+1))

            try:
                commands = step['commands']
            except:
                try:
                    commands = step['cmd']
                except:
                    self._syntax_error("Step %d is missing a commands block" % (i+1))


            yield {
                'name': name,
                'commands': commands
            }



class DevlogConfig:
    '''Config file for server'''

    TEMPLATE = dedent("""\
        ---
        logs:
         - path: /var/log/syslog
         - cmd:  systemctl status ssh
           type: command
        commands:
         - name:     Build Test Server
           working:  /vagrant/devlog
           steps:
            - name:  Run tests
              cmd:   run_tests.sh
            - name:  Collect Statics
              cmd:   python manage.py collectstatic
        """)


    def __init__(self, path):
        '''Config file directs devlog server on what to present'''

        if not os.path.exists(path):
            raise KeyError("%s does not exist" % (path))

        self.__data = None
        self.__path = path

        self._load(path)


    def _load(self, path):
        with open(path, 'r') as fh:
            self.__data = yaml.load(fh)


    def _syntax_error(self, msg):
        raise ConfigFileSyntaxError("Error in %s: %s" % (self.__path, msg))

    @property
    def monitors(self):
        '''
        List the monitored log files

        :return: DevlogLogConfigs
        '''

        # Add log files to monitor
        try:
            for info in self.__data['logs']:
                yield DevlogLogConfig(self.__path, info)
        except KeyError:
            self._syntax_error("Missing logs: section")

        # Add command monitors
        try:
            for info in self.__data['commands']:
                yield DevlogCommandConfig(self.__path, info)
        except KeyError:
            pass # no ['commands']


class NullDevlogConfig(DevlogConfig):

    def __init__(self):
        self.__data = dict()

    @property
    def monitors(self):
        if False:
            yield None
