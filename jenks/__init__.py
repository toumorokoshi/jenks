"""Jenks, a Jenkins command line tool.
Usage:
  jenks [<keys>] [-c]

Options:
  -c, --console   print console information
"""
import signal
import sys

from docopt import docopt
from .config import get_configuration, Config


def signal_handler(signal, frame):
    sys.exit(0)


def main(argv=sys.argv[1:]):
    signal.signal(signal.SIGINT, signal_handler)
    #try:
    options = docopt(__doc__, argv=argv, version="jenks 0.1")
    config = Config(get_configuration())
    if options['--console']:
        config.get_console(options['<keys>'])
    else:
        config.get_status(options['<keys>'])
    #except Exception as e:
    #    print("Error! {0}".format(str(e)))

if __name__ == '__main__':
    main()
