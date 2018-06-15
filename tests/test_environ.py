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
        for k, v in self.env_context.items():
            self.env_backup[k] = self.environ.get(k)
            if v:
                self.environ[k] = v
            elif k in self.environ:
                del self.environ[k]

    def __exit__(self, *exc_info):
        for k, v in self.env_backup.items():
            if v:
                self.environ[k] = v
            elif k in self.environ:
                del self.environ[k]
        return False


class TestEnviron:

    def test_get_set(self):
        k = 'HAZEL_ENV_MODULE'

        with EnvironContext({k: None}):
            assert k not in environ
            pytest.raises(KeyError, environ.__getitem__, k)
            assert environ.get(k) is None
            assert environ.get(k, 'FOO') == 'FOO'

            environ[k] = 'BAR'
            assert environ.get(k, 'FOO') == 'BAR'
            assert environ.get(k) == 'BAR'
            assert len(environ) > 0
            assert k in environ

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
