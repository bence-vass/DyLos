from django.core.management.base import BaseCommand, CommandError
from ... import factories
import random


class Command(BaseCommand):
    help = 'Generate fake data and seed the models with them, default are 10'

    def add_arguments(self, parser):
        # https://docs.python.org/3/library/argparse.html#the-add-argument-method
        # Optional!
        parser.add_argument('--amount', type=int,
                            help='The amount of fake data you want')
        # parser.add_argument('amount', nargs='+', type=int)

    def handle(self, amount, *args, **options):
        factories.UserFactory.create_batch(amount)
