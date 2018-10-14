# pylint: disable=len-as-condition
import os
import pytest
from hazel import environ


class EnvironContext:
    '''Context manager which help swap out original environment variables
    values with temporary values for tests then restoring original values
    back to exit or error. Usage::

        with EnvironContext({'HOME': '/test/foo', 'USER': 'abdul'}):
            ...
    '''

    environ = os.environ

    def __init__(self, env_context):
        self.env_context = env_context
        self.env_backup = {}

    def __enter__(self):
        for key, value in self.env_context.items():
            self.env_backup[key] = self.environ.get(key)
            if value:
                self.environ[key] = value
            elif key in self.environ:
                del self.environ[key]

    def __exit__(self, *exc_info):
        for key, value in self.env_backup.items():
            if value:
                self.environ[key] = value
            elif key in self.environ:
                del self.environ[key]
        return False


class TestEnviron:
    def test_get_set(self):
        k = 'HAZEL_ENV_MODULE'
        keyx, keyy = ('KEY-X', 'KEY-Y')

        with EnvironContext({k: None, keyx: '', keyy: 'stone'}):
            assert k not in environ.keys()
            pytest.raises(KeyError, environ.__getitem__, k)
            assert environ.get(k) is None
            assert environ.get(k, 'FOO') == 'FOO'

            environ[k] = 'BAR'
            assert environ.get(k, 'FOO') == 'BAR'
            assert environ.get(k) == 'BAR'
            assert len(environ) > 0
            assert k in environ

            assert keyx not in environ
            assert keyy in environ

            assert environ.get(keyx, 'DEFAULT') == 'DEFAULT'
            del environ[k]

    def test_get_list_path(self):
        paths = environ.get_list('PATH')
        assert len(paths) > 0
        for path in paths:
            if os.path.exists(path):
                break
        else:
            errmsg = 'No existing dirs found in PATH: {}'
            raise AssertionError(errmsg.format(paths))

    def test_get_list_when_value_is_none(self):
        key = 'KEY-X'
        with EnvironContext({key: None}):
            assert key not in environ
            assert environ.get_list(key) == []

            value = environ.get_list(key, ['/', '/users'])
            assert value and isinstance(value, (list, tuple))

    def test_home_and_user(self):
        user = environ.get('USER')
        assert user is not None

        home = environ.get('HOME')
        assert home is not None
        assert os.path.exists(home) and os.path.isdir(home)

        if os.name == 'nt':
            appdata = environ.get('APPDATA')
            assert appdata is not None
            assert os.path.exists(appdata) and os.path.isdir(appdata)
