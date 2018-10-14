'''Provides a wrapper class for os.environ

When this module is loaded it will try to set proper values for HOME
and USER if they are not set, and on Windows it will also try to set
APPDATA
'''
import collections
import logging
import os

_log = logging.getLogger('hazel')  # pylint: disable=invalid-name


class Environ(collections.MutableMapping):
    def __getitem__(self, key):
        return os.environ[key]

    def __setitem__(self, key, value):
        os.environ[key] = value

    def __delitem__(self, key):
        del os.environ[key]

    def __iter__(self):
        return iter(os.environ)

    def __len__(self):
        return len(os.environ)

    def get(self, key, default=None):
        '''Get a parameter from the environment like os.environ.get()

        :param key: the parameter to get
        :param default: the default if param does not exists
        :return: string
        '''
        try:
            value = self[key]
        except KeyError:
            return default
        else:
            if not value or value.isspace():
                return default
            return value

    def get_list(self, key, default=None, sep=None):
        '''Get a parameter from the environment and convert to a list.

        :param key: the parameter to get
        :param default: the default if param does not exists
        :param sep: optional separator, default to os.path.sep if not given
        :returns: a list or the default
        '''
        value = self.get(key, default)
        if value is None:
            return []
        if isinstance(value, str):
            if sep is None:
                sep = os.pathsep
            return value.split(sep)
        assert isinstance(value, (list, tuple))
        return value


# Singleton Instance
environ = Environ()  # pylint: disable=invalid-name


if os.name == 'nt':  # pragma: no cover
    # Windows specific environment variables
    if 'USER' not in environ or not environ['USER']:
        environ['USER'] = environ['USERNAME']
    if 'HOME' not in environ or not environ['HOME']:
        if 'USERPROFILE' in environ:
            environ['HOME'] = environ['USERPROFILE']
        elif 'HOMEDRIVE' in environ and 'HOMEPATH' in environ:
            environ['HOME'] = environ['HOMEDRIVE'] + environ['HOMEPATH']
    if 'APPDATA' not in environ or not environ['APPDATA']:
        environ['APPDATA'] = environ['HOME'] + '\\Application Data'


if not os.path.isdir(environ['HOME']):  # pragma: no cover
    _log.error(
        "Env variable $HOME does not point to an existing directory: %s",
        environ['HOME'],
    )


if 'USER' not in environ or not environ['USER']:  # pragma: no cover
    environ['USER'] = os.path.basename(environ['HOME'])
    _log.error(
        "Env variable $USER had no value and got set to %s", environ['USER']
    )
