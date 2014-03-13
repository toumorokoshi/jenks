from nose.tools import eq_, ok_

from jenks.data import JenksData

config_dict = {
    'localhost': {
        'url': 'http://localhost:8080/',
        'jobs': [
            'foo',
            'bar'
        ]
    }
}


class TestData(object):

    def setUp(self):
        self.data = JenksData(config_dict)

    def test_job_keys(self):
        """ job_keys() should return a list of sorted one-character keys"""
        result_keys = ('0', '1')
        for return_key, result_key in zip(self.data.job_keys(), result_keys):
            eq_(return_key, result_key)

    def test_get_jobs_from_arguments(self):
        """ get_jobs_from_arguments(":<keys>") should return all JenksJob objects """
        jobs = self.data.get_jobs_from_arguments(":01")
        ok_(any(map(lambda x: x.name == 'foo', jobs)))
        ok_(any(map(lambda x: x.name == 'bar', jobs)))

    def test_add_job(self):
        """ add_job(<host>, <job_name>) should add the job to the JenksData object """
        self.data.add_job("localhost", "baz")
        ok_(self.data.has_job('localhost', 'baz'))

    def test_add_job_host_url(self):
        """ add_job(<host_url>, <job_name>) should add the job to the JenksData object """
        self.data.add_job("http://localhost:8080/", "baz")
        ok_(self.data.has_job('localhost', 'baz'))


class TestYamlConfig(object):
