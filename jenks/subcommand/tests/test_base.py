from mock import Mock
from jenks.data import JenksData, JenksJob
from jenkinsapi.job import Job
from jenkinsapi.build import Build
from jenkinsapi.jenkins import Jenkins


class TestSubcommandBase(object):

    def setUp(self):
        self.data = Mock(spec=JenksData)
        self.api_instance_mock = Mock(spec=Job)
        self.job_mock = Mock(spec=JenksJob)
        self.jenkins_mock = Mock(spec=Jenkins)
        self.job_mock.api_instance.return_value = self.api_instance_mock
        self.data.get_jobs_from_argument = Mock(return_value=(self.job_mock,))
        self.data.hosts = Mock(return_value=(self.jenkins_mock,))


class TestJobActionBase(object):

    def setUp(self):
        self.job = Mock(JenksJob)
        self.api_instance = Mock(spec=Job)
        self.job.api_instance = self.api_instance
        # jenkins mock
        self.jenkins = Mock(spec=Jenkins)

        def get_jobs():
            yield ('foo', self.job)
        self.jenkins.get_jobs = Mock(return_value=get_jobs())

        self.build = Mock(spec=Build)
        self.build_console_output = "FOO"
        self.build_revision_output = "BAR"
        self.build_timestamp_output = "BAZ"
        self.build.get_console.return_value = self.build_console_output
        self.build.get_revision.return_value = self.build_revision_output
        self.build.get_timestamp.return_value = self.build_timestamp_output
