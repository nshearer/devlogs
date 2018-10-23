import os
from textwrap import dedent
import yaml


class DevlogConfig:
    '''Config file for server'''

    TEMPLATE = dedent("""\
        ---
        logs:
         - path: /var/log/syslog
         - cmd:  systemctl status ssh
           type: command
        commands:
         - name:     Build
           title:    Build Test Server
           working:  /vagrant/devlog
           commands:
            - title: Run tests
              cmd:   run_tests.sh
            - title: Collect Statics
              cmd:   python manage.py collectstatic
        """)


    def __init__(self, path):
        '''Config file directs devlog server on what to present'''

        if not os.path.exists(path):
            raise KeyError("%s does not exist" % (self.__path))

        self.__data = None
        self._load(path)


    def _load(self, path):
        with open(path, 'r') as fh:
            self.__data = yaml.load(fh)


class NullDevlogConfig(DevlogConfig):

    def __init__(self):
        self.__data = dict()

