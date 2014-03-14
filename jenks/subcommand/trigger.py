"""
Jenks trigger, to trigger a particular job

Usage:
    trigger <keys_or_code>
"""
import logging

import requests
from docopt import docopt

LOGGER = logging.getLogger(__name__)


def trigger(data, argv):
    options = docopt(__doc__, argv=argv)

    jobs = data.get_jobs_from_arguments(job_keys=options['<keys_or_code>'])

    for job in jobs:
        LOGGER.info(trigger_job(job))


def trigger_job(job):
    """ trigger a job """
    if job.api_instance().is_running():
        return "{0}, {1} is already running".format(job.host, job.name)
    else:
        requests.get(job.api_instance().get_build_triggerurl())
        return "triggering {0}, {1}...".format(job.host, job.name)
