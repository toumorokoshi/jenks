"""
Jenks build, to output information about jenkins builds. By default,
jenks will print all output regarding a build. If one or more
qualifiers are passed, that subset will be printed instead.

Usage:
    build (<keys> | -j <job_code>) [ -csw ] [ -b <build_id> ]

Options:
    -j <job_code>, --jobs <job_code>     host:name job code
    -c, --console                        console output
    -s, --scm                            scm information
    -w, --wait                           if a build is running, wait until the build is finished before returning
    -b <build_id>, --build <build_id>    output information regarding a specific build
"""
import logging

from docopt import docopt
from jenks.utils import JenksException

LOGGER = logging.getLogger(__name__)

DEFAULT_BUILD_KEYS = ('console', 'scm')


class BuildException(JenksException):
    pass


def build(data, argv):
    options = docopt(__doc__, argv=argv)

    keys = []
    wait = False
    build_id = None
    jobs = data.get_jobs_from_arguments(job_keys=options['<keys>'],
                                        job_code=options['--jobs'])
    if options['--console']:
        keys.append('console')

    if options['--scm']:
        keys.append('scm')

    if options['--wait']:
        wait = True

    if options['--build']:
        build_id = options['--build']

    for job in jobs:
        LOGGER.info(get_build_info(job, build_id=build_id,
                                   keys=(keys or DEFAULT_BUILD_KEYS),
                                   wait=wait))


def get_build_info(job, build_id=None, keys=DEFAULT_BUILD_KEYS, wait=False):
    """ print build info about a job """
    build = job.get_build(build_id) if build_id else job.get_last_build()
    output = ""

    if wait:
        build.block_until_complete()

    if 'console' in keys:
        output += build.get_console()

    if 'scm' in keys:
        output += build.get_revision()

    return output