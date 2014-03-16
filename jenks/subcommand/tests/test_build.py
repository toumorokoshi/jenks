import shlex
from mock import Mock, patch
from .test_base import TestSubcommandBase, TestJobActionBase
from jenks.subcommand.build import build, get_build_info
from nose.tools import ok_


class TestBuildParse(TestSubcommandBase):

    def test_options_no_options(self):
        """ build <keys> should print build summaries for the job """
        with patch('jenks.subcommand.build.get_build_info') as get_build_info:
            args = shlex.split(":1")
            build(self.data, args)
            self.data.get_jobs_from_argument.assert_called_with(":1")
            ok_(get_build_info.called_with(self.api_instance_mock))

    def test_options_console_only(self):
        """ build -c should print just console output """
        with patch('jenks.subcommand.build.get_build_info') as get_build_info:
            args = shlex.split(":1 -c")
            build(self.data, args)
            ok_(get_build_info.called_with(self.api_instance_mock,
                                           keys=('console,')))

    def test_options_timestamp_only(self):
        """ build -t should print just timestamp output """
        with patch('jenks.subcommand.build.get_build_info') as get_build_info:
            args = shlex.split(":1 -t")
            build(self.data, args)
            ok_(get_build_info.called_with(self.api_instance_mock,
                                           keys=('timestamp,')))

    def test_options_wait(self):
        """ build -w should pass get_build_info wait """
        with patch('jenks.subcommand.build.get_build_info') as get_build_info:
            args = shlex.split(":1 -c")
            build(self.data, args)
            ok_(get_build_info.called_with(self.api_instance_mock, wait=True))

    def test_options_scm(self):
        """ build -s should pass get_build_info scm """
        with patch('jenks.subcommand.build.get_build_info') as get_build_info:
            args = shlex.split(":1 -c")
            build(self.data, args)
            ok_(get_build_info.called_with(self.api_instance_mock,
                                           keys=('scm')))

    def test_options_build_id(self):
        """ build -b <build_id> should pass get_build_info <build_id> """
        with patch('jenks.subcommand.build.get_build_info') as get_build_info:
            args = shlex.split(":1 -b 12")
            build(self.data, args)
            ok_(get_build_info.called_with(self.api_instance_mock,
                                           build_id=12))

    def test_options_multiple_options(self):
        """ build -csw -b <build_id> should aggregate functionality """
        with patch('jenks.subcommand.build.get_build_info') as get_build_info:
            args = shlex.split(":1 -csw -b 12")
            build(self.data, args)
            ok_(get_build_info.called_with(self.api_instance_mock,
                                           build_id=12,
                                           keys=('console', 'scm'),
                                           wait=True))


class TestPrintBuildInfo(TestJobActionBase):

    def test_get_build_info_default(self):
        """ get_build_info should print defaults without arguments """
        self.api_instance.get_last_build.return_value = self.build
        output = get_build_info(self.api_instance)
        ok_(self.build_console_output in output)
        ok_(self.build_revision_output in output)
        ok_(self.build_timestamp_output in output)

    def test_get_build_info_build_id(self):
        """ get_build_info should print that build's information when a build_id is passed """
        build_id = 10
        self.api_instance.get_build.return_value = self.build
        get_build_info(self.api_instance, build_id=build_id)
        self.api_instance.get_build.assert_called_with(build_id)
        ok_(not self.api_instance.get_last_build.called)

    def test_get_build_info_wait(self):
        """ get_build_info with wait should call block_until_complete """
        self.api_instance.get_last_build.return_value = self.build
        self.build.block_until_complete.return_value = True
        get_build_info(self.api_instance, wait=True)
        ok_(self.build.block_until_complete.called)

    def test_get_build_info_specific_keys(self):
        """ get_build_info with specific keys should only use those specific keys """
        self.api_instance.get_last_build.return_value = self.build
        get_build_info(self.api_instance, keys=('console,'))
        ok_(self.build.get_console.called)
