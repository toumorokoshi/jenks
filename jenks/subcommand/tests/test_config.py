import shlex
from jenks.subcommand.config import config, _parse_add_url, ConfigException
from jenks.data import JenksData
from nose.tools import eq_, raises
from mock import Mock


class TestConfigParse(object):

    def test_add_url_options(self):
        """ config --add <url> should add a jenkins url """
        args = shlex.split("--add 'http://localhost:8080/job/bar'")
        data = Mock(spec=JenksData)
        config(data, args)
        data.add_job.assert_called_with('http://localhost:8080', 'bar')
        data.write.assert_called_with()


class TestParseAddUrl(object):

    def test_parse_add_url(self):
        """ a jenkins job url should resolve to a host and jobname """
        TEST_URL = "http://localhost:8080/job/bar/"
        eq_(_parse_add_url(TEST_URL), ('http://localhost:8080', 'bar'))

    def test_parse_add_url_from_view(self):
        """ a jenkins job url should resolve to a host and jobname """
        TEST_URL = "http://localhost:8080/view/baz/job/bar/"
        eq_(_parse_add_url(TEST_URL), ("http://localhost:8080", "bar"))

    def test_parse_add_url_from_view_with_build_id(self):
        """ a jenkins job url should resolve to a host and jobname """
        TEST_URL = "http://localhost:8080/view/baz/job/bar/17/"
        eq_(_parse_add_url(TEST_URL), ("http://localhost:8080", "bar"))

    @raises(ConfigException)
    def test_parse_add_url_bad_url(self):
        """ a bad jenkins job url should raise an exception """
        TEST_URL = "http://localhost:8080/view/baz/"
        _parse_add_url(TEST_URL)
