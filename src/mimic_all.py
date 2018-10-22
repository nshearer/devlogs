import os
import sys
import subprocess
from time import sleep

MIMIC = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mimic.py')
TESTFILES = r"G:\Projects\sbc-signup\testfiles"

PROCS=list()

def mimic_file(path):
    src = os.path.join(TESTFILES, 'source', path)
    dst = os.path.join(TESTFILES, 'test', path)

    if os.path.exists(dst):
        os.unlink(dst)

    PROCS.append(subprocess.Popen((sys.executable, MIMIC, src, dst)))


FILES_TO_MIMIC = (
    r'letsencrypt\letsencrypt.log',
    r'alternatives.log',
    r'auth.log',
    r'cloud-init-output.log',
    r'cloud-init.log',
    r'dpkg.log',
    r'kern.log',
    r'syslog',
    r'ufw.log',
    r'apt\history.log',
    r'apt\term.log',
    r'letsencrypt\letsencrypt.log',
    r'nginx\access.log',
    r'nginx\error.log',
    r'postgresql\postgresql-10-main.log',
    r'unattended-upgrades\unattended-upgrades-dpkg.log',
    r'unattended-upgrades\unattended-upgrades.log',
)


if __name__ == '__main__':

    for path in FILES_TO_MIMIC:
        mimic_file(path)

    for proc in PROCS:
        sleep(1)
        proc.wait()
