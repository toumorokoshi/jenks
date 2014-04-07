import copy

from jenkinsapi import jenkins
from collections import namedtuple

from .utils import generate_valid_keys

CONFIG_FILE_NAME = ".jenksrc"

STATUS_STRING = "{key}: {host}, {name} (build #{number}) {status}"
LIST_TEMPLATE = "{key} {host} {name}"

KEYS = generate_valid_keys()

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

    def __init__(self, config_dict, write_method=None):
        self._write_method = write_method
        self._config_dict = copy.deepcopy(config_dict) or {}
        self._host_cache = {}
        self._host_list = list(self._config_dict.keys())
        self._job_cache = {}
        self._jobs = {}
        self._empty_key_index = 0
        for host in sorted(self._host_list):
            host_dict = self._config_dict[host]
            host_url = host_dict.get('url', None)
            if 'jobs' in host_dict:
                for job in host_dict['jobs']:
                    self._add_job(host, job, host_url=host_url)

    def _get_job_api_instance(self, host, job_name):
        if host not in self._job_cache:
            self._job_cache[host] = {}
        if job_name not in self._job_cache[host]:
            host_api_instance = self.get_host(host)
            self._job_cache[host][job_name] = host_api_instance[job_name]

        return self._job_cache[host][job_name]

    def get_host(self, host):
        if host not in self._host_cache:
            host_url = host
            if host in self._config_dict:
                host_url = self._config_dict[host].get('url', host_url)
            self._host_cache[host] = jenkins.Jenkins(host_url)
        return self._host_cache[host]

    def job_keys(self):
        """ return a list of jobs """
        return sorted((j for j in self._jobs))

    def jobs(self, job_keys):
        return (self._jobs[key] for key in job_keys)

    def hosts(self):
        """ return a generator of hosts """
        return (h for h in self._host_list)

    def get_jobs_from_argument(self, raw_job_string):
        """ return a list of jobs corresponding to the raw_job_string """
        jobs = []
        if raw_job_string.startswith(":"):
            job_keys = raw_job_string.strip(" :")
            jobs.extend([job for job in self.jobs(job_keys)])
        # we assume a job code
        else:
            assert "/" in raw_job_string, "Job Code {0} is improperly formatted!".format(raw_job_string)
            host, job_name = raw_job_string.rsplit("/", 1)
            host_url = self._config_dict.get(host, {}).get('url', host)
            host = self.get_host(host_url)
            if host.has_job(job_name):
                jobs.append(JenksJob(None, host, job_name,
                                     lambda: self._get_job_api_instance(host_url, job_name)))
            else:
                raise JenksDataException(
                    "Could not find Job {0}/{1}!".format(host, job_name))
        return jobs

    def has_job(self, host, job_name):
        """ return true if the job in the JenksData """
        return job_name in self._config_dict.get(host, {'jobs': []})['jobs']

    def add_job(self, raw_host, job_name):
        """ add a job to the config with <host> and <job_name> """
        url_host_map = dict(((host_dict.get('url', host_name).rstrip('/'), host_name)
                             for host_name, host_dict in self._config_dict.items()))

        if raw_host in self._config_dict:
            host_url = self._config_dict[raw_host].get('url', raw_host)
            host = raw_host
        elif raw_host in url_host_map:
            host_url = raw_host
            host = url_host_map[raw_host]
        else:
            host_url, host = raw_host, raw_host

        if host not in self._config_dict:
            self._config_dict[host] = {
                'url': host_url,
                'jobs': []
            }
        self._config_dict[host]['jobs'].append(job_name)
        self._add_job(host, job_name, host_url=host_url)

    def write(self):
        if self._write_method is not None:
            self._write_method(self._config_dict)

    def _add_job(self, host, job_name, host_url=None):
        if host_url is None:
            host_url = host
        key = KEYS[self._empty_key_index]

        def get_api_instance():
            return self._get_job_api_instance(host_url, job_name)
        value = JenksJob(key, host, job_name, get_api_instance)
        self._jobs[key] = value
        self._empty_key_index += 1
