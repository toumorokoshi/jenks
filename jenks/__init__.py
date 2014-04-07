"""Jenks, a Jenkins command line tool.
Usage:
  jenks docs
  jenks <command> [<args>...]
  jenks [-l | -t] [<keys_or_code>]
  jenks (-h | --help)
  jenks

Options:
  -l, --list      list the jobs
  -h, --help      print this help guide. use `jenks docs` for a full page of documentation

Available Jenks Commands:
  config    modify jenks configuration
  build     get information about a specific build for a job
  host      prints information about a host
  trigger   trigger a job
"""
import logging
import os
import signal
import sys
import yaml

from docopt import docopt
from .data import JenksData
from .utils import (get_configuration_file,
                    generate_write_yaml_to_file,
                    CONFIG_FILE_NAME)
from .command import List, Status
from .docs import DOCS, README_CONTENT
from .subcommand import build, config, trigger, host


def signal_handler(signal, frame):
    sys.exit(0)

DEFAULT_COMMAND = Status
ARGUMENT_COMMANDS = [List]
SUBCOMMANDS = (
    ('build', build.build),
    ('config', config.config),
    ('trigger', trigger.trigger),
    ('host', host.host)
)


def _create_stdout_logger():
    """ create a logger to stdout """
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)


def _get_jenks_config():
    """ retrieve the jenks configuration object """
    config_file = (get_configuration_file() or
                   os.path.expanduser(os.path.join("~", CONFIG_FILE_NAME)))

    if not os.path.exists(config_file):
        open(config_file, 'w').close()

    with open(config_file, 'r') as fh:
        return JenksData(
            yaml.load(fh.read()),
            write_method=generate_write_yaml_to_file(config_file)
        )


def main(argv=sys.argv[1:], print_method=None):

    if print_method is None:
        def print_to_stdout(x):
            print(x)
        print_method = print_to_stdout

    signal.signal(signal.SIGINT, signal_handler)
    _create_stdout_logger()
    options = docopt(__doc__, argv=argv, options_first=True)
    if options['docs']:
        print(DOCS.format(
            readme=README_CONTENT,
            usage=__doc__
        ))
        sys.exit(0)
    try:
        data = _get_jenks_config()
        inp = None
        if not sys.stdin.isatty():
            inp = sys.stdin.read().strip().replace('\n', '')
        # parse subcommands
        if options['<command>']:
            subcommand_argv = options['<args>']
            if inp:
                subcommand_argv.append(inp)
            for name, method in SUBCOMMANDS:
                if options['<command>'] == name:
                    return method(data, subcommand_argv)

        keys_or_code = options['<keys_or_code>'] or options['<command>'] or inp
        if keys_or_code is None:
            jobs = data.jobs(data.job_keys())
        else:
            jobs = data.get_jobs_from_argument(keys_or_code)

        command = DEFAULT_COMMAND
        for cmd in ARGUMENT_COMMANDS:
            if options[cmd.argument]:
                command = cmd
        for job in jobs:
            print_method(command.act(job))
    except AssertionError as e:
        print_method("Error! {0}".format(str(e)))
    except Exception as e:
        raise

if __name__ == '__main__':
    main()
