from django.core.management.base import BaseCommand, CommandError
from website.models import *
import datetime
from swingtime import models as swingtime
from django.contrib.auth.models import User
from decouple import config
from website.email import sendemail

class Command(BaseCommand):
    help = 'setup environment'

    def handle(self, *args, **options):
        try:
            #query region and find out which region which we need to send notification
            region = Region.objects.filter(notification=True)
            for re in region:
                print(re)
                sendemail('thiyaguj19@live.com', re, re)
        except Exception as err:
            self.stdout.write(self.style.ERROR('error creating the data'))
            print("err-message-", err)