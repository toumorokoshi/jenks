import os
from jenkinsapi.jenkins import Jenkins
from collections import namedtuple
import yaml

CONFIG_FILE_NAME = ".jenksrc"

STATUS_STRING = "{key}: {host}, {name} (build #{number}) {status}"
LIST_TEMPLATE = "{key} {host} {name}"

KEYS = ('0', '1', '2', '3', '4')

UNABLE_TO_FIND_JENKS_CONFIG = """
Unable to find {0} file! Maybe you need to add one?

Jenks searches for files from the current working directory up.

Example .jenksrc:

localhost:
  url: 'http://localhost:8080/'
  jobs:
    - foo
    - bar
""".format(CONFIG_FILE_NAME)


class JenksDataException(Exception):
    """ Wrapper for configs """

JenksJob = namedtuple('JenksJob', 'key, host, name, api_instance')


class JenksData(object):

    def __init__(self, config_dict):
        self._parse_dict(config_dict)

    def job_keys(self):
        """ return a list of jobs """
        return (j for j in self._jobs)

    def jobs(self, job_keys):
        return (self._jobs[key] for key in job_keys)

    def _parse_dict(self, config_dict):
        """ parse the dictionary into a config object """
        self.hosts_info = config_dict
        self.hosts = {}
        self._jobs = {}
        self._empty_key_index = 0
        for host, info in config_dict.items():
            url = info.get('url', host)
            self.hosts[host] = Jenkins(url)
            if 'jobs' in info:
                for job_name in info['jobs']:
                    self._add_job(host, job_name)

    def _add_job(self, host, job_name):
        key = self._empty_key_index
        value = JenksJob(key, host, job_name, self.hosts[host][job_name])
        self._jobs[key] = value
        self._empty_key_index += 1


def get_configuration():
    """ return jenks configuration """
    path = os.path.abspath(os.curdir)
    while path != os.sep:
        config_path = os.path.join(path, CONFIG_FILE_NAME)
        if os.path.exists(config_path):
            with open(config_path) as fh:
                return yaml.load(fh.read())
        path = os.path.dirname(path)
    raise JenksDataException(UNABLE_TO_FIND_JENKS_CONFIG)
