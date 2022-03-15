from django.core.management.base import BaseCommand, CommandError
from website.models import *
import datetime

class Command(BaseCommand):
    help = 'setup environment'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('...'))