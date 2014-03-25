from jenks.data import JenksJob
from jenks.command import Status, List
from jenkinsapi import Job, Build
from mock import Mock
from nose.tools import eq_


class TestStatus():

    def setUp(self):
        """ if the job has run, Status.act should return the current status """
        # mock build
        self.mock_build = Mock(spec=Build)
        self.mock_build.get_ = Mock(spec=Build)
        # mock job
        self.mock_job = Mock(spec=Job)
        self.mock_job.get_last_build.return_value = self.mock_build
        self.mock_job.is_queued.return_value = False

    def test_is_queued(self):
        """ if job is queued, Status.act should return queued """
        self.mock_.is_queued.return_value = True



def test_list():
    """ List.act should return a list job template """
    job = JenksJob('key', 'host', 'name', Mock())
    eq_(List.act(job), "key host name")
