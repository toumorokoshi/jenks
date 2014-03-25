from jenks.data import JenksJob
from jenks.command import Status, List
from jenkinsapi.job import Job
from jenkinsapi.build import Build
from mock import Mock
from nose.tools import eq_


class TestStatus():

    def setUp(self):
        """ if the job has run, Status.act should return the current status """
        # mock build
        self.mock_build = Mock(spec=Build)
        self.mock_build.get_number.return_value = 1
        self.mock_build.get_status.return_value = "status"
        # mock job
        self.mock_job = Mock(spec=Job)
        self.mock_job.get_last_build.return_value = self.mock_build
        self.mock_job.is_queued.return_value = False
        # jenks job
        self.job = JenksJob('key', 'host', 'name', lambda: self.mock_job)

    def test_is_queued(self):
        """ if job is queued, Status.act should return queued """
        self.mock_job.is_queued.return_value = True
        eq_(Status.act(self.job), "key: host, name (last build #1) queued")

    def test_last_build(self):
        """ if job is queued, Status.act should return queued """
        eq_(Status.act(self.job), "key: host, name (last build #1) status")


def test_list():
    """ List.act should return a list job template """
    job = JenksJob('key', 'host', 'name', Mock())
    eq_(List.act(job), "key host name")
