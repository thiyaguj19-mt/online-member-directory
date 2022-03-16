from django.core.management.base import BaseCommand, CommandError
from website.models import *
import datetime
from swingtime import models as swingtime

class Command(BaseCommand):
    help = 'setup environment'

    def handle(self, *args, **options):
        try:
            et = swingtime.EventType.objects.create(abbr='even', label='SSIO event')
        except Exception as err:
            self.stdout.write(self.style.ERROR('.....'))
            print("err-message-", err)
        self.stdout.write(self.style.SUCCESS('...'))