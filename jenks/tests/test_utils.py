import os
import tempfile
import shutil
from nose.tools import ok_, eq_
from jenks.utils import (generate_valid_keys,
                         generate_write_yaml_to_file,
                         get_configuration_file,
                         CONFIG_FILE_NAME)


def test_valid_keys():
    """ get_valid_keys should produce valid one-character shortcuts """
    keys = generate_valid_keys()
    ok_('0' in keys)
    ok_('9' in keys)
    ok_('a' in keys)
    ok_('z' in keys)
    ok_('A' in keys)
    ok_('Z' in keys)
    ok_('!' not in keys)
    ok_('?' not in keys)


def test_generate_write_yaml_to_file():
    """ generate_write_yaml_to_file should generate a method to write yaml to a file """
    temp_file_path = tempfile.mkstemp()[1]
    desired_content = """
{foo: bar}
"""
    try:
        dump_method = generate_write_yaml_to_file(temp_file_path)
        config = {'foo': 'bar'}
        dump_method(config)
        contents = None
        with open(temp_file_path) as fh:
            contents = fh.read()
        eq_(contents.strip(), desired_content.strip())
    finally:
        os.unlink(temp_file_path)


CONFIG_TEMPLATE = """
foo: bar
""".strip()


class TestGetConfigurationFile(object):

    def setUp(self):
        self.original_dir = os.getcwd()
        self.temp_dir = tempfile.mkdtemp()
        self.jenksrc_path = os.path.join(self.temp_dir, CONFIG_FILE_NAME)
        with open(self.jenksrc_path, 'w+') as fh:
            fh.write(CONFIG_TEMPLATE)
        os.chdir(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        os.chdir(self.original_dir)

    def test_get_configuration_file(self):
        """ get_configuration_file should get the configuration file in the cwd if it exists """
        eq_(get_configuration_file(), self.jenksrc_path)
