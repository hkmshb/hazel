# pylint: disable=protected-access
import pytest
from zope.interface import Interface
from hazel.services import Context, Registry, RegistrySingleton


class TestContext:
    def test_context_is_dict_and_empty_by_default(self):
        context = Context()
        assert isinstance(context, dict) is True
        assert list(context.keys()) == []
        assert context.registry is not None

    def test_getting_settings_from_context(self):
        context = Context(settings={'gender': 'male', 'age': 7})
        assert 'gender' in context
        assert 'age' in context


class TestRegistrar:
    def test_singleton_nature(self):
        reg1 = RegistrySingleton()
        reg2 = RegistrySingleton()
        assert reg1 == reg2
        assert reg1._component == reg2._component

    def test_resolve_service_factory_by_type(self):
        def foo_factory(context):
            assert context == 'bolo'
            return 'foo-factory'

        def bar_factory(context):
            assert context is None
            return 'bar-factory'

        registry = Registry()
        registry.register_factory(foo_factory, IFooService)
        registry.register_factory(bar_factory, IBarService)

        factory = registry.find_service(IFooService, 'bolo')
        assert factory is not None
        assert factory == 'foo-factory'

        factory2 = registry.find_service(IBarService)
        assert factory2 is not None
        assert factory2 == 'bar-factory'
        assert factory is not factory2

    def test_resolve_service_by_type(self):
        registry = Registry()
        registry.register_service(DummyService('bar'), IBarService)
        registry.register_service(DummyService('foo'), IFooService)

        srv = registry.find_service(IFooService)
        assert srv == 'foo'
        srv2 = registry.find_service(IBarService)
        assert srv2 == 'bar'

    def test_resolve_service_by_type_and_name(self):
        registry = Registry()
        registry.register_service(DummyService('foo'), IFooService, name='foo')
        registry.register_service(DummyService('bar'), IFooService, name='bar')

        srv = registry.find_service(IFooService, name='foo')
        assert srv == 'foo'
        srv = registry.find_service(IFooService, name='bar')
        assert srv == 'bar'

    def test_resolve_service_by_context(self):
        registry = Registry()
        registry.register_service(DummyService('foo'), IFooService)
        registry.register_service(
            DummyService('bar'), IFooService, name='bar-service'
        )

        srv = registry.find_service(IFooService)
        assert srv == 'foo'
        srv = registry.find_service(IFooService, name='bar-service')
        assert srv == 'bar'

    def test_find_service_fails_for_unregistered_service(self):
        from hazel.services import ServiceError

        registry = Registry()
        with pytest.raises(ServiceError):
            registry.find_service(IFooService)


class IFooService(Interface):
    pass


class IBarService(Interface):
    pass


class DummyService:
    def __init__(self, result):
        self.result = result

    def __call__(self):
        return self.result
