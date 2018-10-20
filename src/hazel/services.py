# pylint: disable=C0330, no-self-argument
from zope.interface import Attribute, Interface, implementer
from zope.interface.registry import Components


class ServiceError(Exception):
    """Exception thrown for service related errors."""


class IContext(Interface):
    """A marker interface for a context object.
    """

    registry = Attribute('registry')
    settings = Attribute('settings')


class IRegistry(Interface):
    """A marker interface for a registry dependency container.
    """

    _container = Attribute('_container')

    def find_service(iface, context, name):
        """Finds a service registered with the provided interface.

        This can be used to locate services registered either as a utility or
        factory service. If no service exists for either of the categories an
        error is thrown.
        """

    def register_service(service, iface, name):
        """Registers a singleton utility service."""

    def register_factory(factory, iface, requires, name):
        """Registers a service factory."""


@implementer(IContext)
class Context(dict):
    """Defines objects available within an execution context.
    """

    def __init__(self, registry=None, settings=None):
        super().__init__()
        if not registry:
            registry = Registry()

        self.registry = registry
        self.set_settings(settings)

    def set_settings(self, settings):
        if not settings:
            settings = {}
        self.update(settings)


@implementer(IRegistry)
class Registry:
    """A service registry for dependency management.
    """

    def __init__(self):
        self._component = Components()

    def find_service(self, iface, context=None, name=''):
        """Finds a service registered with the provided interface.

        This can be used to locate services registered either as a utility or
        factory service. If no service exists for either of the categories an
        error is thrown.
        """
        service = self._component.queryUtility(iface, name=name)
        if not service:
            service = self._component.queryAdapter(context, iface, name=name)

        if not service:
            msgfmt = "No utility or factory service found for {}"
            iface_name = getattr(iface, '__name__', str(iface))
            raise ServiceError(msgfmt.format(iface_name))
        return service

    def register_service(self, service, iface, name=''):
        """Registers a singleton utility service.

        A callable serving as a factory to lazily create the utility service
        can be provided in place of the service instance.
        """
        key = 'component' if not callable(service) else 'factory'
        kwargs = {'provided': iface, key: service, 'name': name}
        self._component.registerUtility(**kwargs)

    def register_factory(self, factory, iface, required=None, name=''):
        """Registers a service factory.
        """
        required = required or Interface
        if not isinstance(required, (list, tuple)):
            required = (required,)

        self._component.registerAdapter(
            factory=factory, provided=iface, required=required, name=name
        )


class SingletonMeta(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)

        cls.__instance = None
        original_new = cls.__new__

        def meta_new(cls, *args, **kwargs):
            if not cls.__instance:
                cls_obj = original_new(cls, *args, **kwargs)
                cls.__instance = cls_obj
            return cls.__instance

        # replace `__new__` method
        cls.__new__ = staticmethod(meta_new)


class RegistrySingleton(Registry, metaclass=SingletonMeta):
    """A singleton class for registering and managing services.
    """
