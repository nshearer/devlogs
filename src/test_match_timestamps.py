

from devlogs.monitors.timestamps import common_timestamp_formats

if __name__ == '__main__':

    for fmt in common_timestamp_formats():
        print(fmt.fmt)