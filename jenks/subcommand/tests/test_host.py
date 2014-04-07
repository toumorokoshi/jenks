import shlex
from mock import patch
from nose.tools import ok_, eq_
from .test_base import TestSubcommandBase, TestJobActionBase
from jenks.subcommand.host import host, get_all_jobs, get_all_hosts


class TestHostParse(TestSubcommandBase):

    def test_no_options(self):
        """ with no options, host should print a list of hosts """
        with patch('jenks.subcommand.host.get_all_hosts') as m_get_all_hosts:
            host(self.data, [])
            ok_(m_get_all_hosts.called_with((self.jenkins_mock,)))

    def test_with_key(self):
        """ with a host key, host should print a list of jobs """
        with patch('jenks.subcommand.host.get_all_jobs') as m_get_all_jobs:
            args = shlex.split("key")
            host(self.data, args)
            ok_(m_get_all_jobs.called_with(self.jenkins_mock))


class TestHostMethods(TestJobActionBase):

    def test_get_all_hosts(self):
        """ get_all_hosts should return a newline-delimited list of hosts"""
        eq_(get_all_hosts(("foo", "bar")), "foo\nbar")

    def test_get_all_jobs(self):
        """ get_all_jobs should print a list of jobs """
        eq_(get_all_jobs(self.jenkins), "foo")
