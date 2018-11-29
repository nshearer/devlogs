import sys
import re

# Change the version of the project

if __name__ == '__main__':

    # Parse args
    try:
        version, = sys.argv[1:]
    except:
        print("Must specify version number")
        sys.exit(1)

    # Edit setup.py

    # version = '0.0.3', # version string
    pat = re.compile(r"version\s+=\s+'([0-9.]+)'\s*,\s*#\s*version\s*string.*")
    try:
        with open('setup.py', 'rt') as fh:
            lines = list(fh.readlines())
        for i, line in enumerate(lines):
            m = pat.search(line)
            if m:
                lines[i] = lines[i].replace(m.group(1), version)
        with open('setup.py', 'wt') as fh:
            fh.writelines(lines)
    except Exception as e:
        print("ERROR: " + str(e))
        sys.exit(2)

    print("Finished")




