import os
import yaml
CONFIG_FILE_NAME = ".jenksrc"

RANGES = (('0', '9'), ('a', 'z'), ('A', 'Z'))

UNABLE_TO_FIND_JENKS_CONFIG = """
Unable to find {0} file! Maybe you need to add one?

Jenks searches for files from the current working directory up.

Example .jenksrc:

localhost:
  url: 'http://localhost:8080/'
  jobs:
    - foo
    - bar
""".format(CONFIG_FILE_NAME)


class JenksException(Exception):
    """ an exception to notify that the exception arrives from jenks """
    pass


def generate_valid_keys():
    """ create a list of valid keys """
    valid_keys = []
    for minimum, maximum in RANGES:
        for i in range(ord(minimum), ord(maximum) + 1):
            valid_keys.append(chr(i))
    return valid_keys


def get_configuration_file():
    """ return jenks configuration file """
    path = os.path.abspath(os.curdir)
    while path != os.sep:
        config_path = os.path.join(path, CONFIG_FILE_NAME)
        if os.path.exists(config_path):
            return config_path
        path = os.path.dirname(path)
    raise JenksException(UNABLE_TO_FIND_JENKS_CONFIG)


def generate_write_yaml_to_file(file_name):
    """ generate a method to write the configuration in yaml to the method desired """
    def write_yaml(config):
        with open(file_name, 'w+') as fh:
            fh.write(yaml.dump(config))
    return write_yaml
