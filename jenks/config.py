import os
from jenkinsapi.jenkins import Jenkins
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


class ConfigException(Exception):
    """ Wrapper for configs """


class Config(object):

    def __init__(self, config_dict):
        self._parse_dict(config_dict)

    def job_keys(self):
        """ return a list of jobs """
        return (j for j in self._jobs)

    def get_status(self, keys):
        """ get the status of the jobs """
        for job_key in sorted(keys):
            self.print_job(job_key)

    def get_console(self, keys):
        """ get the console output """
        for job_key in sorted(keys):
            self.print_console(job_key)

    def get_list(self, keys):
        """ list the jobs in a easily parsable manner """
        for job_key in sorted(keys):
            self.print_list(job_key)

    def print_job(self, job_key):
        host, job_name = self._jobs[job_key]
        job = self.hosts[host][job_name]
        last_build = job.get_last_build()
        print(STATUS_STRING.format(
            key=job_key,
            host=host,
            name=job.name,
            number=last_build.get_number(),
            status=last_build.get_status() or "running..."
        ))

    def print_console(self, job_key):
        host, job_name = self._jobs[job_key]
        job = self.hosts[host][job_name]
        self.print_job(job_key)
        print(job.get_last_build().get_console())

    def print_list(self, job_key):
        host, job_name = self._jobs[job_key]
        print(LIST_TEMPLATE.format(key=job_key,
                                   host=host,
                                   name=job_name))

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
        self._jobs[KEYS[self._empty_key_index]] = (host, job_name)
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
    raise ConfigException(UNABLE_TO_FIND_JENKS_CONFIG)
