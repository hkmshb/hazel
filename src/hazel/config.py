import base64
import binascii
import uuid


#: boolean string reprs
TRUTHY = frozenset(('true', 't', 'yes', 'y', '1'))
FALSEY = frozenset(('false', 'f', 'no', 'n', '0'))


def get_version():  # pragma: no cover
    """Returns the version details for the package.
    """
    import pkg_resources

    package = pkg_resources.require('hazel')
    return package[0].version


def asbool(strval):
    """Returns the boolean value ``True`` if the case-lowered value of string
    input ``s`` is a :term:``truthy string `. If ``s`` is already one of the
    boolean values ``True`` or ``False``, return it.
    """
    if strval is None:
        return False
    if isinstance(strval, bool):
        return strval
    strval = str(strval).strip()
    return strval.lower() in TRUTHY


def asenum(enum_type, plain_value):
    """Returns the enum value for specified ``enum_type`` that matches the
    specified string or numeric value as provided in ``plain_value``.
    """
    if plain_value is not None:
        if isinstance(plain_value, int) or plain_value.isdigit():
            plain_value = int(plain_value)
            try:
                return enum_type(plain_value)
            except ValueError:
                return None
        plain_value = str(plain_value)
        if plain_value and hasattr(enum_type, plain_value):
            return enum_type[plain_value]
    return None


def aslist_cronly(value):
    if isinstance(value, str):
        value = filter(None, [x.strip() for x in value.splitlines()])
    return list(value)


def aslist(value, flatten=True):
    """Returns a list of strings, separating the input based on newlines
    and, if flatten=True (the default), also split on spaces within each
    line.
    """
    values = aslist_cronly(value)
    if not flatten:
        return values
    result = []
    for val in values:
        subvalues = val.split()
        result.extend(subvalues)
    return result


def uuid_to_slug(uuid_obj):
    """Converts UUID object to a compact base64 string representation.
    """
    # catch some common typing errors
    assert isinstance(uuid_obj, uuid.UUID)
    encoded = base64.b64encode(uuid_obj.bytes)

    # URLs don't like +
    return (
        encoded.decode('utf-8')
        .rstrip('=\n')
        .replace('/', '_')
        .replace('+', '-')
    )


def slug_to_uuid(slug):
    """Converts UUID slug string to UUID object.
    """
    assert isinstance(slug, str) is True
    try:
        slug = (slug + '==').replace('_', '/').replace('-', '+')
        slug_bytes = base64.b64decode(slug)
        return uuid.UUID(bytes=slug_bytes)
    except (ValueError, binascii.Error) as ex:
        err_msg = "Cannot decode supposed base64 slug: %s"
        raise ValueError(err_msg % slug) from ex
