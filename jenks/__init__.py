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
from .config import get_configuration, Config


def signal_handler(signal, frame):
    sys.exit(0)


def main(argv=sys.argv[1:]):
    signal.signal(signal.SIGINT, signal_handler)
    options = docopt(__doc__, argv=argv, version="jenks 0.1")
    try:
        config = Config(get_configuration())
        inp = ""
        if not sys.stdin.isatty():
            inp = sys.stdin.read().strip().replace('\n', '')
        keys = options['<keys>'] or inp or config.job_keys()
        if options['--console']:
            config.get_console(keys)
        elif options['--list']:
            config.get_list(keys)
        else:
            config.get_status(keys)
    except Exception as e:
        print("Error! {0}".format(str(e)))

if __name__ == '__main__':
    main()
