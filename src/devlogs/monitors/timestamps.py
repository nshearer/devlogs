from datetime import datetime
import re

from pytz import timezone


class DateFormat:
    def __init__(self, fmt, example):
        self.fmt = fmt
        self.example = example
        self.re_src = None
        self.parsestr = None
        self.shims = list()
    def __str__(self):
        return self.fmt
    def __repr__(self):
        return "DateFormat('%s', '%s')" % (self.fmt, self.example)



def split_format(fmt):
    '''
    Split up format into parts

    YYYY-MM-DD -> ('YYYY', '-', 'MM', '-', 'DD')
    '''
    parts = list()
    last_c = None
    for c in fmt:
        if last_c is None or last_c != c:
            parts.append(c)
        else:
            parts[-1] += c
        last_c = c
    return tuple(parts)


assert(split_format("YYYY-MM-DD") == ('YYYY', '-', 'MM', '-', 'DD'))


def shim_year(ts):
    '''Assume 1900 means current year'''
    if ts.year == 1900:
        return datetime(
            year=datetime.now().year,
            month=ts.month,
            day=ts.day,
            hour=ts.hour,
            minute=ts.minute,
            second=ts.second,
            microsecond=ts.microsecond,
            tzinfo=ts.tzinfo)
    return ts


def common_timestamp_formats():

    this_year = datetime.now().year

    formats = (
        # ref: https://help.sumologic.com/03Send-Data/Sources/04Reference-Information-for-Sources/Timestamps%2C-Time-Zones%2C-Time-Ranges%2C-and-Date-Formats
        # ("yyyy-MM-dd'T'HH:mm:ss*SSSZZZZ",    "2018-08-20'T'13:20:10*633+0000"),
        ("yyyy MMM dd HH:mm:ss.SSS zzz",     "2017 Mar 03 05:12:41.211 PDT",     datetime(2017, 3, 3, 5, 12, 41, 211, timezone('US/Pacific'))),
        # ("MMM dd HH:mm:ss ZZZZ yyyy",        "Jan 21 18:20:11 +0000 2017"),
        # ("dd/MMM/yyyy:HH:mm:ss ZZZZ",        "19/Apr/2017:06:36:15 -0700"),
        # ("MMM dd, yyyy hh:mm:ss a",          "Dec 2, 2017 2:39:58 AM"),
        # ("MMM dd yyyy HH:mm:ss",             "Jun 09 2018 15:28:14"),
        # ("MMM dd HH:mm:ss yyyy",             "Apr 20 00:00:35 2010"),
        # ("MMM dd HH:mm:ss ZZZZ",             "Sep 28 19:00:00 +0000"),
        ("MMM dd HH:mm:ss",                  "Mar 16 08:12:04",                   datetime(this_year, 3, 16, 8, 12, 4)),
        # ("yyyy-MM-dd'T'HH:mm:ssZZZZ",        "2017-10-14T22:11:20+0000"),
        # ("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'",     "2017-07-01T14:59:55.711'+0000'"),
        # ("yyyy-MM-dd HH:mm:ss ZZZZ",         "2017-08-19 12:17:55 -0400"),
        # ("yyyy-MM-dd HH:mm:ssZZZZ",          "2017-08-19 12:17:55-0400"),
        # ("yyyy-MM-dd HH:mm:ss,SSS",          "2017-06-26 02:31:29,573"),
        # ("yyyy/MM/dd*HH:mm:ss",              "2017/04/12*19:37:50"),
        # ("yyyy MMM dd HH:mm:ss.SSS*zzz",     "2018 Apr 13 22:08:13.211*PDT"),
        # ("yyyy MMM dd HH:mm:ss.SSS",         "2017 Mar 10 01:44:20.392"),
        # ("yyyy-MM-dd HH:mm:ss,SSSZZZZ",      "2017-03-10 14:30:12,655+0000"),
        # ("yyyy-MM-dd HH:mm:ss.SSS",          "2018-02-27 15:35:20.311"),
        # ("yyyy-MM-dd HH:mm:ss.SSSZZZZ",      "2017-03-12 13:11:34.222-0700"),
        # ("yyyy-MM-dd'T'HH:mm:ss.SSS",        "2017-07-22'T'16:28:55.444"),
        # ("yyyy-MM-dd'T'HH:mm:ss",            "2017-09-08'T'03:13:10"),
        # ("yyyy-MM-dd'T'HH:mm:ss'Z'",         "2017-03-12'T'17:56:22'-0700'"),
        # ("yyyy-MM-dd'T'HH:mm:ss.SSS",        "2017-11-22'T'10:10:15.455"),
        # ("yyyy-MM-dd'T'HH:mm:ss",            "2017-02-11'T'18:31:44"),
        # ("yyyy-MM-dd*HH:mm:ss:SSS",          "2017-10-30*02:47:33:899"),
        # ("yyyy-MM-dd*HH:mm:ss",              "2017-07-04*13:23:55"),
        # ("yy-MM-dd HH:mm:ss,SSS ZZZZ",       "11-02-11 16:47:35,985 +0000"),
        # ("yy-MM-dd HH:mm:ss,SSS",            "10-06-26 02:31:29,573"),
        # ("yy-MM-dd HH:mm:ss",                "10-04-19 12:00:17"),
        # ("yy/MM/dd HH:mm:ss",                "06/01/22 04:11:05"),
        # ("yyMMdd HH:mm:ss",                  "150423 11:42:35"),
        # ("yyyyMMdd HH:mm:ss.SSS",            "20150423 11:42:35.173"),
        # ("MM/dd/yy*HH:mm:ss",                "08/10/11*13:33:56"),
        # ("MM/dd/yyyy*HH:mm:ss",              "11/22/2017*05:13:11"),
        # ("MM/dd/yyyy*HH:mm:ss*SSS",          "05/09/2017*08:22:14*612"),
        # ("MM/dd/yy HH:mm:ss ZZZZ",           "04/23/17 04:34:22 +0000"),
        # ("MM/dd/yyyy HH:mm:ss ZZZZ",         "10/03/2017 07:29:46 -0700"),
        # ("HH:mm:ss",                         "11:42:35"),
        # ("HH:mm:ss.SSS",                     "11:42:35.173"),
        # ("HH:mm:ss,SSS",                     "11:42:35,173"),
        # ("dd/MMM HH:mm:ss,SSS",              "23/Apr 11:42:35,173"),
        # ("dd/MMM/yyyy:HH:mm:ss",             "23/Apr/2017:11:42:35"),
        # ("dd/MMM/yyyy HH:mm:ss",             "23/Apr/2017 11:42:35"),
        # ("dd-MMM-yyyy HH:mm:ss",             "23-Apr-2017 11:42:35"),
        # ("dd-MMM-yyyy HH:mm:ss.SSS",         "23-Apr-2017 11:42:35.883"),
        # ("dd MMM yyyy HH:mm:ss",             "23 Apr 2017 11:42:35"),
        # ("dd MMM yyyy HH:mm:ss*SSS",         "23 Apr 2017 10:32:35*311"),
        # ("MMdd_HH:mm:ss",                    "0423_11:42:35"),
        # ("MMdd_HH:mm:ss.SSS",                "0423_11:42:35.883"),
        # ("MM/dd/yyyy hh:mm:ss a:SSS",        "8/5/2011 3:31:18 AM:234"),
        # ("MM/dd/yyyy hh:mm:ss a",            "9/28/2011 2:23:15 PM"),
    )

    for fmt, example, example_ts in formats:

        re_parts = list()
        parse_parts = list()

        fmt = DateFormat(fmt.upper(), example.upper())

        # Form RE to match the pattern
        for token in split_format(fmt.fmt):

            # Punct
            if token == ' ':
                re_parts.append("\s+")
                parse_parts.append(' ')
            elif token == ':':
                re_parts.append(":")
                parse_parts.append(':')
            elif token == '.':
                re_parts.append("\.")
                parse_parts.append('.')

            # Timezone
            elif token == 'ZZZ':
                re_parts.append("[A-Z]{3}")
                parse_parts.append('%Z')

            # Year
            elif token == 'YYYY':
                re_parts.append("\d{4}")
                parse_parts.append('%Y')

            # Month
            elif token == 'MMM':
                re_parts.append("(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)")
                parse_parts.append("%b")

            # Day
            elif token == 'DD':
                re_parts.append("\d\d?")
                parse_parts.append('%d')

            # Hour
            elif token == 'HH':
                re_parts.append("\d\d?")
                parse_parts.append('%H')

            # Minute
            elif token == 'MM':
                re_parts.append("\d\d?")
                parse_parts.append('%M')

            # Second
            elif token == 'SS':
                re_parts.append("\d\d?")
                parse_parts.append('%S')

            # Sub-second
            elif token == 'SSS':
                re_parts.append("\d\d?")
                parse_parts.append('%f') # %f for microseconds
                fmt.shims.append(lambda ts: )

            else:
                raise Exception("Unknown token in date format %s: '%s'" % (fmt.fmt, token))

        fmt.re_src = ''.join(re_parts)
        fmt.parsestr = ''.join(parse_parts)

        # Check that pattern matches the example
        if not re.compile('^' + fmt.re_src + '$').match(fmt.example.upper()):
            raise ValueError("RE ^%s$ from date pattern %s doesn't match example %s" % (
                fmt.re_src, fmt.fmt, fmt.example.upper()))

        # Check parser returns same date
        try:
            parsed = datetime.strptime(fmt.example, fmt.parsestr)
            parsed = shim_year(parsed)
        except Exception as e:
            raise ValueError("datetime.strptime('%s', '%s') failed: %s" % (
                fmt.example,
                fmt.parsestr,
                str(e)))
        if parsed != example_ts:
            raise ValueError("datetime.strptime('%s', '%s')\nreturned: %s\nexpected: %s" % (
                fmt.example,
                fmt.parsestr,
                str(parsed),
                str(example_ts)))

        yield fmt