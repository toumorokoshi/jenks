import shlex
from mock import Mock
from jenks.subcommand.build import build
from jenks.data import JenksData
from jenkinsapi.job import Job
from nose.tools import ok_, eq_, raises
from mock import patch


class TestBuildParse(object):

    def setUp(self):
        self.data = Mock(spec=JenksData)
        self.job_mock = Mock(spec=Job)
        self.data.get_jobs_from_arguments = Mock(return_value=(self.job_mock,))

    def test_options_no_options(self):
        """ build <keys> should print build summaries for the job """
        with patch('jenks.subcommand.build._print_build_info') as _print_build_info:
            args = shlex.split(":1")
            build(self.data, args)
            self.data.get_jobs_from_arguments.assert_called_with(job_keys=":1",
                                                                 job_code=None)
            ok_(_print_build_info.called_with(self.job_mock))

    def test_options_job_code(self):
        """ build -j <job_code> should return job code """
        args = shlex.split("-j host:name")
        build(self.data, args)
        self.data.get_jobs_from_arguments.assert_called_with(job_keys=None,
                                                             job_code="host:name")

    def test_options_console_only(self):
        """ build -c should print just console output """
        with patch('jenks.subcommand.build._print_build_info') as _print_build_info:
            args = shlex.split(":1 -c")
            build(self.data, args)
            ok_(_print_build_info.called_with(self.job_mock, keys=('console,')))

    def test_options_wait(self):
        """ build -w should pass _print_build_info wait """
        with patch('jenks.subcommand.build._print_build_info') as _print_build_info:
            args = shlex.split(":1 -c")
            build(self.data, args)
            ok_(_print_build_info.called_with(self.job_mock, wait=True))

    def test_options_scm(self):
        """ build -s should pass _print_build_info scm """
        with patch('jenks.subcommand.build._print_build_info') as _print_build_info:
            args = shlex.split(":1 -c")
            build(self.data, args)
            ok_(_print_build_info.called_with(self.job_mock, keys=('scm')))

    def test_options_build_id(self):
        """ build -b <build_id> should pass _print_build_info <build_id> """
        with patch('jenks.subcommand.build._print_build_info') as _print_build_info:
            args = shlex.split(":1 -b 12")
            build(self.data, args)
            ok_(_print_build_info.called_with(self.job_mock, build_id=12))

    def test_options_multiple_options(self):
        """ build -csw -b <build_id> should aggregate functionality """
        with patch('jenks.subcommand.build._print_build_info') as _print_build_info:
            args = shlex.split(":1 -csw -b 12")
            build(self.data, args)
            ok_(_print_build_info.called_with(self.job_mock, build_id=12, keys=('console', 'scm'), wait=True))


class TestPrintBuildInfo(object):
    pass
