from nose.tools import eq_

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

    def test_jobs(self):
        pass
