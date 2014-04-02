import shlex
from mock import patch, Mock
from jenks.data import JenksData
from .test_data import config_dict
from jenks import main


class TestMain(object):
    """ tests for the main jenks interface """

    def setUp(self):
        self.jenksdata = JenksData(config_dict)

    def test_list_command(self):
        with patch('jenks._get_jenks_config') as get_jenks_config:
            get_jenks_config.return_value = self.jenksdata
            args = shlex.split("jenks -l")
            print_method = Mock()
            main(args, print_method=print_method)
            assert print_method.called_with('0 localhost bar')
            assert print_method.called_with('1 localhost foo')
