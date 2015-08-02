"""
Hello World Nameko Microservice
"""
import random

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
