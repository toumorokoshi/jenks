"""Jenks, a Jenkins command line tool.
Usage:
  jenks docs
  jenks [<keys>] [-c | -l | -t]
  jenks (-h | --help)

Options:
  -c, --console   print console information
  -l, --list      list the jobs
  -t, --trigger   trigger jobs
  -h, --help      print this help guide. use `jenks docs` for a full page of documentation
"""
import signal
import sys

from docopt import docopt
from .data import get_configuration, JenksData
from .command import List, Console, Status, Trigger
from .docs import DOCS, README_CONTENT


def signal_handler(signal, frame):
    sys.exit(0)

DEFAULT_COMMAND = Status
ARGUMENT_COMMANDS = [List, Console, Trigger]


def main(argv=sys.argv[1:]):
    signal.signal(signal.SIGINT, signal_handler)
    options = docopt(__doc__, argv=argv, version="jenks 0.2")
    if options['docs']:
        print(DOCS.format(
            readme=README_CONTENT,
            usage=__doc__
        ))
        sys.exit(0)
    try:
        data = JenksData(get_configuration())

        inp = None
        if not sys.stdin.isatty():
            inp = sys.stdin.read().strip().replace('\n', '')
        keys = options['<keys>'] or inp 
        if keys:
            keys = keys.lstrip(':')
        else:
            keys = data.job_keys()

        command = DEFAULT_COMMAND
        for cmd in ARGUMENT_COMMANDS:
            if options[cmd.argument]:
                command = cmd
        for job in data.jobs(sorted(keys)):
            print(command.act(job))
    except Exception as e:
        print("Error! {0}".format(str(e)))

if __name__ == '__main__':
    main()
