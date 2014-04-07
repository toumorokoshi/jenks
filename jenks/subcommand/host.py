"""
Jenks host, to output information about jenkins hosts. By default,
it will output a list of hosts. If a name is present, it will print
information about that host.

Usage:
    host <hostname_or_key>
    host
"""
import logging

from docopt import docopt

LOGGER = logging.getLogger(__name__)


def host(data, argv):
    options = docopt(__doc__, argv=argv)

    if not options['<hostname_or_key>']:
        LOGGER.info(get_all_hosts(data.hosts()))
    else:
        host = data.get_host(options['<hostname_or_key>'])
        LOGGER.info(get_all_jobs(host))


def get_all_hosts(hosts):
    """ return a string of hosts """
    return "\n".join(hosts)


def get_all_jobs(host):
    """ given a jenkins host object, print all jobs """
    return "\n".join((job[0] for job in host.get_jobs()))
