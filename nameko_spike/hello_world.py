"""
Hello World Nameko Microservice
"""
import json
import random

from nameko.events import event_handler, EventDispatcher, BROADCAST
from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http


class GreetingService:
    name = 'greeting_service'

    title_builder = RpcProxy('title_builder')

    @rpc
    def hello(self, name):
        full_name = self.title_builder.build_name(name=name)
        return 'Hello {}!'.format(full_name)


class NameBuilder:
    name = 'title_builder'

    available_titles = [
        'The Great',
        'The Destroyer',
        'The Wise',
        'The Grim',
    ]

    @rpc
    def build_name(self, name):
        title = random.choice(self.available_titles)

        return '{} {}'.format(name, title)


class WatchDog:
    name = 'watchdog'

    dispatch = EventDispatcher()

    @rpc
    def bark(self):
        self.dispatch('bark', 'Woof!')


class SleepyGuard:
    name = 'sleepy_guard'

    @event_handler('watchdog', 'bark', handler_type=BROADCAST, reliable_delivery=False)
    def wake_up(self, payload):
        print('Oi! I\'m not sleeping, no need to bark!')


class AwareGuard:
    name = 'aware_guard'

    @event_handler('watchdog', 'bark', handler_type=BROADCAST, reliable_delivery=False)
    def on_bark(self, payload):
        print('Good boy!')


class HttpService:
    name = 'http_service'

    @http('GET', '/get_user/<int:id>')
    def on_get(self, request, id):
        return json.dumps({
            'summary': 'Here is a list of user {} properties ...'.format(id),
            'values': [],
        })

    @http('POST', '/save_state')
    def on_post(self, request):
        return 201, 'The game state has been saved! {}'.format(request.get_data())

