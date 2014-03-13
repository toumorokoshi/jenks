"""Jenks, a Jenkins command line tool.
Usage:
  jenks docs
  jenks [<keys>] [-l | -t]
  jenks <command> [<args>...]
  jenks (-h | --help)
  jenks

Options:
  -l, --list      list the jobs
  -t, --trigger   trigger jobs
  -h, --help      print this help guide. use `jenks docs` for a full page of documentation

Available Jenks Commands:
  config    modify jenks configuration
  build     get information about a specific build for a job
"""
import logging
import signal
import sys
import yaml

from docopt import docopt
from .data import JenksData
from .utils import get_configuration_file, generate_write_yaml_to_file
from .command import List, Status, Trigger
from .docs import DOCS, README_CONTENT
from .subcommand import build, config


def signal_handler(signal, frame):
    sys.exit(0)

DEFAULT_COMMAND = Status
ARGUMENT_COMMANDS = [List, Trigger]


def _create_stdout_logger():
    """ create a logger to stdout """
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)


def _get_jenks_config():
    """ retrieve the jenks configuration object """
    config_file = get_configuration_file()
    with open(config_file, 'r') as fh:
        return JenksData(
            yaml.load(fh.read()),
            write_method=generate_write_yaml_to_file(config_file)
        )


def main(argv=sys.argv[1:]):
    signal.signal(signal.SIGINT, signal_handler)
    _create_stdout_logger()
    options = docopt(__doc__, argv=argv,
                     version="jenks 0.2",
                     options_first=True)
    if options['docs']:
        print(DOCS.format(
            readme=README_CONTENT,
            usage=__doc__
        ))
        sys.exit(0)
    try:
        data = _get_jenks_config()
        # parse subcommands
        if options['<command>']:
            subcommand_argv = options['<args>']
            if options['<command>'] == 'build':
                return build.build(data, subcommand_argv)
            elif options['<command>'] == 'config':
                return config.config(data, subcommand_argv)
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
        raise
        print("Error! {0}".format(str(e)))

if __name__ == '__main__':
    main()
