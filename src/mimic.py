import os
import sys
from time import sleep

if __name__ == '__main__':

    try:
        srcpath, dstpath = sys.argv[1:]
    except ValueError:
        print("ERROR: usage source dest")
        sys.exit(1)

    with open(srcpath, 'rt') as fh:
        source = list(fh.readlines())

        if len(source) == 0:
            print("%s is empty" % (srcpath))
            sys.exit(2)

    i = 0

    if not os.path.exists(os.path.dirname(dstpath)):
        os.makedirs(os.path.dirname(dstpath))

    with open(dstpath, 'wt') as fh:
        while True:
            fh.write(source[i])
            print(source[i].rstrip())
            fh.flush()
            sleep(7)
            i = (i + 1) % (len(source))

