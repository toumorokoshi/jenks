"""
Jenks config, to manage jenks configurations.  All actions will
directly affect the loaded jenks configuration, defaulting to the user
root if no config is found.

Usage:
    config (-a <job_url> | --add <job_url>)

Options:
    -a <job_url>, --add <job_url>    Add a job
"""
import logging
from urlparse import urlparse

from docopt import docopt
from jenks.utils import JenksException

LOGGER = logging.getLogger(__name__)


class ConfigException(JenksException):
    pass


def config(data, argv):
    options = docopt(__doc__, argv=argv)

    if options['--add']:
        job_info = _parse_add_url(options['--add'])
        LOGGER.info("Adding job: {0}".format(job_info))
        data.add_job(*job_info)
    data.write()


def _parse_add_url(url):
    """ return a tuple (host, job_name) from a url """
    parsed_url = urlparse(url)
    job_name = None
    paths = parsed_url.path.strip("/").split("/")
    for i, path in enumerate(paths):
        if path == "job" and len(paths) > i:
            job_name = paths[i + 1]
    if job_name is None:
        raise ConfigException("Unable to parse valid job from {0}".format(url))
    return (
        "{0}://{1}".format(parsed_url.scheme, parsed_url.netloc),
        job_name
    )
