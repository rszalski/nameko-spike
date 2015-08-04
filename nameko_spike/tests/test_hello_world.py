from nameko.runners import ServiceRunner
from nameko.testing.services import worker_factory, entrypoint_hook, replace_dependencies
from nameko.testing.utils import get_container
from nameko_spike.hello_world import GreetingService, NameBuilder


class TestGreetingService:
    def test_greeting_service__given_name__should_format_it(self):
        service = worker_factory(GreetingService)
        service.title_builder.build_name.side_effect = lambda name: name

        assert service.hello(name='Man') == 'Hello Man!'

class TestNameBuilderService:
    def test_name_builder__given_name__should_pick_available_title(self):
        service = worker_factory(NameBuilder)
        service.available_titles = ['The Title']

        assert service.build_name('name') == 'name The Title'
