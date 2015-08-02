"""
Hello World Nameko Microservice
"""
import random

from nameko.events import event_handler, EventDispatcher, BROADCAST
from nameko.rpc import rpc, RpcProxy


class GreetingService(object):
    name = 'greeting_service'

    title_builder = RpcProxy('title_builder')

    @rpc
    def hello(self, name):
        full_name = self.title_builder.build_name(name=name)
        return 'Hello {}!'.format(full_name)


class NameBuilder(object):
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


class WatchDog(object):
    name = 'watchdog'

    dispatch = EventDispatcher()

    @rpc
    def bark(self):
        self.dispatch('bark', 'Woof!')


class SleepyGuard(object):
    name = 'sleepy_guard'

    @event_handler('watchdog', 'bark', handler_type=BROADCAST, reliable_delivery=False)
    def wake_up(self, payload):
        print('Oi! I\'m not sleeping, no need to bark!')


class AwareGuard(object):
    name = 'aware_guard'

    @event_handler('watchdog', 'bark', handler_type=BROADCAST, reliable_delivery=False)
    def on_bark(self, payload):
        print('Good boy!')
