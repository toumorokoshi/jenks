"""
Jenks build, to output information about jenkins builds. By default,
jenks will print all output regarding a build. If one or more
qualifiers are passed, that subset will be printed instead.

Usage:
    build [ <keys_or_code> ] [ -cswt ] [ -b <build_id> ]

Options:
    -c, --console                        console output
    -s, --scm                            scm information
    -t, --timestamp                      get the timestamp
    -w, --wait                           if a build is running, wait until the build is finished before returning
    -b <build_id>, --build <build_id>    output information regarding a specific build
"""
import logging

from docopt import docopt
from jenks.utils import JenksException

LOGGER = logging.getLogger(__name__)

DEFAULT_BUILD_KEYS = ('timestamp', 'console', 'scm')


class BuildException(JenksException):
    pass


def build(data, argv):
    options = docopt(__doc__, argv=argv)

    keys = []
    wait = False
    build_id = None
    jobs = data.get_jobs_from_argument(options['<keys_or_code>'])
    if options['--console']:
        keys.append('console')

    if options['--scm']:
        keys.append('scm')

    if options['--timestamp']:
        keys.append('timestamp')

    if options['--wait']:
        wait = True

    if options['--build']:
        build_id = options['--build']

    for job in jobs:
        LOGGER.info(get_build_info(job.api_instance(), build_id=build_id,
                                   keys=(keys or DEFAULT_BUILD_KEYS),
                                   wait=wait))


def get_build_info(api_instance, build_id=None,
                   keys=DEFAULT_BUILD_KEYS, wait=False):
    """ print build info about a job """
    build = (api_instance.get_build(build_id) if build_id
             else api_instance.get_last_build())
    output = ""

    if wait:
        build.block_until_complete()

    if 'timestamp' in keys:
        output += str(build.get_timestamp()) + '\n'

    if 'console' in keys:
        output += build.get_console() + '\n'

    if 'scm' in keys:
        # https://github.com/salimfadhley/jenkinsapi/pull/250
        # try/except while this is still occuring
        try:
            output += build.get_revision() + '\n'
        except IndexError:
            pass

    return output
