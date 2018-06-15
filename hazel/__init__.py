#: retrieve Environ singleton instance
from hazel.environ import environ

#: boolean string reprs
truthy = frozenset(('true', 't', 'yes', 'y', '1'))
falsey = frozenset(('false', 'f', 'no', 'n', '0'))
