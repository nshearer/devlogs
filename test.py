#!/usr/bin/python3
'''Test the server'''

import os
import sys
import requests
from tempfile import TemporaryDirectory
import subprocess
from textwrap import dedent
from threading import Thread
from time import sleep

from devlogs import main

TEST_PORT = 48080

TEST_FILE_CONTENTS = dedent("""\
    Line 1
    Line 2
    Line 3
    """)


class TestFailed(Exception): pass


if __name__ == '__main__':

    failed = False
    project = os.path.abspath(os.path.dirname(__file__))
    server = None

    with TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)

        try:
            # Create file to monitor
            logfile = os.path.join(tmpdir, 'test.log')
            with open(logfile, 'wt') as fh:
                fh.write(TEST_FILE_CONTENTS)

            # Do init
            config_file = os.path.join(tmpdir, 'devlogs.yml')
            main(('--path', config_file, 'init'))
            if not os.path.exists(config_file):
                raise TestFailed("init command didn't create devlog.yml")

            # Write test config
            with open(config_file, 'wt') as fh:
                fh.write(dedent("""\
                    ---
                    logs:
                      - path: test.log
                    """))

            # Start Test Server
            server = subprocess.Popen((sys.executable, os.path.join(project, 'run_devlogs.py'), 'run', '--port', str(TEST_PORT)))

            # Wait for server to startup
            print("Waiting for server startup")
            sleep(10)

            # See if we can retrieve pages
            endpoints = [url.strip() for url in """\
                
                index.html
                log.html?monitor_id=0
                status
                nextlines?monitor_id=all&last_line_id=-1&how_many=all
                """.rstrip().split("\n")]
            for endpoint in endpoints:
                url = 'http://127.0.0.1:%d/%s' % (TEST_PORT, endpoint)

                print('')
                print("="*len(url))
                print(url)
                print("="*len(url))

                r = requests.get(url)

                print(r.content.decode('utf-8'))

                if not r.ok:
                    raise TestFailed("Failed to get %s: %s" % (url, r.content))


        except TestFailed as e:
            print(str(e))
            failed = True

        # cleanup
        if server is not None:
            server.kill()
            server.wait()
        for path in (logfile, config_file):
            if os.path.exists(path):
                os.unlink(path)
        os.chdir(project)

    if failed:
        sys.exit(2)

    print("\nFinished")
