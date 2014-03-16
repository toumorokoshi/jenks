import shlex
from mock import patch
from .test_base import TestSubcommandBase, TestJobActionBase
from nose.tools import ok_

from jenks.subcommand import trigger


class TestTrigger(TestSubcommandBase):

    def test_trigger_command(self):
        """ trigger command should trigger jobs """
        with patch('jenks.subcommand.trigger._trigger_job') as trigger_job:
            args = shlex.split(":1")
            trigger.trigger(self.data, args)
            ok_(self.data.get_jobs_from_argument.called)
            ok_(trigger_job.called_with(self.job_mock))


class TestTriggerJob(TestJobActionBase):

    def test_trigger_job(self):
        """ _trigger_job should trigger a job """
        pass
