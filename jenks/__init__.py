"""Jenks, a Jenkins command line tool.
Usage:
  jenks [<keys>] [-c | -l]

Options:
  -c, --console   print console information
  -l, --list      list the jobs
"""
import signal
import sys

from docopt import docopt
from .data import get_configuration, JenksData
from .command import List, Console, Status


def signal_handler(signal, frame):
    sys.exit(0)

DEFAULT_COMMAND = Status
ARGUMENT_COMMANDS = [List, Console]


def main(argv=sys.argv[1:]):
    signal.signal(signal.SIGINT, signal_handler)
    options = docopt(__doc__, argv=argv, version="jenks 0.1")
    #try:
    data = JenksData(get_configuration())
    inp = None
    if not sys.stdin.isatty():
        inp = sys.stdin.read().strip().replace('\n', '')
    keys = options['<keys>'] or inp or data.job_keys()
    command = DEFAULT_COMMAND
    for cmd in ARGUMENT_COMMANDS:
        if options[cmd.argument]:
            command = cmd
    for job in data.jobs(keys):
        print(command.act(job))
    #except Exception as e:
    #    print("Error! {0}".format(str(e)))

if __name__ == '__main__':
    main()
